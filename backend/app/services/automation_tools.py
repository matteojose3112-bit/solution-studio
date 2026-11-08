"""Small allowlisted workflow runner with an explicit approval checkpoint."""
import re

ALLOWED_STEPS = {
    "trim_whitespace",
    "collapse_whitespace",
    "extract_emails",
    "mask_emails",
    "uppercase",
    "lowercase",
    "count_words",
}
EMAIL_PATTERN = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")


class WorkflowInputError(ValueError):
    """Raised when a workflow definition is invalid."""


def run_workflow(input_text: str, steps: list[str]) -> dict:
    if not input_text.strip():
        raise WorkflowInputError("Enter some text to process.")
    if len(input_text) > 20_000:
        raise WorkflowInputError("Input exceeds the 20,000-character limit.")
    if not 1 <= len(steps) <= 8:
        raise WorkflowInputError("Choose between 1 and 8 workflow steps.")
    unknown = [step for step in steps if step not in ALLOWED_STEPS]
    if unknown:
        raise WorkflowInputError(f"Unsupported workflow step: {unknown[0]}.")

    output = input_text
    log = []
    for index, step in enumerate(steps, start=1):
        if step == "trim_whitespace":
            output = output.strip()
            message = "Removed leading and trailing whitespace."
        elif step == "collapse_whitespace":
            output = re.sub(r"\s+", " ", output).strip()
            message = "Collapsed repeated whitespace into single spaces."
        elif step == "extract_emails":
            found = list(dict.fromkeys(EMAIL_PATTERN.findall(output)))
            output = "\n".join(found)
            message = f"Extracted {len(found)} unique email address(es)."
        elif step == "mask_emails":
            output, count = EMAIL_PATTERN.subn("[REDACTED]", output)
            message = f"Masked {count} email address(es)."
        elif step == "uppercase":
            output = output.upper()
            message = "Converted text to uppercase."
        elif step == "lowercase":
            output = output.lower()
            message = "Converted text to lowercase."
        else:
            count = len(output.split())
            output = f"Word count: {count}"
            message = f"Counted {count} word(s)."
        log.append({"step": index, "action": step, "status": "completed", "message": message})

    return {"output": output, "log": log}
