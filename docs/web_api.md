# Web API Documentation

This document describes the FastAPI REST API interface endpoints, validation rules, schemas, and rate limits.

---

## 1. Authentication & Rate Limiting

The API does not require user accounts. It uses a **sliding window rate limiter** mapped by the client IP address:
- Limit: **60 requests per minute**.
- If a client exceeds this limit, the server responds with a `429 Too Many Requests` HTTP error code.

---

## 2. API Endpoints

### Health Status
Check if the web service is up and running.

- **URL**: `/api/health`
- **Method**: `GET`
- **Response**: `200 OK`
  ```json
  {
    "status": "ok",
    "timestamp": 1783709090.23
  }
  ```

---

### Translate Text block
Translates text either from Telugu Unicode to legacy CP1252 visual bytes, or vice versa.

- **URL**: `/api/translate/text`
- **Method**: `POST`
- **Headers**: `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "text": "మండపేట",
    "direction": "unicode_to_legacy",
    "editorial_mode": false
  }
  ```
  - `direction`: Set to `"unicode_to_legacy"` or `"legacy_to_unicode"`.
  - `editorial_mode`: Set to `true` to enable transition corrections (applies only in forward mode).
- **Response**: `200 OK`
  ```json
  {
    "translated_text": "మండపేట visual CP1252 string representation",
    "stats": {
      "chars": 6,
      "words": 1,
      "time_ms": 1.45
    }
  }
  ```
- **Error Codes**:
  - `422 Unprocessable Entity`: Input string is empty or parameters are invalid.
  - `429 Too Many Requests`: Rate limit reached.
  - `500 Internal Server Error`: Engine processing failure.

---

### Translate Document File
Uploads a document file (`.txt` or `.docx`), translates it, and returns the converted file directly as a download.

- **URL**: `/api/translate/file`
- **Method**: `POST`
- **Headers**: `Content-Type: multipart/form-data`
- **Payload Parameters**:
  - `file`: Binary file upload (`.txt` or `.docx`). Max size: **5 MB**.
  - `direction`: Form string `"unicode_to_legacy"` or `"legacy_to_unicode"`.
  - `editorial_mode`: Form boolean `true` or `false` (default: `false`).
- **Response**: `200 OK`
  - Returns a binary stream download of the translated document.
  - Header `Content-Disposition: attachment; filename=translated_[original_filename].[ext]`.
- **Error Codes**:
  - `400 Bad Request`: Mime-type mismatch, invalid extension, or file exceeds 5MB size limit.
  - `429 Too Many Requests`: Rate limit reached.
  - `500 Internal Server Error`: Conversion process failure.
