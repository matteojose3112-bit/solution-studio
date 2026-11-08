"""Allowlisted workflow preview and execution endpoints."""
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.automation_tools import WorkflowInputError, run_workflow

router = APIRouter(prefix="/automation", tags=["automation"])


class WorkflowRequest(BaseModel):
    input_text: str = Field(min_length=1, max_length=20_000)
    steps: list[Literal[
        "trim_whitespace",
        "collapse_whitespace",
        "extract_emails",
        "mask_emails",
        "uppercase",
        "lowercase",
        "count_words",
    ]] = Field(min_length=1, max_length=8)
    approval_required: bool = True
    approved: bool = False


@router.post("/run")
def execute_workflow(payload: WorkflowRequest) -> dict:
    try:
        result = run_workflow(payload.input_text, payload.steps)
    except WorkflowInputError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    if payload.approval_required and not payload.approved:
        return {
            "status": "awaiting_approval",
            "approval_required": True,
            "message": "Review the workflow output and approve before treating the run as complete.",
            **result,
        }

    return {
        "status": "completed",
        "approval_required": payload.approval_required,
        "message": "Workflow completed successfully.",
        **result,
    }
