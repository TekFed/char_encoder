# char-encoder

Convert text to **ASCII, binary, hex, and Unicode encodings** — with a
Tkinter GUI, a CLI, and a clean core module you can reuse.

## Install (dev)

    python -m venv .venv
    source .venv/bin/activate    # Windows: .venv\Scripts\activate
    pip install -e ".[dev]"

## Run

    char-encoder-gui                  # GUI
    python -m char_encoder            # same GUI
    char-encoder "Hello 你好"         # CLI
    python -m char_encoder.cli "A"    # CLI directly

## Test

    pytest

## Architecture

- `core/converter.py` — pure logic, no GUI. Testable.
- `gui/app.py` — Tkinter window, calls only the core API.
- `cli.py` — CLI entry point, same core.

Adding a new encoding is a one-liner in `DEFAULT_ENCODINGS`; both UI
and CLI pick it up automatically.