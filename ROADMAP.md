# Roadmap

Items are marked complete only after implementation and automated verification. Planned cards are not functional modules.

## Phase 0 — Repository foundation
- [x] Establish public repository and license
- [x] Define project purpose and modular scope
- [x] Document architecture and delivery principles
- [x] Add local setup instructions
- [x] Add CI and test configuration

## Phase 1 — Core application foundation
- [x] Create FastAPI backend and lightweight JavaScript frontend
- [x] Add health/version endpoints and same-origin hosting
- [x] Add baseline automated tests

## Phase 2 — Data Studio
- [x] CSV/XLSX upload, validation, inspection and preview
- [x] Infer column types and report missing/inconsistent values
- [x] Clean whitespace, blank rows and duplicates
- [x] Rename, normalize, select and reorder columns
- [x] Export cleaned/transformed CSV and XLSX
- [ ] Add richer profiling, explicit type conversion and analysis

## Phase 3 — Research Studio
- [x] Build source-aware report workflow from user-supplied notes
- [x] Generate structured executive summaries and key points
- [x] Track source titles and linked references
- [x] Explain verification limits and uncertainty
- [x] Export reports as Markdown
- [ ] Add optional web research/source retrieval adapter
- [ ] Add optional AI-assisted synthesis adapter with human review

## Phase 4 — Document Studio
- [x] Extract text and metadata from PDF, DOCX and TXT
- [x] Add upload size, PDF page, DOCX expansion and output-length limits
- [x] Add downloadable text export
- [x] Add extraction and API tests
- [ ] Add PDF/DOCX conversion and structured document transformations

## Phase 5 — Automation Studio
- [ ] Define reusable workflow patterns
- [ ] Add webhook and API integration examples
- [ ] Demonstrate approval and notification steps
- [ ] Document optional n8n integration
- [ ] Add retries, logging and failure handling

## Phase 6 — Development Studio
- [ ] Add reusable patterns for small business tools
- [ ] Publish at least two working example applications
- [ ] Document customization and handoff process

## Phase 7 — Portfolio readiness
- [ ] Complete automated tests and CI for all modules
- [ ] Review security, privacy and dependency risks
- [ ] Add screenshots and synthetic demonstration data
- [ ] Publish setup, user documentation and known limitations
- [ ] Document deployment options

## Scope rule

Prioritize a small number of complete, reliable demonstrations over a large collection of unfinished features. Keep paid APIs and hosted services optional where practical.
