import pytest
from src.char_encoder.core.converter import (
    analyze_chars,
    analyze_text,
    encode_text,
)


def test_ascii_char():
    (info,) = analyze_chars("A")
    assert info.codepoint == 65
    assert info.codepoint_hex == "U+0041"
    assert info.codepoint_binary == "01000001"
    assert info.ascii_decimal == "65"


def test_non_ascii_has_no_ascii_value():
    (info,) = analyze_chars("你")
    assert info.codepoint == 0x4F60
    assert info.ascii_decimal == "—"


def test_utf8_round_trip_for_chinese():
    r = encode_text("你好", "utf-8")
    assert r.ok
    assert r.data == b"\xe4\xbd\xa0\xe5\xa5\xbd"
    assert r.hex == "E4 BD A0 E5 A5 BD"


def test_ascii_encoding_fails_for_chinese():
    r = encode_text("你好", "ascii")
    assert not r.ok
    assert "ascii" in (r.error or "")


def test_analyze_text_returns_one_result_per_encoding():
    chars, results = analyze_text("ab", encodings=("utf-8", "ascii"))
    assert len(chars) == 2
    assert [r.encoding for r in results] == ["utf-8", "ascii"]


def test_unknown_encoding_does_not_raise():
    r = encode_text("abc", "not-a-real-encoding")
    assert not r.ok