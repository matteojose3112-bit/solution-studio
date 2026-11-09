# Changelog

Only implemented changes and verified deployment facts are recorded here.

## [Unreleased]

### Added
- Five functional first-version studios: Research, Documents, Data, Automation and Development.
- Research briefs from up to eight user-provided source notes, with key points, linked references, limitations and Markdown export.
- In-memory PDF, DOCX and UTF-8 TXT text/metadata extraction with downloadable text output.
- CSV/XLSX inspection, validation, cleanup, column transformations and export.
- Allowlisted deterministic text workflows with preview, approval checkpoint, execution logs, output download and JSON workflow export.
- Static responsive business website starter generation with validated inputs and ZIP packaging.
- Backend automated tests and frontend JavaScript syntax checks in CI.

### Changed
- Updated project documentation to describe implemented functionality, setup, API routes, safeguards and remaining work.
- Hardened spreadsheet processing with archive-expansion limits and regression coverage.
- Integrated all five studio modules into the main application.

### Deployment
- Published the application as a public Render web service: https://solution-studio-secb.onrender.com
- Verified that the public homepage loads and `/api/health` returns `{"status":"ok","service":"solution-studio"}`.
- Render free-tier instances may sleep after inactivity, which can increase first-request latency.

### Verification
- The integrated backend test suite passed 58 tests.
- Frontend JavaScript syntax checks are included in CI.
- Public homepage and health endpoint smoke checks passed.
- Live browser regression checks passed for Research report generation/Markdown export, Automation preview/approval/execution and output controls, and Development website ZIP generation.
- The live header now correctly reports “API connected”; all five studio sections and the Automation approval guidance were verified after deployment.
- Data and Documents file-upload/extraction/download flows still require manual file-picker verification; synthetic CSV and TXT fixtures are available in `examples/`.

### Known limitations
- Research Studio organizes supplied notes only; automatic web research and independent source verification are not implemented.
- Document Studio extracts text and metadata only; conversion and editing are not implemented.
- Automation Studio runs local allowlisted text actions only; external integrations, persistence and scheduling are not implemented.
- Development Studio generates a static one-page starter; custom backend development and hosting are outside its current scope.
- Uploaded files and workflow inputs are processed in memory and are not persisted.
