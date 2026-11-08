# Backend

Python API built with [FastAPI](https://fastapi.tiangolo.com/). The application serves the static frontend from the same origin.

## Run

From the repository root:

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

Install dependencies and launch:

```bash
python -m pip install -r backend/requirements.txt
uvicorn app.main:app --reload --app-dir backend
```

## Routes

- `GET /api/health`
- `GET /api/version`
- `GET /docs` — interactive API documentation

## Tests

Run `pytest` from the repository root. The suite covers the system endpoints and frontend entry point.
