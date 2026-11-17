"""Pure conversion logic — no GUI dependencies."""
from __future__ import annotations

import unicodedata
from collections.abc import Iterable
from dataclasses import dataclass

DEFAULT_ENCODINGS: tuple[str, ...] = ("utf-8", "utf-16-be", "utf-16-le", "gbk", "ascii")


# ---------------------------------------------------------------------------
# Data containers
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CharInfo:
    """Everything you can know about one character."""
    char: str
    codepoint: int
    name: str

    @property
    def codepoint_hex(self) -> str:
        return f"U+{self.codepoint:04X}"

    @property
    def codepoint_binary(self) -> str:
        width = 8 if self.codepoint < 0x80 else 16 if self.codepoint < 0x10000 else 32
        return format(self.codepoint, f"0{width}b")

    @property
    def ascii_decimal(self) -> str:
        """Decimal ASCII value, or an em-dash if outside 0–127."""
        return str(self.codepoint) if self.codepoint < 128 else "—"


@dataclass(frozen=True)
class EncodingResult:
    """The result of trying to encode a string with one encoding."""
    encoding: str
    data: bytes | None = None
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.error is None

    @property
    def hex(self) -> str:
        return " ".join(f"{b:02X}" for b in self.data) if self.data else ""

    @property
    def binary(self) -> str:
        return " ".join(format(b, "08b") for b in self.data) if self.data else ""

    @property
    def size(self) -> int:
        return len(self.data) if self.data else 0


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def analyze_chars(text: str) -> list[CharInfo]:
    """Return one CharInfo per character in ``text``."""
    infos: list[CharInfo] = []
    for ch in text:
        try:
            name = unicodedata.name(ch)
        except ValueError:
            name = "<unnamed>"
        infos.append(CharInfo(char=ch, codepoint=ord(ch), name=name))
    return infos


def encode_text(text: str, encoding: str) -> EncodingResult:
    """Try to encode ``text`` with ``encoding`` — never raises."""
    try:
        return EncodingResult(encoding=encoding, data=text.encode(encoding))
    except (UnicodeEncodeError, LookupError) as exc:
        return EncodingResult(encoding=encoding, error=str(exc))


def analyze_text(
    text: str, encodings: Iterable[str] = DEFAULT_ENCODINGS
) -> tuple[list[CharInfo], list[EncodingResult]]:
    """Convenience wrapper: characters + every requested encoding."""
    return analyze_chars(text), [encode_text(text, enc) for enc in encodings]