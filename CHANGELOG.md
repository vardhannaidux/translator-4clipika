# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-07-10
### Added
- Transitioned project to a modern web application (FastAPI backend + responsive HTML/CSS/JS frontend).
- Built-in drag-and-drop file uploader supporting batch conversions of `.txt` and `.docx` documents.
- Continuous auto-save local backup recovery inside user settings.
- Centralized configuration manager (`config.json`) and thread-safe rotating logging handler.
- Added Light/Dark mode themes with visual transitions and customizable tooltips.
- Added GitHub actions workflow for automatic CI test execution.
- Multi-stage Dockerfile and Compose configurations.
- API validation schemas, rate limiting, and CORS headers.
