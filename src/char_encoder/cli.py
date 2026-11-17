"""Command-line interface: python -m char_encoder 'Hello 你好'."""
from __future__ import annotations

import argparse
import sys

from .core.converter import analyze_text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="char-encoder",
        description="Show ASCII / binary / hex / Unicode encodings of text.",
    )
    parser.add_argument("text", nargs="*", help="Text to convert (default: stdin)")
    args = parser.parse_args(argv)

    text = " ".join(args.text) if args.text else sys.stdin.read().rstrip("\n")
    if not text:
        parser.print_help()
        return 1

    chars, encodings = analyze_text(text)

    print(f"\nWord: {text}\n")
    print(f"{'Char':<6}{'U+':<10}{'Dec':<8}{'CodePointBinary':<20}{'ASCII':<8}Name")
    print("-" * 80)
    for c in chars:
        print(f"{c.char:<6}{c.codepoint_hex:<10}{c.codepoint:<8}"
            f"{c.codepoint_binary:<20}{c.ascii_decimal:<8}{c.name}")

    print()
    for r in encodings:
        print(f"── {r.encoding.upper()} ──")
        if r.ok:
            print(f"  hex:    {r.hex}")
            print(f"  binary: {r.binary}")
        else:
            print(f"  ⚠  {r.error}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())