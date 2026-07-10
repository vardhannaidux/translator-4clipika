# Troubleshooting & Diagnostic Guide

This guide helps resolve common rendering, configuration, and runtime errors in the **Eenadu 4C Lipika Translator**.

---

## 1. Font and Visual Formatting Mismatches

### Problem: Output text looks like garbage CP1252 symbols (e.g., "ë¯yô¢í£²è…")
- **Cause**: This is normal. The 4C Lipika system relies on CP1252 characters to represent Telugu shapes visually.
- **Fix**: Install the `4CEENADU_0.TTF` font provided in the repository on your system. In your publishing program (InDesign, PageMaker, Illustrator), select the pasted text and change its font to **4C Eenadu** (or **4C Lipika**). The garbage characters will transform into standard Telugu script.

---

## 2. Text Normalization and Mappings

### Problem: Translation fails with "Translation engine processing failed"
- **Cause**: The input text may contain non-standard or corrupt Unicode glyph sequences that cannot be parsed by the syllable segmenter.
- **Fix**: Check the application log files in `logs/translator.log`. Ensure the text uses standard Telugu Unicode block codes (`0x0C00` - `0x0C7F`). 

---

## 3. Logs and Diagnostic Analysis

All error traces and operational logs are written to:
- `logs/translator.log`

### Config Level Setting
To enable verbose debugging:
1. Open [sandbox/config.json](file:///e:/translator/translator/sandbox/config.json)
2. Modify the `"log_level"` setting to `"DEBUG"`:
   ```json
   "log_level": "DEBUG"
   ```
3. Restart the application and view logging traces inside the log file.
