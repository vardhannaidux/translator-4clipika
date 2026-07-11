# Eenadu 4C Lipika Web Translator

[![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.11%20%7C%203.14-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/fastapi-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com)
[![License](https://img.shields.io/badge/license-MIT-red.svg)](LICENSE)

A high-fidelity, production-grade web application and REST API suite designed to convert modern **Telugu Unicode** text to and from legacy **Eenadu 4C Lipika** font encoding (CP1252/CP1251 based visual byte sequences).

Developed by: **Vardhan Naidu**

---

## Overview

Historically, major Telugu newsrooms like *Eenadu* used proprietary page-layout applications (e.g., Adobe PageMaker, InDesign) utilizing legacy font systems like **4C Lipika** to publish newspapers. Since 4C Lipika uses a visual character mapping system overlaying the standard CP1252/CP1251 Windows encoding, these files are unreadable as logical Telugu text and cannot be searched, indexed, or easily digitized.

This **Web Application** makes this translator publicly available to anyone with a web browser. It features:
1. **FastAPI Backend**: A performant API service handling text translations and batch file conversions.
2. **Premium Glassmorphic Frontend**: A fully responsive web interface with dark/light modes, drag-and-drop file uploads, copy tools, live character stats, and toast notifications.

---

## Features

### Web Interface & UX
- **Responsive Theme Modes**: Supports both a Catppuccin Mocha-inspired dark mode and a clean, high-contrast light mode.
- **Bi-directional Translation**: Toggles between Unicode-to-Legacy and Legacy-to-Unicode conversion modes.
- **Text Area Translators**: Paste, translate, copy output, clear fields, and view real-time statistics (characters, words, translation speeds).
- **Document Drag-and-Drop**: Upload `.txt` and `.docx` files, translate them dynamically preserving typography/formatting runs, and download the output immediately.
- **Micro-interactions**: Subtle loading animations, progress indicators, and custom success/error toast alerts.

### Backend & API
- **FastAPI Core**: Lightweight, asynchronous web framework generating automatic OpenAPI/Swagger interfaces at `/docs`.
- **Sliding-Window Rate Limiting**: Security middleware that guards endpoints against overloading, tracking clients by IP.
- **Word Document (.docx) Translation Services**: Parses paragraphs, tables, and runs, converting Telugu text layout layers while preserving fonts and styling.
- **Production Packaging**: Docker and docker-compose configurations, Render blueprint manifests, Heroku Procfiles, and GitHub CI actions.

---

## Project Structure

```text
translator/
├── backend/
│   ├── main.py                     # FastAPI application entrypoint (REST endpoints)
│   ├── services.py                 # File & text translation service engines (.docx, .txt)
│   ├── schemas.py                  # Pydantic validation schemas
│   ├── config.py                   # Central settings (CORS, Rate limits, limits)
│   └── tests/                      # API endpoint unit tests
├── frontend/
│   ├── index.html                  # Main responsive Single-Page UI
│   ├── style.css                   # Premium CSS styles (Glassmorphism, Catppuccin Mocha)
│   └── script.js                   # JavaScript actions, AJAX progress bars, theme toggle
├── docs/                           # System documentation guides
│   ├── architecture.md             # Desktop architecture overview
│   ├── web_api.md                  # Web REST API schemas & payload details
│   └── deployment.md               # Render, Railway and Docker instructions
├── requirements.txt                # Python backend package dependencies
├── Dockerfile                      # Production Docker builder and runner
├── docker-compose.yml              # Local container orchestrator
├── render.yaml                     # Render Blueprint deploy manifest
├── Procfile                        # Heroku/Render process script
├── runtime.txt                     # Specify python runner version
├── .gitignore                      # Git ignore parameters
├── LICENSE                         # MIT License
├── CHANGELOG.md                    # Changelog updates
├── CONTRIBUTING.md                 # Open-source contributing manual
├── SECURITY.md                     # Security report guidelines
└── .github/
    └── workflows/
        └── ci.yml                  # GitHub Actions continuous integration workflow
```

---

## Installation & Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/translator.git
   cd translator
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the backend server**:
   ```bash
   uvicorn backend.main:app --reload
   ```
   Open `http://127.0.0.1:8000` in your web browser.

---

## Container Deployment (Docker)

To run the application locally inside Docker:

```bash
# Build & start container services
docker-compose up --build
```
Access the translator web page at `http://localhost:8000`.

---

## Web API Reference

The FastAPI service exposes an interactive Swagger documentation page at:
- **Interactive docs**: `http://localhost:8000/docs`

For details on JSON payloads and multipart upload formats, see [docs/web_api.md](docs/web_api.md).

---

## Deployment to the Cloud

For instructions on deploying the application to **Render** or **Railway**, see [docs/deployment.md](docs/deployment.md).

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
