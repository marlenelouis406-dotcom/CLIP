"""FastHTML app that turns rough ideas into structured markdown drafts using OpenAI."""

from __future__ import annotations

import os
from textwrap import dedent

from fasthtml.common import Div, Form, H1, H2, Label, Main, P, Pre, Script, Section, Style, Textarea, Button, Input, fast_app, serve
from openai import OpenAI

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
SYSTEM_PROMPT = dedent(
    """
    You are a professional drafting assistant.
    Convert rough user ideas into clean, structured markdown drafts.

    Always respond in markdown format with this structure:
    # Draft Title
    ## Objective
    ## Audience
    ## Key Points
    ## Draft Content
    ## Next Steps

    Keep the draft clear and practical. Do not include extra commentary outside the markdown draft.
    """
).strip()


def generate_markdown_draft(idea: str, extra_context: str = "") -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return """# Missing API Key\n\nPlease set `OPENAI_API_KEY` before generating drafts."""

    client = OpenAI(api_key=api_key)
    user_prompt = dedent(
        f"""
        User idea:
        {idea.strip()}

        Additional context:
        {extra_context.strip() or 'None'}
        """
    ).strip()

    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
    )
    return response.output_text.strip()


app, rt = fast_app()


@rt("/")
def get():
    return Main(
        Style(
            """
            body { font-family: Inter, system-ui, sans-serif; margin: 0; background: #f7f8fb; color: #1f2937; }
            .container { max-width: 960px; margin: 0 auto; padding: 2rem 1rem 3rem; }
            .card { background: white; border-radius: 12px; box-shadow: 0 8px 30px rgba(0,0,0,.08); padding: 1.2rem; margin-bottom: 1rem; }
            textarea, input { width: 100%; border: 1px solid #cbd5e1; border-radius: 8px; padding: .7rem; font-size: .96rem; }
            button { background: #2563eb; color: white; border: none; border-radius: 8px; padding: .7rem 1rem; font-weight: 600; cursor: pointer; }
            button:hover { background: #1d4ed8; }
            pre { white-space: pre-wrap; padding: 1rem; background: #0f172a; color: #e2e8f0; border-radius: 8px; overflow-x: auto; }
            .muted { color: #64748b; font-size: .9rem; }
            .row { display: grid; grid-template-columns: 1fr; gap: 1rem; }
            @media (min-width: 900px) { .row { grid-template-columns: 1fr 1fr; } }
            """
        ),
        Div(
            H1("Idea → Structured Markdown Draft"),
            P(
                f"Model: {OPENAI_MODEL}. Enter rough notes below, then generate a polished markdown draft.",
                cls="muted",
            ),
            Section(
                Form(
                    Label("Your idea"),
                    Textarea(
                        "",
                        name="idea",
                        rows=8,
                        placeholder="Example: Launch a weekly newsletter for indie developers with practical AI tips...",
                        required=True,
                    ),
                    Label("Extra context (optional)"),
                    Input(
                        name="extra_context",
                        placeholder="Tone, brand voice, target audience, deadline, etc.",
                    ),
                    Button("Generate Draft", type="submit"),
                    hx_post="/generate",
                    hx_target="#draft-output",
                    hx_swap="innerHTML",
                    cls="card",
                ),
                Div(
                    H2("Generated Markdown"),
                    Div(
                        P("Your generated markdown will appear here."),
                        id="draft-output",
                        cls="card",
                    ),
                ),
                cls="row",
            ),
            Script(src="https://unpkg.com/htmx.org@1.9.12"),
            cls="container",
        ),
    )


@rt("/generate", methods=["POST"])
def post(idea: str, extra_context: str = ""):
    if not idea.strip():
        return Div(P("Please enter an idea before generating."))

    draft = generate_markdown_draft(idea, extra_context)
    return Div(
        Pre(draft),
        P("Tip: copy this markdown into your editor or docs workflow.", cls="muted"),
    )


if __name__ == "__main__":
    serve()
