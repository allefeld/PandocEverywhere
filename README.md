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
- **Flask Backend** (`localhost:5000`) - Orchestrates VS Code editing workflow with Pandoc conversions

## Installation

### Prerequisites

- Python 3.9 or later and [pipx](https://pipx.pypa.io/)
- Pandoc (tested with Quarto's bundled Pandoc at `/opt/quarto/bin/tools/pandoc`)
- VS Code (at `/usr/bin/code`)

### Browser Extension

1. Open your browser's extension management page
2. Enable "Developer mode"
3. Load unpacked extension from the `extension/` directory

### Backend Server

Install the server as a Python package with pipx, which pulls in Flask and the [Waitress](https://docs.pylonsproject.org/projects/waitress/) server:

```bash
pipx install ./server
```

Use `pipx install -e ./server` instead for an editable install, where changes to the source take effect after restarting the server.

Then run it:

```bash
pandoc-everywhere
```

The server listens on `http://localhost:5000`, and only accepts connections from the same computer.

To start it automatically at login, run it as a systemd user service, e.g. from a startup script:

```bash
systemd-run --user --collect --unit=pandoc-everywhere -p Restart=on-failure \
  -E PYTHONUNBUFFERED=1 ~/.local/bin/pandoc-everywhere
```

Its output is then available via `journalctl --user -u pandoc-everywhere`.

For development, `python server/pandoc_everywhere.py` runs it with Flask's development server in debug mode instead.

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
│   ├── pandoc_everywhere.py # Flask backend server
│   └── pyproject.toml       # Python package definition
└── notes.md                 # Development notes
```

## Technical Details

- **Version**: 1.1.0
- **Manifest Version**: 3
- **Languages**: JavaScript (extension), Python (backend)
- **Data Storage**: edited files are kept in the system temporary directory, in `PandocEverywhere-<version>/`

## Tested Platforms

- Outlook Web
- Moodle
- TinyMCE editors

## Contributing

This project is in active development. See `notes.md` for current TODOs and planned features.

***

Copyright © 2025–2026 Carsten Allefeld. Portions of this software were generated with AI assistance (Claude Code, GitHub Copilot) and may not be subject to copyright. To the extent copyright subsists, this software is released under the terms of the GNU General Public License, version 3 or later.
