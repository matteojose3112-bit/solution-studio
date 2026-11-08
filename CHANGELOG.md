# Changelog

Only implemented and verified changes belong in this file.

## [Unreleased]

### Added
- Research Studio source-note briefs with linked references, key points, limitations and Markdown export.
- Document Studio in-memory extraction for PDF, DOCX and UTF-8 TXT, including available metadata and downloadable text output.
- Data Studio CSV/XLSX inspection, validation, cleanup, column transformations and exports.
- Automation Studio allowlisted text workflows with ordered steps, preview, approval checkpoint, execution log, output download and JSON definition export.
- Automated backend service and API tests for the implemented studios.

### Changed
- Updated README, roadmap and workspace interface to reflect implemented Research, Document, Data and Automation workflows.

### Limitations
- Research Studio organizes supplied notes only; it does not automatically browse or verify sources.
- Document Studio extracts text only; it does not yet convert file formats or edit source documents.
- Automation Studio currently runs local deterministic text actions only; external integrations, schedules and notifications remain future work.
- Development Studio remains planned.
