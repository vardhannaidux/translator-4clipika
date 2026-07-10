# -*- coding: utf-8 -*-
"""
config.py — Backend Configuration settings and rate limiting parameters.
"""

# CORS Settings
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "*", # Allow all for Render/Railway dynamic hostnames
]

# File constraints
MAX_FILE_SIZE = 5 * 1024 * 1024 # 5 Megabytes
ALLOWED_EXTENSIONS = {".txt", ".docx"}
ALLOWED_MIME_TYPES = {
    "text/plain",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
}

# Rate Limiting Settings (Requests per client IP)
RATE_LIMIT_REQUESTS = 60 # max requests
RATE_LIMIT_WINDOW = 60   # window in seconds (1 minute)
