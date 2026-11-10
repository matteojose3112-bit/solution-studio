# Changelog

Only implemented changes and verified deployment facts are recorded here.

## [Unreleased]

### Release
- Published [Solution Studio v0.1.0 — Initial Public Demo](https://github.com/matteojose3112-bit/solution-studio/releases/tag/v0.1.0) as a GitHub pre-release targeting `main`.
- Added Solution Studio to the Aster portfolio's six-project collection with a verified project card and dedicated case study.
- Release notes describe all five studios, the public Render demo, prior passing backend/CI checks, successful live smoke-tested workflows, and the outstanding Data/Document browser file-picker QA. This is explicitly a pre-release, not stable v1.0.

### Verification update — 2026-11-10
- Re-ran the public production smoke test: Render homepage loaded, API-connected indicator was visible, all five studios rendered and no visible application errors appeared.
- Passed live Research report generation and Markdown download-control check.
- Passed live Automation preview, approval and execution; output and workflow JSON controls were present.
- Passed live Development website ZIP generation using synthetic business details.
- Inspected Data and Documents upload controls and limits. Actual browser file-picker uploads were not attempted because this browser automation environment cannot attach local fixtures; API-level CSV and TXT upload coverage remains covered by the existing passing backend tests.
- Confirmed the latest documentation deployment is live on Render. The most recent available backend CI evidence remains the previously recorded passing 58-test suite and JavaScript syntax check; no new CI run was returned for the documentation-only head commit.

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
- The integrated backend test suite passed 58 tests, including API-level CSV upload/inspection/cleanup/export and TXT upload/extraction coverage.
- GitHub Actions CI passed for the latest documentation updates; the workflow runs the backend test suite and frontend JavaScript syntax checks.
- Public homepage and health endpoint smoke checks passed.
- Live browser regression checks passed for Research report generation/Markdown export, Automation preview/approval/execution and output controls, and Development website ZIP generation.
- The live header now correctly reports “API connected”; all five studio sections and the Automation approval guidance were verified after deployment.
- Data and Documents API-level upload/processing behavior is covered by passing automated tests. Live browser file-picker upload/download checks remain pending because the browser automation session cannot attach downloaded local files to file inputs; synthetic CSV and TXT fixtures are available in `examples/`.
- Updated the README and roadmap to separate verified API coverage, successful live browser checks and the remaining manual file-picker QA.

### Known limitations
- Research Studio organizes supplied notes only; automatic web research and independent source verification are not implemented.
- Document Studio extracts text and metadata only; conversion and editing are not implemented.
- Automation Studio runs local allowlisted text actions only; external integrations, persistence and scheduling are not implemented.
- Development Studio generates a static one-page starter; custom backend development and hosting are outside its current scope.
- Uploaded files and workflow inputs are processed in memory and are not persisted.
