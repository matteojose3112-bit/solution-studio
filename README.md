# Solution Studio

**A modular toolkit for delivering custom AI-powered digital solutions.**

Solution Studio is a practical workspace for research, document processing, data analysis, workflow automation and custom digital tools. It uses the simplest reliable approach for each task: AI where it adds value, deterministic code where it does not, and human review throughout.

## Current foundation

- Python **FastAPI** backend and lightweight **JavaScript** frontend.
- API health/version endpoints, automated backend tests and GitHub Actions CI.
- **Research Studio:** turn a research question and up to eight user-supplied source notes into a structured brief with key points, linked references and explicit limitations. Reports can be downloaded as Markdown. It does not crawl or verify source pages.
- **Data Studio:** CSV/XLSX inspection, column type inference, missing/inconsistent-value warnings, preview, cleanup, explicit column renaming, snake_case normalization, column selection/reordering and CSV/XLSX exports.
- One local server for both the API and browser interface.

## The five studios

| Studio | Capabilities |
|---|---|
| Research | Source-note briefs, comparisons, linked references and Markdown reports |
| Documents | PDF and office-document extraction, transformation and exports — planned |
| Data | CSV/XLSX cleanup, validation, transformations and exports |
| Automation | Integrations, repeatable workflows, approvals and notifications — planned |
| Development | Custom websites, dashboards, prototypes and business tools — planned |

## Technology

- **Python / FastAPI** — backend and processing services
- **JavaScript** — browser interface and selected Node.js integrations
- **SQL / SQLite** — optional future structured persistence
- **Optional integrations** — n8n, Supabase and AI model providers

Core modules are local-first. Paid APIs and hosted services are not required for the current workflows.

## Run locally

Requires Python 3.10 or newer.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r backend/requirements.txt
uvicorn app.main:app --reload --app-dir backend
```

Open **http://127.0.0.1:8000**. Interactive API documentation is at **http://127.0.0.1:8000/docs**.

### API endpoints

- `GET /api/health` — service health
- `GET /api/version` — application version
- `POST /api/research/report` — create a source-linked brief from a question and 1–8 source records (`title`, `url`, `notes`)
- `POST /api/data/inspect` — inspect an uploaded CSV/XLSX file
- `POST /api/data/clean` — clean and export an uploaded CSV/XLSX file
- `POST /api/data/transform` — rename, normalize, select/reorder columns and clean before export

### Run tests

```bash
pytest
```

## Repository layout

```text
backend/       FastAPI routes, processing services and tests
frontend/      Static JavaScript interface, studio modules and styles
docs/          Architecture and project documentation
examples/      Synthetic demonstration material
.github/       CI workflows
ROADMAP.md     Planned implementation phases
CHANGELOG.md   Verified project changes
```

## Principles

1. Start with the client's actual task and required deliverable.
2. Use AI only when it improves the result.
3. Validate inputs and outputs; preserve human oversight.
4. Protect private files, customer data and credentials.
5. Keep modules reusable, testable and independently understandable.
6. Prefer complete, reliable demonstrations over unfinished feature counts.

Never commit API keys, credentials, private client documents or real customer data. Use synthetic or explicitly authorized sample data.

## License

MIT. See [LICENSE](LICENSE).
