# Changelog

All notable project changes are recorded here. Only implemented and verified changes belong in this file.

## [Unreleased]

### Added
- Data Studio supports CSV and XLSX upload, inspection, column statistics, inferred column types, missing/inconsistent-value warnings, preview, cleanup, explicit column renaming, snake_case header normalization, column selection/reordering and cleaned/transformed-file downloads. XLSX processing uses the first worksheet and cached formula values; formulas are not evaluated.
- CSV/XLSX safeguards: 5 MB limit, row and column caps and unique header normalization; CSV includes UTF-8 and malformed-row validation, plus spreadsheet-formula neutralization on CSV export.
- Automated tests for CSV and XLSX parsing, cleanup, upload endpoints, transformation validation and workbook exports.
- FastAPI application with health and version endpoints.
- JavaScript landing interface introducing the five planned studios.
- Same-origin static frontend hosting through FastAPI.
- Initial backend tests for API routes and frontend delivery.
- GitHub Actions workflow to install dependencies and run tests.
- Local setup and run instructions.

### Changed
- Updated README and workspace guides to reflect the runnable foundation.
- Marked repository and core application foundation tasks complete in the roadmap.

### Notes
- Research, document, data, automation and development modules remain planned work.
