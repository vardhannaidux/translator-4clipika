# User Guide & Manual

This guide describes how to run, configure, and use the **Eenadu 4C Lipika Translator**.

---

## 1. Graphical User Interface (GUI)

### Launching the Application
Run the main script to start the desktop window:
```bash
python app.py
```

### Visual Layout
- **Telugu Unicode Input**: Paste or type standard Unicode Telugu script into the top text box.
- **Translation Settings**: 
  - **Editorial Archive Mode**: Toggle optional transition corrections (e.g. spelling normalization) on or off.
- **Actions**:
  - Click **Translate Text** or press `Ctrl + Return` to run the translation.
  - Click **Copy to Clipboard** or press `Ctrl + C` (while output box is selected) to copy.
- **Output Box**: Displays the CP1252 character preview that represents the legacy 4C Lipika font bytes. Copy-paste this text directly into PageMaker or InDesign.
- **Status Footer**: Shows operation outcomes, text metrics, and processing speeds in milliseconds.

### Keyboard Shortcuts
- `Ctrl + Return` / `Ctrl + T`: Translates the current input.
- `Ctrl + C`: Copies output to the clipboard (when focus is in the output text frame).
- `Tab` / `Shift + Tab`: Moves focus indicator between controls.

---

## 2. Command Line Interface (CLI)

The CLI supports direct conversions, stream redirections, and output file writes.

### Translate direct text input
```bash
python translation_engine.py "తెలుగు టెక్స్ట్"
```

### Convert file to output
```bash
python translation_engine.py -f input_unicode.txt -o output_legacy.txt
```

### Pipe stream input
```bash
cat input.txt | python translation_engine.py > output.txt
```

---

## 3. Configuration Settings

Configurations are saved automatically in [sandbox/config.json](file:///e:/translator/translator/sandbox/config.json). You can edit this file to customize:
- `window_geometry`: Preserves the dimensions and coordinates of the desktop window.
- `font_size`: Sets the font size of the text boxes.
- `font_family`: Changes the text interface font (defaults to `"Segoe UI"`).
- `log_level`: Sets logging logging thresholds (`"INFO"`, `"DEBUG"`, `"WARNING"`, `"ERROR"`).
- `autosave_enabled`: Toggles active crash recovery backups on/off.
