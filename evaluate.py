from __future__ import annotations

import json
from pathlib import Path

from query import ask


EVALUATION_QUESTIONS = [
    {
        "question": "Which Seoul restaurant should I choose if I want one of the oldest local soup institutions near Jongno or Insadong?",
        "expected": "Imun Seolnongtang should be recommended because it is an old Seoul seolleongtang institution near Jongno/Insadong and the corpus says it is one of Seoul/Korea's oldest restaurants.",
    },
    {
        "question": "I am staying in Myeongdong and want a classic old beef soup instead of a tourist-trap meal. What should I eat?",
        "expected": "Hadongkwan should be recommended for Myeongdong gomtang, with context that it dates to 1939 and is a historically meaningful beef-soup option.",
    },
    {
        "question": "What is a good summer-specific noodle dish in Seoul, and where should I try it?",
        "expected": "Jinju Hoegwan should be recommended for kongguksu, cold soybean noodles, especially during hot weather near City Hall, Deoksugung, or Namdaemun.",
    },
    {
        "question": "What cold noodle place should I try in Seoul, and how are the styles different?",
        "expected": "The answer should mention Woo Lae Oak for subtle, broth-focused Pyongyang naengmyeon and Gangnam Myeonok for Hamhung-style naengmyeon with chewy noodles and a spicier mixed style.",
    },
    {
        "question": "What place should I choose for a high-budget hanwoo splurge, and what should I not expect from it?",
        "expected": "Born and Bred should be recommended for premium hanwoo, special occasion, or polished beef dining; the answer should warn that it is not a cheap, old street-level local restaurant or market meal.",
    },
]


def summarize_chunks(result: dict) -> list[dict]:
    return [
        {
            "rank": index,
            "title": chunk["title"],
            "source_file": chunk["source_file"],
            "distance": round(chunk["distance"], 4),
            "preview": chunk["text"][:350].replace("\n", " "),
        }
        for index, chunk in enumerate(result["retrieved_chunks"], start=1)
    ]


def main() -> None:
    output = []
    for item in EVALUATION_QUESTIONS:
        result = ask(item["question"])
        output.append(
            {
                "question": item["question"],
                "expected": item["expected"],
                "answer": result["answer"],
                "sources": result["sources"],
                "retrieved_chunks": summarize_chunks(result),
            }
        )

    out_path = Path("data/evaluation_results.json")
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(output)} evaluation results to {out_path}")


if __name__ == "__main__":
    main()
