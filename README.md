# Solution Studio

**A modular toolkit for delivering custom AI-powered digital solutions.**

Solution Studio is a practical workspace for research, document processing, data analysis, workflow automation and custom digital tools. It uses the simplest reliable approach for each task: AI where it adds value, deterministic code where it does not, and human review throughout.

## Current foundation

- Python **FastAPI** backend and lightweight **JavaScript** frontend.
- API health/version endpoints, automated backend tests and GitHub Actions CI.
- **Research Studio:** source-linked working briefs from up to eight user-provided source notes, with key points, limitations and Markdown export.
- **Document Studio:** in-memory text and metadata extraction from PDF, DOCX and UTF-8 TXT files, with downloadable text export.
- **Data Studio:** CSV/XLSX inspection, validation, cleanup, column transformations and exports.
- **Automation Studio:** compose up to eight deterministic text-processing steps, preview output, require approval, inspect execution logs and export workflow JSON.
- One local server for both the API and browser interface.

## The five studios

| Studio | Capabilities |
|---|---|
| Research | Source-note briefs, linked references and Markdown reports |
| Documents | PDF/DOCX/TXT text extraction, metadata and text export |
| Data | CSV/XLSX cleanup, validation, transformations and exports |
| Automation | Allowlisted text workflows, previews, approval checkpoints and execution logs |
| Development | Custom websites, dashboards, prototypes and business tools — planned |

## Technology

- **Python / FastAPI** — backend and processing services
- **JavaScript** — browser interface and studio workflows
- **openpyxl, pypdf, python-docx** — spreadsheet and document processing
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
- `POST /api/research/report` — create a source-linked brief from a question and 1–8 source records
- `POST /api/documents/extract` — extract text and metadata from PDF, DOCX or TXT uploads
- `POST /api/data/inspect` — inspect an uploaded CSV/XLSX file
- `POST /api/data/clean` — clean and export an uploaded CSV/XLSX file
- `POST /api/data/transform` — rename, normalize, select/reorder columns and clean before export
- `POST /api/automation/run` — preview or execute a workflow made from allowlisted steps

### Document safeguards

- 10 MB maximum upload; PDF limited to 100 pages.
- DOCX archive expansion limited to 25 MB.
- Extracted output limited to 100,000 characters.
- Password-protected PDFs and non-UTF-8 text files are not supported.
- Files are processed in memory and are not persisted.

### Automation safeguards

- Maximum 20,000 input characters and eight steps per workflow.
- Only built-in, allowlisted text actions can run; arbitrary code and shell commands are not accepted.
- Approval is required by default. Preview and execution are stateless.
- No third-party API calls, webhooks or notifications are performed by this initial module.

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
