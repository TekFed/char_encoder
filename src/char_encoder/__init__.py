"""Character Encoder — text to ASCII / binary / hex / Unicode."""
from .core.converter import (
    CharInfo,
    EncodingResult,
    analyze_chars,
    analyze_text,
    encode_text,
)

__all__ = [
    "CharInfo",
    "EncodingResult",
    "analyze_chars",
    "analyze_text",
    "encode_text",
]
__version__ = "0.1.0"