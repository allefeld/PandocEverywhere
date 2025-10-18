# PandocEverywhere

A browser extension that enhances web-based text editors with powerful document conversion and external editing capabilities.

## Features

- **Format Conversion**: Convert between HTML and Markdown using Pandoc
- **External Editor Integration**: Edit web content in VS Code
- **Raw HTML Editing**: Direct HTML editing in VS Code
- **Universal Compatibility**: Works with email clients (Outlook), learning management systems (Moodle), and WYSIWYG editors (TinyMCE)

## Architecture

PandocEverywhere uses a client-server architecture:

- **Browser Extension** (content script) - Monitors and enhances contenteditable elements
- **Flask Backend** (port 5000) - Orchestrates VS Code editing workflow with Pandoc conversions

## Installation

### Prerequisites

- Python 3.x with Flask
- Pandoc (tested with Quarto's bundled Pandoc at `/opt/quarto/bin/tools/pandoc`)
- VS Code (at `/usr/bin/code`)

### Browser Extension

1. Open your browser's extension management page
2. Enable "Developer mode"
3. Load unpacked extension from the `extension/` directory

### Backend Server

```bash
cd server
python pandoc_everywhere.py
```

The Flask server will run on `http://localhost:5000`

## Usage

### Keyboard Shortcuts

All shortcuts open VS Code for editing:

- **Pause**: Edit in Markdown format (HTML → Markdown → VS Code → HTML)
- **Ctrl+Pause**: Edit in HTML with raw HTML preservation
- **Alt+Pause**: Edit raw HTML directly

### Workflow

1. Click into any contenteditable field on a webpage
2. Press the appropriate keyboard shortcut
3. VS Code opens with the content converted to the selected format
4. Edit and save the file in VS Code
5. Close VS Code to convert back and update the web content

## Project Structure

```
PandocEverywhere/
├── extension/
│   ├── content.js           # Main extension logic
│   ├── manifest.json        # Extension manifest
│   └── icons/              # Extension icons
├── server/
│   └── pandoc_everywhere.py # Flask backend server
└── notes.md                 # Development notes
```

## Technical Details

- **Version**: 1.1.0
- **Manifest Version**: 3
- **Languages**: JavaScript (extension), Python (backend)
- **Data Storage**: `~/.local/share/PandocEverywhere/` (XDG compliant)

## Tested Platforms

- Outlook Web
- Moodle
- TinyMCE editors

## License

TBD

## Contributing

This project is in active development. See `notes.md` for current TODOs and planned features.
