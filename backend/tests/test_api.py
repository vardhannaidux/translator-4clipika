# -*- coding: utf-8 -*-
"""
test_api.py — FastAPI endpoint verification suite.
Tests API status, text translation, file conversions, and error handling.
"""

import sys
import os
import pytest
from fastapi.testclient import TestClient

# Ensure parent directory is in search path to import backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from backend.main import app

client = TestClient(app)

def test_health_check():
    """Verify that the health status API returns OK."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_unauthorized_access():
    """Verify that calling translation endpoints without the correct auth token returns 401."""
    payload = {
        "text": "మండపేట",
        "direction": "unicode_to_legacy"
    }
    response = client.post("/api/translate/text", json=payload)
    assert response.status_code == 401
    
    response = client.post("/api/translate/text", json=payload, headers={"X-Auth-Token": "invalid"})
    assert response.status_code == 401

def test_text_translate_unicode_to_legacy():
    """Test text translation from Unicode to 4C Lipika visual bytes."""
    payload = {
        "text": "మండపేట",
        "direction": "unicode_to_legacy",
        "editorial_mode": False
    }
    response = client.post("/api/translate/text", json=payload, headers={"X-Auth-Token": "eenadu_1976"})
    assert response.status_code == 200
    data = response.json()
    assert "translated_text" in data
    assert data["stats"]["chars"] == 6

def test_text_translate_legacy_to_unicode():
    """Test reverse transdecoding from legacy visual bytes to Unicode."""
    payload = {
        "text": "Oª",
        "direction": "legacy_to_unicode",
        "editorial_mode": False
    }
    response = client.post("/api/translate/text", json=payload, headers={"X-Auth-Token": "eenadu_1976"})
    assert response.status_code == 200
    data = response.json()
    assert "translated_text" in data
    assert "మీ" in data["translated_text"]

def test_text_translate_invalid_payload():
    """Test API input validation on invalid parameters."""
    payload = {
        "text": "",
        "direction": "invalid_direction"
    }
    response = client.post("/api/translate/text", json=payload, headers={"X-Auth-Token": "eenadu_1976"})
    assert response.status_code == 422

def test_file_translate_txt():
    """Test file uploader API with a plain text file."""
    file_content = "మండపేట".encode("utf-8")
    files = {"file": ("test.txt", file_content, "text/plain")}
    data = {
        "direction": "unicode_to_legacy",
        "editorial_mode": "false"
    }
    response = client.post("/api/translate/file", files=files, data=data, headers={"X-Auth-Token": "eenadu_1976"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
    assert "attachment" in response.headers["content-disposition"]

def test_file_translate_invalid_extension():
    """Test file uploader handles unsupported extensions gracefully."""
    file_content = b"garbage data"
    files = {"file": ("test.jpg", file_content, "image/jpeg")}
    data = {"direction": "unicode_to_legacy"}
    response = client.post("/api/translate/file", files=files, data=data, headers={"X-Auth-Token": "eenadu_1976"})
    assert response.status_code == 400
    assert "Unsupported file extension" in response.json()["detail"]
