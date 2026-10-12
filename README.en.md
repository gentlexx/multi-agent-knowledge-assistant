# Multi-Agent Knowledge Assistant

[中文](README.md) · [English](README.en.md) · [Demo](docs/demo.md) · [Verification](docs/verification.md)

A Python assistant for small personal knowledge bases. It plans each request, routes it to either a RAG pipeline or a ReAct tool agent, and synthesizes the final response with short-term conversation context.

## Highlights

- Planner–executor–writer workflow with visible routing and tool traces.
- Three-stage RAG/Agent routing: explicit keywords, BM25/vector hybrid retrieval, then LLM fallback.
- Local `.txt` ingestion, chunking, Chroma retrieval, and context-grounded answers.
- In-process memory for the latest 20 conversation turns.
- ReAct tools for weather, time, safe arithmetic, search, calendar, notes, and optional email.
- Gradio primary UI and a Streamlit alternative.

## Quick start

Python 3.11 is recommended. The default embedding model is downloaded on first use; `EMBEDDING_MODEL` may point to a local model directory instead.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python app.py
```

Set `ZHIPU_API_KEY` in `.env`, then open `http://127.0.0.1:7861`. The alternative UI starts with `streamlit run app_st.py`.

## Validation

```bash
python -m compileall -q src app.py app_st.py
pytest
ruff check src tests
```

Offline tests cover source syntax, arithmetic-expression safety, and note-path isolation. GitHub Actions repeats compilation, tests, and repository-content auditing on every push and pull request. End-to-end RAG and Agent execution requires external model access; see [docs/verification.md](docs/verification.md).

## Current limitations

- Memory is process-local and has no persistence or user isolation.
- Only `.txt` knowledge files are supported; index rebuilding is synchronous.
- Weather and search rely on public network services; email remains disabled without SMTP settings.
- Routing thresholds were manually tuned and do not yet have a benchmark dataset.
- The displayed process is an application-level route/tool trace, not private model reasoning.

The repository author led requirements, workflow design, task breakdown, review, fixes, and acceptance while using AI coding tools during implementation. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for dependency attribution. Code is licensed under the [MIT License](LICENSE).
