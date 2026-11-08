# Architecture

## Overview

Solution Studio is a modular toolkit for delivering practical digital work. It is not intended to force every task into one monolithic application. Each capability should be independently testable and reusable.

## High-level design

```text
User
  |
  v
JavaScript web interface
  |
  v
Python API (FastAPI)
  |
  +--> Research services
  +--> Document processing
  +--> Data processing and analysis
  +--> Workflow and integration adapters
  +--> Custom tool demonstrations
  |
  +--> Local storage (initially SQLite / filesystem)
  |
  +--> Optional external services
         - AI model providers
         - n8n workflows
         - Supabase
         - Third-party APIs
```

## Language responsibilities

- **Python:** primary application and processing language; API, document handling, data operations, AI orchestration and integrations.
- **JavaScript:** browser interface and selected Node.js integrations.
- **SQL:** persistence, querying and data transformation.

TypeScript is intentionally not a primary requirement for this repository because the existing portfolio already contains several TypeScript projects.

## Module boundaries

### Research
Coordinates research inputs, source references, extraction and report generation. AI-generated claims must be distinguishable from verified source material.

### Documents
Handles file validation, metadata, text extraction, transformation and export. Uploaded files are untrusted input.

### Data
Provides deterministic inspection, cleaning, validation, transformation and analysis for structured files.

### Automation
Connects well-defined steps through APIs, webhooks or optional n8n workflows. Actions with external consequences should support approval and clear execution logs.

### Development
Contains reusable patterns and examples for small custom applications. It is a showcase of delivery capability, not an unrestricted code-generation environment.

## Reliability and safety principles

- Validate file type, size and content before processing.
- Keep secrets in environment variables; provide an example environment file without real credentials.
- Do not commit customer data or private documents.
- Use deterministic processing for tasks that do not require AI.
- Validate AI outputs against explicit schemas where possible.
- Preserve source references for research outputs.
- Add human review for sensitive, uncertain or externally consequential actions.
- Log operational events without unnecessarily logging personal or confidential content.
- Keep external providers optional and isolate them behind adapters.

## Initial implementation choices

The first implementation should favor local development and low operational cost:
- FastAPI for the Python API.
- A lightweight JavaScript frontend.
- SQLite for local persistence if persistence is needed.
- Local filesystem storage for development examples.
- Automated tests and GitHub Actions before adding deployment complexity.

These are initial choices, not permanent constraints. Revisit them when a concrete feature justifies a change.
