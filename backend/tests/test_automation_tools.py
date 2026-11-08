import pytest

from app.services.automation_tools import WorkflowInputError, run_workflow


def test_runs_multiple_steps_in_order():
    result = run_workflow("  Contact  TEAM@example.com  ", ["trim_whitespace", "lowercase", "extract_emails"])
    assert result["output"] == "team@example.com"
    assert len(result["log"]) == 3
    assert all(item["status"] == "completed" for item in result["log"])


def test_masks_emails_and_counts_words():
    result = run_workflow("Email me at person@example.com today", ["mask_emails", "count_words"])
    assert result["output"] == "Word count: 5"


@pytest.mark.parametrize("text,steps", [
    ("", ["trim_whitespace"]),
    ("valid text", []),
    ("valid text", ["unknown_step"]),
])
def test_rejects_invalid_workflows(text, steps):
    with pytest.raises(WorkflowInputError):
        run_workflow(text, steps)
