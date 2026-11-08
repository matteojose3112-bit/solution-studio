"""Static business microsite generator endpoint."""
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field

from app.services.site_builder import generate_site_package

router = APIRouter(prefix="/development", tags=["development"])


class SiteRequest(BaseModel):
    business_name: str = Field(min_length=1, max_length=100)
    tagline: str = Field(min_length=1, max_length=180)
    description: str = Field(min_length=1, max_length=800)
    services: list[str] = Field(min_length=1, max_length=6)
    contact_email: str = Field(default="", max_length=254)
    accent_color: str = Field(default="#7CE0B5", max_length=7)


@router.post("/generate")
def generate_website(payload: SiteRequest) -> Response:
    try:
        filename, archive = generate_site_package(payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return Response(
        content=archive,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
