# Roadmap

Items are marked complete only after implementation. Planned studio cards in the interface are not functional modules.

## Phase 0 — Repository foundation
- [x] Establish public repository and license
- [x] Define project purpose and modular scope
- [x] Document initial architecture and delivery principles
- [x] Add development environment and local run instructions
- [x] Add baseline CI and test configuration

## Phase 1 — Core application foundation
- [x] Create Python backend using FastAPI
- [x] Add health and version endpoints
- [x] Establish initial application configuration
- [x] Create lightweight JavaScript frontend
- [x] Connect frontend to backend
- [x] Serve frontend and API from one local server
- [x] Add initial automated tests

## Phase 2 — Document and data tools
- [x] Build initial CSV upload and file-validation utilities (CSV and XLSX, 5 MB limit)
- [ ] Add document metadata and text extraction
- [x] Add CSV inspection, preview and column statistics
- [x] Add CSV cleanup: trim whitespace, remove blank rows and duplicate rows
- [x] Support cleaned CSV downloads
- [x] Add synthetic CSV tests
- [x] Add initial XLSX inspection, cleanup and export support\n- [ ] Add richer data validation, type inference and analysis

## Phase 3 — Research tools
- [ ] Create source-aware research workflow
- [ ] Generate structured summaries and reports
- [ ] Track source references and uncertainty
- [ ] Add optional AI provider adapter
- [ ] Require review for unverified or consequential output

## Phase 4 — Workflow automation
- [ ] Define reusable workflow patterns
- [ ] Add webhook and API integration examples
- [ ] Demonstrate approval and notification steps
- [ ] Document optional n8n integration
- [ ] Add retries, logging and failure handling

## Phase 5 — Custom development demonstrations
- [ ] Add reusable patterns for small business tools
- [ ] Publish at least two working example applications
- [ ] Document customization and handoff process

## Phase 6 — Portfolio readiness
- [ ] Complete automated tests and CI for all modules
- [ ] Review security, privacy and dependency risks
- [ ] Add screenshots and demonstration data
- [ ] Publish setup and user documentation
- [ ] Record known limitations and deployment options

## Scope rule

Prioritize a small number of complete, reliable demonstrations over a large collection of unfinished features. Paid APIs and hosted services should remain optional where practical.
