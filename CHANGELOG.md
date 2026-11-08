# Changelog

Only implemented and verified changes belong in this file.

## [Unreleased]

### Added
- Research Studio source-note briefs with linked references, key points, limitations and Markdown export.
- Document Studio in-memory extraction for PDF, DOCX and UTF-8 TXT, including metadata and downloadable text output.
- Data Studio CSV/XLSX inspection, validation, cleanup, column transformations and exports.
- Automation Studio allowlisted text workflows with ordered steps, preview, approval checkpoint, logs, output download and JSON export.
- Development Studio static business website generator with validated inputs, escaped content and ZIP export containing HTML, CSS and setup notes.
- Automated backend service and API tests for the implemented studios.

### Changed
- Updated README, roadmap and workspace interface to reflect all five functional first-version studios.

### Limitations
- Research Studio organizes supplied notes only; it does not automatically browse or verify sources.
- Document Studio extracts text only; it does not yet convert or edit source documents.
- Automation Studio runs local deterministic text actions only; external integrations and scheduling remain future work.
- Development Studio produces a static one-page starter, not a complete custom application or hosted website.
