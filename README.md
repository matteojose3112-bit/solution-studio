# Solution Studio

**A modular toolkit for delivering custom AI-powered digital solutions.**

Solution Studio is a practical workspace for research, document processing, data analysis, workflow automation and custom digital tools. It uses the simplest reliable approach for each task: AI where it adds value, deterministic code where it does not, and human review throughout.

## Current foundation

The first runnable application is now in place:
- Python **FastAPI** backend.
- Lightweight, responsive **JavaScript** frontend.
- API health and version endpoints.
- Backend tests and GitHub Actions CI.
- **Data Studio:** CSV and XLSX inspection, column type inference, missing-value and inconsistent-value warnings, preview, whitespace cleanup, blank-row removal, duplicate-row removal and cleaned-file downloads.
- One local server for both the API and browser interface.

<badge color="success">Runnable foundation</badge>

## The five studios

| Studio | Intended capabilities |
|---|---|
| Research | Source-based research, comparisons, summaries and reports |
| Documents | PDF and office-document extraction, transformation and exports |
| Data | CSV/XLSX cleanup, validation, analysis and reporting |
| Automation | Integrations, repeatable workflows, approvals and notifications |
| Development | Custom websites, dashboards, prototypes and business tools |

Research, Document, Automation and Development remain planned modules. Data Studio has working CSV and XLSX workflows.

## Technology

- **Python / FastAPI** — backend and processing services
- **JavaScript** — browser interface and selected Node.js integrations
- **SQL** — structured data operations
- **SQLite** — planned lightweight local persistence
- **Optional integrations** — n8n, Supabase and AI model providers

Core development is local-first. Paid APIs and hosted services are not required to run the current foundation.

## Run locally

Requires Python 3.10 or newer.

```bash
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.venv\\Scripts\\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Install and start:

```bash
python -m pip install -r backend/requirements.txt
uvicorn app.main:app --reload --app-dir backend
```

Open **http://127.0.0.1:8000**. Interactive API documentation is at **http://127.0.0.1:8000/docs**.

### API endpoints

- `GET /api/health` — service health
- `GET /api/version` — application version
- `POST /api/data/inspect` — inspect an uploaded CSV or XLSX workbook (multipart field: `file`)
- `POST /api/data/clean` — clean and download an uploaded CSV or XLSX workbook; accepts `trim_whitespace`, `remove_empty_rows` and `remove_duplicate_rows` query options

### Run tests

```bash
pytest
```

## Repository layout

```text
backend/       FastAPI application, CSV processing services and tests
frontend/      Static JavaScript interface, Data Studio module and styles
docs/          Architecture and project documentation
examples/      Synthetic demonstration material
tests/         Shared test resources
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
