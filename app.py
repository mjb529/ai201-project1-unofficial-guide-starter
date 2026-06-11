from __future__ import annotations

import gradio as gr

from query import ask


def handle_query(question: str) -> tuple[str, str, str]:
    question = question.strip()
    if not question:
        return "Enter a question first.", "", ""

    result = ask(question)
    sources = "\n".join(
        f"- {source['title']}\n  {source['source_file']}\n  {source['url']}"
        for source in result["sources"]
    )
    retrieved = "\n\n".join(
        "\n".join(
            [
                f"{index}. {chunk['title']}",
                f"distance: {chunk['distance']:.4f}",
                f"source: {chunk['source_file']}",
                chunk["text"][:700],
            ]
        )
        for index, chunk in enumerate(result["retrieved_chunks"], start=1)
    )
    return result["answer"], sources, retrieved


with gr.Blocks(title="Unofficial Korea Guide") as demo:
    gr.Markdown("# Unofficial Korea Guide")
    gr.Markdown("Ask about Seoul restaurants, old local food institutions, and food-centered activities.")
    question = gr.Textbox(label="Question", placeholder="Where should I get a classic old beef soup near Myeongdong?")
    ask_button = gr.Button("Ask")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Sources", lines=8)
    retrieved = gr.Textbox(label="Retrieved chunks", lines=12)

    ask_button.click(handle_query, inputs=question, outputs=[answer, sources, retrieved])
    question.submit(handle_query, inputs=question, outputs=[answer, sources, retrieved])


if __name__ == "__main__":
    demo.launch(server_port=8008)
