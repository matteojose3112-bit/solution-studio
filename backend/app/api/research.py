"""Source-aware research report endpoint."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.research_tools import ResearchInputError, build_research_report

router = APIRouter(prefix="/research", tags=["research"])


class ResearchSource(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    url: str = Field(min_length=1, max_length=2000)
    notes: str = Field(min_length=1, max_length=4000)


class ResearchRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)
    sources: list[ResearchSource] = Field(min_length=1, max_length=8)


@router.post("/report")
def create_research_report(payload: ResearchRequest) -> dict:
    try:
        return build_research_report(
            payload.question,
            [source.model_dump() for source in payload.sources],
        )
    except ResearchInputError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
