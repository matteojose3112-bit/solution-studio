# Frontend

A responsive, dependency-free JavaScript interface served by the FastAPI application.

The current landing workspace introduces the five planned studios and checks the backend health and version endpoints. The studio cards are roadmap descriptions, not functional tools yet.

The frontend is served at the root URL when the backend is running:

```bash
uvicorn app.main:app --reload --app-dir backend
```

Open http://127.0.0.1:8000.
