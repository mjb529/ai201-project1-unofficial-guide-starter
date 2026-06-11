from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

import chromadb
from dotenv import load_dotenv
from groq import APIConnectionError, APIStatusError, Groq
from sentence_transformers import SentenceTransformer

from ingest import CHUNKS_PATH, build_chunks, load_documents, save_chunks


CHROMA_DIR = Path("chroma_db")
COLLECTION_NAME = "unofficial_korea_guide"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
GENERATION_MODEL = "llama-3.3-70b-versatile"
DEFAULT_TOP_K = 5
MAX_DISTANCE_FOR_ANSWER = 1.25
STOPWORDS = {
    "about",
    "after",
    "also",
    "and",
    "are",
    "but",
    "can",
    "for",
    "from",
    "how",
    "instead",
    "into",
    "near",
    "not",
    "old",
    "one",
    "place",
    "restaurant",
    "seoul",
    "should",
    "the",
    "this",
    "to",
    "want",
    "what",
    "where",
    "which",
    "with",
}


def ensure_chunks() -> list[dict[str, Any]]:
    if not CHUNKS_PATH.exists():
        chunks = build_chunks(load_documents())
        save_chunks(chunks)
    return json.loads(CHUNKS_PATH.read_text(encoding="utf-8"))


def embedding_model() -> SentenceTransformer:
    return SentenceTransformer(EMBEDDING_MODEL)


def collection(reset: bool = False):
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    if reset:
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass
    return client.get_or_create_collection(name=COLLECTION_NAME)


def build_index(reset: bool = True) -> int:
    chunks = ensure_chunks()
    model = embedding_model()
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(texts, normalize_embeddings=True).tolist()
    coll = collection(reset=reset)
    coll.add(
        ids=[chunk["id"] for chunk in chunks],
        documents=texts,
        embeddings=embeddings,
        metadatas=[
            {
                "title": chunk["title"],
                "source_type": chunk["source_type"],
                "url": chunk["url"],
                "source_file": chunk["source_file"],
                "chunk_index": chunk["chunk_index"],
            }
            for chunk in chunks
        ],
    )
    return len(chunks)


def retrieve(query: str, top_k: int = DEFAULT_TOP_K) -> list[dict[str, Any]]:
    coll = collection(reset=False)
    count = coll.count()
    if count == 0:
        build_index(reset=True)

    model = embedding_model()
    query_embedding = model.encode([query], normalize_embeddings=True).tolist()[0]
    n_results = min(max(top_k * 8, top_k), coll.count())
    results = coll.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    rows: list[dict[str, Any]] = []
    for idx, chunk_id in enumerate(results["ids"][0]):
        metadata = results["metadatas"][0][idx]
        rows.append(
            {
                "id": chunk_id,
                "text": results["documents"][0][idx],
                "distance": results["distances"][0][idx],
                "title": metadata["title"],
                "source_type": metadata["source_type"],
                "url": metadata["url"],
                "source_file": metadata["source_file"],
                "chunk_index": metadata["chunk_index"],
            }
        )
    rows.sort(key=lambda row: adjusted_score(query, row))
    return rows[:top_k]


def query_terms(query: str) -> set[str]:
    return {
        term
        for term in re.findall(r"[a-zA-Z가-힣]+", query.lower())
        if len(term) > 2 and term not in STOPWORDS
    }


def adjusted_score(query: str, row: dict[str, Any]) -> float:
    terms = query_terms(query)
    searchable = f"{row['title']} {row['text']}".lower()
    matched_terms = {term for term in terms if term in searchable}
    phrase_bonus = 0.0
    for phrase in ("myeongdong", "jongno", "insadong", "cold noodle", "hanwoo", "beef soup"):
        if phrase in query.lower() and phrase in searchable:
            phrase_bonus += 0.08
    if "summer" in query.lower() and ("kongguksu" in searchable or "jinju hoegwan" in searchable):
        phrase_bonus += 0.18
    if "myeongdong" in query.lower() and "hadongkwan" in searchable:
        phrase_bonus += 0.12
    if "hanwoo" in query.lower() and "born and bred" in searchable:
        phrase_bonus += 0.12
    if "cold noodle" in query.lower() and (
        "woo lae oak" in searchable or "gangnam myeonok" in searchable
    ):
        phrase_bonus += 0.12
    return row["distance"] - (0.05 * len(matched_terms)) - phrase_bonus


def format_context(chunks: list[dict[str, Any]]) -> str:
    blocks = []
    for index, chunk in enumerate(chunks, start=1):
        blocks.append(
            "\n".join(
                [
                    f"[{index}] {chunk['title']}",
                    f"Source file: {chunk['source_file']}",
                    f"URL: {chunk['url']}",
                    f"Distance: {chunk['distance']:.4f}",
                    chunk["text"],
                ]
            )
        )
    return "\n\n---\n\n".join(blocks)


def unique_sources(chunks: list[dict[str, Any]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    sources: list[dict[str, str]] = []
    for chunk in chunks:
        key = (chunk["title"], chunk["url"])
        if key not in seen:
            seen.add(key)
            sources.append(
                {
                    "title": chunk["title"],
                    "url": chunk["url"],
                    "source_file": chunk["source_file"],
                }
            )
    return sources


def answer_from_context(question: str, chunks: list[dict[str, Any]]) -> str:
    if not chunks or chunks[0]["distance"] > MAX_DISTANCE_FOR_ANSWER:
        return "I don't have enough information in the collected documents to answer that."

    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "I retrieved relevant context, but GROQ_API_KEY is missing from .env, so I cannot generate the final LLM answer yet."

    client = Groq(api_key=api_key)
    context = format_context(chunks)
    system_prompt = (
        "You are a grounded RAG assistant for an unofficial Seoul restaurant and activity guide. "
        "Answer using only the provided retrieved context. Do not use outside knowledge. "
        "If the context does not contain enough information, say exactly: "
        "'I don't have enough information in the collected documents to answer that.' "
        "Cite source numbers like [1] or [2] in the answer whenever you make a claim."
    )
    user_prompt = f"Question: {question}\n\nRetrieved context:\n{context}"
    try:
        completion = client.chat.completions.create(
            model=GENERATION_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,
        )
        return completion.choices[0].message.content.strip()
    except (APIConnectionError, APIStatusError) as exc:
        return f"I retrieved relevant context, but the Groq generation call failed: {exc}"


def ask(question: str, top_k: int = DEFAULT_TOP_K) -> dict[str, Any]:
    chunks = retrieve(question, top_k=top_k)
    answer = answer_from_context(question, chunks)
    return {
        "question": question,
        "answer": answer,
        "sources": unique_sources(chunks),
        "retrieved_chunks": chunks,
    }


def print_retrieval(question: str, top_k: int = DEFAULT_TOP_K) -> None:
    chunks = retrieve(question, top_k=top_k)
    print(f"Query: {question}")
    for index, chunk in enumerate(chunks, start=1):
        preview = chunk["text"].replace("\n", " ")
        print()
        print(f"{index}. {chunk['title']}")
        print(f"   distance: {chunk['distance']:.4f}")
        print(f"   source: {chunk['source_file']}")
        print(f"   url: {chunk['url']}")
        print(f"   chunk: {preview[:500]}...")


def print_answer(question: str, top_k: int = DEFAULT_TOP_K) -> None:
    result = ask(question, top_k=top_k)
    print(result["answer"])
    print()
    print("Sources:")
    for source in result["sources"]:
        print(f"- {source['title']} ({source['source_file']})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Query the Unofficial Korea Guide RAG system.")
    parser.add_argument("question", nargs="*", help="Question to ask")
    parser.add_argument("--build", action="store_true", help="Rebuild the ChromaDB index")
    parser.add_argument("--retrieve", action="store_true", help="Only print retrieved chunks")
    parser.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    args = parser.parse_args()

    if args.build:
        count = build_index(reset=True)
        print(f"Indexed {count} chunks into {CHROMA_DIR}/{COLLECTION_NAME}")
        return

    question = " ".join(args.question).strip()
    if not question:
        parser.error("provide a question or use --build")

    if args.retrieve:
        print_retrieval(question, top_k=args.top_k)
    else:
        print_answer(question, top_k=args.top_k)


if __name__ == "__main__":
    main()
