# Solution Studio

**A modular toolkit for delivering custom AI-powered digital solutions.**

Solution Studio is a practical workspace for research, document processing, data analysis, workflow automation and custom digital tools. It uses the simplest reliable approach for each task: AI where it adds value, deterministic code where it does not, and human review throughout.

## Current foundation

- Python FastAPI backend and lightweight JavaScript frontend.
- API health/version endpoints, automated backend tests and GitHub Actions CI.
- **Research Studio:** source-linked working briefs from up to eight user-provided source notes, with key points, limitations and Markdown export.
- **Document Studio:** in-memory text and metadata extraction from PDF, DOCX and UTF-8 TXT files, with downloadable text export.
- **Data Studio:** CSV/XLSX inspection, validation, cleanup, column transformations and exports.
- **Automation Studio:** deterministic text workflows with previews, approval checkpoints, execution logs and JSON export.
- **Development Studio:** generate a responsive static business website starter as a ZIP containing HTML, CSS and setup notes.

## The five studios

| Studio | Capabilities |
|---|---|
| Research | Source-note briefs, linked references and Markdown reports |
| Documents | PDF/DOCX/TXT text extraction, metadata and text export |
| Data | CSV/XLSX cleanup, validation, transformations and exports |
| Automation | Allowlisted text workflows, previews, approval checkpoints and logs |
| Development | Static business website starter generation and downloadable ZIP |

## Technology

- Python / FastAPI — backend and processing services
- JavaScript — browser interface and studio workflows
- openpyxl, pypdf, python-docx — spreadsheet and document processing
- Python standard library — ZIP generation and deterministic workflow utilities
- Optional future integrations — n8n, Supabase and AI model providers

All five studios have a functional first version. Core workflows are local-first and do not require paid APIs or hosted services.

## Run locally

Requires Python 3.10 or newer.

    python -m venv .venv
    .venv\Scripts\Activate.ps1
    python -m pip install -r backend/requirements.txt
    uvicorn app.main:app --reload --app-dir backend

Open http://127.0.0.1:8000. Interactive API documentation is at http://127.0.0.1:8000/docs.

### API endpoints

- GET /api/health — service health
- GET /api/version — application version
- POST /api/research/report — create a source-linked brief
- POST /api/documents/extract — extract text and metadata from PDF, DOCX or TXT
- POST /api/data/inspect — inspect an uploaded CSV/XLSX file
- POST /api/data/clean — clean and export an uploaded CSV/XLSX file
- POST /api/data/transform — rename, normalize, select/reorder columns and clean before export
- POST /api/automation/run — preview or execute an allowlisted text workflow
- POST /api/development/generate — generate a static business website ZIP

### Safeguards and limitations

- Document uploads: 10 MB maximum; PDF limited to 100 pages; DOCX archive expansion limited to 25 MB; extracted output limited to 100,000 characters.
- Research Studio organizes supplied notes only; it does not automatically browse or verify sources.
- Automation Studio accepts only built-in text actions; arbitrary code, shell commands, outbound requests and persistence are not supported.
- Development Studio generates a static one-page starter. Custom backend features, hosting setup and advanced design still require project-specific work.
- Uploaded files and workflow inputs are processed in memory and are not persisted.

### Run tests

    pytest

## Repository layout

- backend/ — FastAPI routes, processing services and tests
- frontend/ — static JavaScript interface, studio modules and styles
- docs/ — architecture and project documentation
- examples/ — synthetic demonstration material
- .github/ — CI workflows
- ROADMAP.md — planned implementation phases
- CHANGELOG.md — verified project changes

## Principles

1. Start with the client's actual task and required deliverable.
2. Use AI only when it improves the result.
3. Validate inputs and outputs; preserve human oversight.
4. Protect private files, customer data and credentials.
5. Keep modules reusable, testable and independently understandable.
6. Prefer complete, reliable demonstrations over unfinished feature counts.

Never commit API keys, credentials, private client documents or real customer data. Use synthetic or explicitly authorized sample data.

## License

MIT. See LICENSE.
