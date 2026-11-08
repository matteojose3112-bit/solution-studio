# Solution Studio

**A modular workshop for practical digital solutions.**

Solution Studio brings together five focused studios for research, document processing, data work, workflow automation and lightweight website generation. It favors deterministic code where possible, human review at decision points, and optional AI/integrations only where they add value.

<https://solution-studio-secb.onrender.com>

## Live demo

The application is deployed as a public Render web service. The health endpoint is available at [/api/health](https://solution-studio-secb.onrender.com/api/health).

- Python FastAPI backend and lightweight JavaScript frontend
- Five functional first-version studios
- Automated backend tests and frontend JavaScript syntax checks in GitHub Actions
- Free-tier hosting; the service may take longer to respond after periods of inactivity

## The five studios

| Studio | Current capabilities |
|---|---|
| **Research** | Builds structured briefs from up to eight user-provided source notes, with key points, linked references, limitations and Markdown export |
| **Documents** | Extracts text and metadata from PDF, DOCX and UTF-8 TXT files; provides downloadable text output |
| **Data** | Inspects, validates, cleans and transforms CSV/XLSX files; exports processed data |
| **Automation** | Runs allowlisted deterministic text workflows with preview, approval checkpoint, execution logs, output download and JSON workflow export |
| **Development** | Generates a responsive static business website starter ZIP containing HTML, CSS and setup notes |

## Technology

- **Backend:** Python, FastAPI, Uvicorn
- **Frontend:** HTML, CSS and JavaScript
- **Document/data libraries:** openpyxl, pypdf, python-docx
- **Quality:** pytest and GitHub Actions CI
- **Deployment:** Render

Core workflows do not require paid APIs. Optional future integrations may include AI model providers, n8n and Supabase.

## Run locally

Requires Python 3.10 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend/requirements.txt
uvicorn app.main:app --reload --app-dir backend
```

Open http://127.0.0.1:8000. Interactive API documentation is at http://127.0.0.1:8000/docs.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Service health |
| GET | `/api/version` | Application version |
| POST | `/api/research/report` | Create a source-note brief |
| POST | `/api/documents/extract` | Extract document text and metadata |
| POST | `/api/data/inspect` | Inspect CSV/XLSX data |
| POST | `/api/data/clean` | Clean and export data |
| POST | `/api/data/transform` | Transform columns and export |
| POST | `/api/automation/run` | Preview or execute an allowlisted workflow |
| POST | `/api/development/generate` | Generate a static website ZIP |

## Safeguards and known limitations

- Document uploads are limited to 10 MB; PDFs to 100 pages; DOCX archive expansion to 25 MB; extracted output to 100,000 characters.
- Research Studio organizes supplied notes; it does not automatically browse the web or independently verify sources.
- Document Studio extracts text and metadata; document conversion and editing are not implemented.
- Automation Studio supports built-in text actions only. It does not run arbitrary code or shell commands, make outbound requests, persist workflows or schedule jobs.
- Development Studio generates a static one-page starter. It does not create a custom backend, deploy or host the generated site.
- Uploaded files and workflow inputs are processed in memory and are not persisted.
- The public Render free-tier service may sleep when inactive.

## Tests

Run the backend test suite from the repository root:

```bash
pytest
```

The integrated backend suite has passed 58 tests. CI also checks frontend JavaScript syntax. Browser-level end-to-end testing of every studio remains a follow-up task.

## Repository structure

- `backend/` — FastAPI routes, processing services and tests
- `frontend/` — browser interface, studio modules and styles
- `docs/` — architecture and project documentation
- `examples/` — synthetic demonstration material
- `.github/` — CI workflows
- `ROADMAP.md` — implementation status and next phases
- `CHANGELOG.md` — project changes

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
