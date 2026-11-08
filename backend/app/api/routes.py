"""Small system endpoints used by the interface and deployment checks."""

from fastapi import APIRouter

router = APIRouter(tags=["system"])


@router.get("/health")
def health() -> dict[str, str]:
    """Return a lightweight liveness response."""
    return {"status": "ok", "service": "solution-studio"}


@router.get("/version")
def version() -> dict[str, str]:
    """Expose the current application version."""
    return {"version": "0.1.0"}
