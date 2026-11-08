# Roadmap

Items are marked complete only after implementation and automated verification.

## Phase 0 — Repository foundation
- [x] Establish public repository and license
- [x] Define project purpose, architecture and delivery principles
- [x] Add local setup instructions, CI and test configuration

## Phase 1 — Core application foundation
- [x] Create FastAPI backend and lightweight JavaScript frontend
- [x] Add health/version endpoints and same-origin hosting
- [x] Add automated tests

## Phase 2 — Data Studio
- [x] CSV/XLSX upload, validation, inspection and preview
- [x] Infer column types and report missing/inconsistent values
- [x] Clean whitespace, blank rows and duplicates
- [x] Rename, normalize, select and reorder columns
- [x] Export cleaned/transformed CSV and XLSX
- [ ] Add richer profiling, explicit type conversion and analysis

## Phase 3 — Research Studio
- [x] Build source-aware reports from user-supplied notes
- [x] Generate executive summaries, key points and linked references
- [x] Explain verification limits and uncertainty
- [x] Export reports as Markdown
- [ ] Add optional web research and AI-assisted synthesis adapters

## Phase 4 — Document Studio
- [x] Extract text and metadata from PDF, DOCX and TXT
- [x] Add upload size, PDF page, DOCX expansion and output-length limits
- [x] Add downloadable text export and automated tests
- [ ] Add PDF/DOCX conversion and structured transformations

## Phase 5 — Automation Studio
- [x] Define allowlisted workflow steps and ordered execution
- [x] Add preview, approval checkpoint and execution logs
- [x] Export workflow definitions and output
- [ ] Add optional webhook/API connectors and n8n integration
- [ ] Add persistent schedules, notifications and retry queues

## Phase 6 — Development Studio
- [x] Generate responsive static business website starters
- [x] Package HTML, CSS and setup notes as a downloadable ZIP
- [x] Validate inputs and escape user-supplied content
- [ ] Add reusable dashboard and internal-tool templates
- [ ] Document client customization and handoff

## Phase 7 — Portfolio readiness
- [x] Add CI syntax checks for every frontend JavaScript module
- [ ] Complete automated tests and CI for all modules
- [ ] Review security, privacy and dependency risks
- [ ] Add screenshots and synthetic demonstration data
- [ ] Perform end-to-end browser testing
- [ ] Publish setup, user documentation and deployment options
- [ ] Record known limitations and versioned releases

## Scope rule

Prioritize complete, reliable demonstrations over feature counts. Keep paid APIs and hosted services optional where practical.
