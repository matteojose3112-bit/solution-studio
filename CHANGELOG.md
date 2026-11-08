# Changelog

Only implemented and verified changes belong in this file.

## [Unreleased]

### Added
- Research Studio API and browser workflow for source-linked research briefs based on user-provided source titles, URLs and notes.
- Structured executive summary, extracted key points, source references, limitations and Markdown report download.
- Research input validation for question/source limits, required notes, HTTP(S) links and duplicate URLs.
- Automated service and API tests for Research Studio.
- Data Studio CSV/XLSX inspection, validation, cleanup, column transformations and exports.
- FastAPI application, lightweight frontend, health/version endpoints and GitHub Actions CI.

### Changed
- Updated README, roadmap and workspace interface to reflect the implemented Research and Data workflows.

### Limitations
- Research Studio organizes supplied notes only. It does not automatically browse, scrape or verify linked pages.
- Document, Automation and Development Studios remain planned modules.
