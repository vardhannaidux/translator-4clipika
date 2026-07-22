# -*- coding: utf-8 -*-
"""
main.py — FastAPI Application Entrypoint.
Exposes REST APIs, implements rate limiting, handles file uploads/downloads,
and serves the static web UI.
"""

import sys
import os
import time
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request, Depends, Header
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError
from io import BytesIO

# Ensure parent directory is in search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.schemas import TranslationRequest, TranslationResponse, TranslationStats
from backend.services import process_text_translation, translate_txt_file, translate_docx_file
from backend.config import (
    ALLOWED_ORIGINS, MAX_FILE_SIZE, ALLOWED_EXTENSIONS,
    ALLOWED_MIME_TYPES, RATE_LIMIT_REQUESTS, RATE_LIMIT_WINDOW
)
from config import setup_logger

logger = setup_logger("backend_main")

# Auth token — set API_AUTH_TOKEN env var in Render dashboard
API_AUTH_TOKEN = os.environ.get("API_AUTH_TOKEN", "eenadu_1976")

app = FastAPI(
    title="Eenadu 4C Lipika Translator API",
    description="REST API suite for bi-directional Telugu Unicode and 4C Lipika conversion.",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# InMemory Rate Limiter Implementation
class InMemoryRateLimiter:
    def __init__(self, requests: int, window: int) -> None:
        self.requests = requests
        self.window = window
        self.clients = {} # ip -> list of timestamps
        
    def check_rate_limit(self, ip: str) -> None:
        now = time.time()
        if ip not in self.clients:
            self.clients[ip] = [now]
            return
            
        # Retain timestamps only within the current sliding window
        self.clients[ip] = [t for t in self.clients[ip] if now - t < self.window]
        
        if len(self.clients[ip]) >= self.requests:
            logger.warning(f"Rate limit triggered for client IP: {ip}")
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please wait a minute before trying again."
            )
            
        self.clients[ip].append(now)

rate_limiter = InMemoryRateLimiter(RATE_LIMIT_REQUESTS, RATE_LIMIT_WINDOW)

def get_client_ip(request: Request) -> str:
    """Helper to extract IP address from headers (handling Render proxies)."""
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"

def rate_limit_dependency(request: Request) -> None:
    ip = get_client_ip(request)
    rate_limiter.check_rate_limit(ip)


def auth_dependency(x_auth_token: Optional[str] = Header(None)) -> None:
    if x_auth_token != API_AUTH_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized. Please log in with correct credentials."
        )


# --- API ROUTES ---

@app.get("/api/health", tags=["System"])
def health_check():
    """Returns application health status."""
    return {"status": "ok", "timestamp": time.time()}


@app.post(
    "/api/translate/text",
    response_model=TranslationResponse,
    dependencies=[Depends(rate_limit_dependency), Depends(auth_dependency)],
    tags=["Translation"]
)
async def translate_text_endpoint(req: TranslationRequest):
    """
    Translates a plain text block.
    Supports bi-directional mapping (Unicode-to-Legacy and Legacy-to-Unicode).
    """
    try:
        translated, elapsed_ms = process_text_translation(
            req.text, req.direction, req.editorial_mode
        )
        
        # Calculate statistics
        words = len(req.text.split())
        stats = TranslationStats(
            chars=len(req.text),
            words=words,
            time_ms=elapsed_ms
        )
        
        return TranslationResponse(translated_text=translated, stats=stats)
    except Exception as e:
        logger.error(f"Text translation API error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal translation error: {str(e)}")


@app.post(
    "/api/translate/file",
    dependencies=[Depends(rate_limit_dependency), Depends(auth_dependency)],
    tags=["Translation"]
)
async def translate_file_endpoint(
    file: UploadFile = File(...),
    direction: str = Form("unicode_to_legacy"),
    editorial_mode: bool = Form(False)
):
    """
    Uploads a file (.txt or .docx) and returns the translated version as a download.
    """
    # 1. Validate file constraints
    filename = file.filename or "file"
    _, ext = os.path.splitext(filename.lower())
    
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file extension '{ext}'. Only .txt and .docx files are permitted."
        )
        
    # Read file stream
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File exceeds the maximum size limit of {MAX_FILE_SIZE / (1024*1024):.1f} MB."
        )
        
    try:
        if ext == ".txt":
            result_bytes = translate_txt_file(content, direction, editorial_mode)
            media_type = "text/plain"
            out_filename = f"translated_{filename}"
        elif ext == ".docx":
            # Translate Word document
            result_bytes = translate_docx_file(content, direction, editorial_mode)
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            out_filename = f"translated_{filename}"
        else:
            raise HTTPException(status_code=400, detail="Invalid file type.")
            
        logger.info(f"Successfully processed file translation for: {filename}")
        
        return StreamingResponse(
            BytesIO(result_bytes),
            media_type=media_type,
            headers={
                "Content-Disposition": f"attachment; filename={out_filename}",
                "Access-Control-Expose-Headers": "Content-Disposition"
            }
        )
    except Exception as e:
        logger.error(f"File translation API error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to translate file '{filename}'. Error: {str(e)}"
        )


# Serve frontend static assets
# Check if frontend folder exists first
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
else:
    logger.warning("Frontend static directory not found. Static file server skipped.")
