from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


DOCUMENTS_DIR = Path("documents")
DATA_DIR = Path("data")
CHUNKS_PATH = DATA_DIR / "chunks.json"
CHUNK_SIZE = 700
CHUNK_OVERLAP = 150


@dataclass
class Document:
    title: str
    source_type: str
    url: str
    path: str
    text: str


@dataclass
class Chunk:
    id: str
    text: str
    title: str
    source_type: str
    url: str
    source_file: str
    chunk_index: int


def _field(raw: str, name: str) -> str:
    match = re.search(rf"^{name}:\s*(.+)$", raw, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def _document_text(raw: str) -> str:
    marker = "DOCUMENT_TEXT:"
    if marker in raw:
        return raw.split(marker, 1)[1].strip()
    return raw.strip()


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def load_documents(documents_dir: Path = DOCUMENTS_DIR) -> list[Document]:
    documents: list[Document] = []
    for path in sorted(documents_dir.glob("*.txt")):
        raw = path.read_text(encoding="utf-8")
        title = _field(raw, "TITLE") or path.stem.replace("_", " ").title()
        source_type = _field(raw, "SOURCE_TYPE") or "Text source"
        url = _field(raw, "URL") or "No URL provided"
        text = clean_text(_document_text(raw))
        if text:
            documents.append(
                Document(
                    title=title,
                    source_type=source_type,
                    url=url,
                    path=str(path),
                    text=text,
                )
            )
    return documents


def _split_long_paragraph(paragraph: str, chunk_size: int) -> list[str]:
    sentences = re.split(r"(?<=[.!?。])\s+", paragraph)
    parts: list[str] = []
    current = ""
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        if current and len(current) + 1 + len(sentence) > chunk_size:
            parts.append(current)
            current = sentence
        else:
            current = f"{current} {sentence}".strip()
    if current:
        parts.append(current)
    return parts


def _with_overlap(chunks: list[str], overlap: int) -> list[str]:
    if overlap <= 0:
        return chunks
    overlapped: list[str] = []
    previous_tail = ""
    for chunk in chunks:
        combined = f"{previous_tail}\n{chunk}".strip() if previous_tail else chunk
        overlapped.append(combined)
        tail = chunk[-overlap:]
        boundary = re.search(r"\s", tail)
        previous_tail = tail[boundary.end() :].strip() if boundary else tail.strip()
    return overlapped


def chunk_document(
    document: Document,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[str]:
    paragraphs = [p.strip() for p in document.text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current = ""

    for paragraph in paragraphs:
        paragraph_parts = (
            _split_long_paragraph(paragraph, chunk_size)
            if len(paragraph) > chunk_size
            else [paragraph]
        )
        for part in paragraph_parts:
            if current and len(current) + 2 + len(part) > chunk_size:
                chunks.append(current)
                current = part
            else:
                current = f"{current}\n\n{part}".strip()

    if current:
        chunks.append(current)

    titled_chunks = [f"{document.title}\n\n{chunk}" for chunk in _with_overlap(chunks, overlap)]
    return [chunk for chunk in titled_chunks if len(chunk.strip()) > 0]


def build_chunks(documents: Iterable[Document]) -> list[Chunk]:
    chunks: list[Chunk] = []
    for document in documents:
        for index, text in enumerate(chunk_document(document)):
            source_stem = Path(document.path).stem
            chunks.append(
                Chunk(
                    id=f"{source_stem}-{index}",
                    text=text,
                    title=document.title,
                    source_type=document.source_type,
                    url=document.url,
                    source_file=document.path,
                    chunk_index=index,
                )
            )
    return chunks


def save_chunks(chunks: list[Chunk], path: Path = CHUNKS_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps([asdict(chunk) for chunk in chunks], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> None:
    documents = load_documents()
    chunks = build_chunks(documents)
    save_chunks(chunks)

    print(f"Loaded {len(documents)} documents")
    print(f"Wrote {len(chunks)} chunks to {CHUNKS_PATH}")
    print()
    print("Sample chunks:")
    for chunk in chunks[:5]:
        preview = chunk.text.replace("\n", " ")
        print(f"- {chunk.id} | {chunk.title} | {preview[:240]}...")


if __name__ == "__main__":
    main()
