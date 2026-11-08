# Changelog

Only implemented and verified changes belong in this file.

## [Unreleased]

### Added
- Research Studio source-note briefs with linked references, key points, limitations and Markdown export.
- Document Studio in-memory extraction for PDF, DOCX and UTF-8 TXT, including available metadata and downloadable text output.
- Document upload safeguards: 10 MB input limit, 100-page PDF limit, 25 MB DOCX expansion limit and 100,000-character output limit.
- Automated document service and API tests.
- Data Studio CSV/XLSX inspection, validation, cleanup, column transformations and exports.
- FastAPI application, lightweight frontend, health/version endpoints and GitHub Actions CI.

### Changed
- Updated README, roadmap and workspace interface to reflect implemented Research, Document and Data workflows.

### Limitations
- Research Studio organizes supplied notes only; it does not automatically browse or verify sources.
- Document Studio extracts text only; it does not yet convert file formats or edit source documents.
- Automation and Development Studios remain planned modules.
