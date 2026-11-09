# Roadmap

Status reflects implemented work and checks completed to date. The 58-test backend suite and frontend JavaScript syntax checks pass in GitHub Actions. Browser-level QA is tracked separately from backend/CI verification.

## Phase 0 — Repository foundation
- [x] Establish public repository and license
- [x] Define project purpose, architecture and delivery principles
- [x] Add local setup instructions, CI and test configuration

## Phase 1 — Core application foundation
- [x] Create FastAPI backend and lightweight JavaScript frontend
- [x] Add health/version endpoints and same-origin hosting
- [x] Add automated backend tests and frontend JavaScript syntax checks

## Phase 2 — Data Studio
- [x] CSV/XLSX upload, validation, inspection and preview
- [x] Infer column types and report missing/inconsistent values
- [x] Clean whitespace, blank rows and duplicates
- [x] Rename, normalize, select and reorder columns
- [x] Export cleaned/transformed CSV and XLSX
- [x] Cover CSV upload, inspection, cleanup and export through API-level tests
- [ ] Complete live browser file-picker upload/download QA
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
- [x] Add downloadable text export and automated API tests for TXT extraction
- [ ] Complete live browser file-picker upload/download QA
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

## Phase 7 — Release and portfolio readiness
- [x] Integrate all five first-version studios on the main branch
- [x] Add backend automated tests and frontend JavaScript syntax checks to CI
- [x] Review security boundaries and address identified XLSX archive-expansion risk
- [x] Deploy the application to Render and verify the public homepage and health endpoint
- [ ] Complete browser file-picker upload/download QA for Data and Documents (their API upload/processing paths are covered by passing automated tests; Research, Automation and Development passed live browser checks)
- [x] Add synthetic CSV and TXT demonstration fixtures
- [x] Document setup, API endpoints, safeguards, test coverage and known limitations
- [ ] Add polished screenshots and client handoff examples
- [ ] Establish versioned releases and release notes

## Scope rule

Prioritize complete, reliable demonstrations over feature counts. Keep paid APIs and hosted services optional where practical. Do not mark browser workflows complete until they have been exercised end to end.
