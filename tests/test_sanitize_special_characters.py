"""Test sanitize special characters.

Port of Vestaboard/vbml/src/__tests__/sanitizeSpecialCharacters.spec.ts
"""

from __future__ import annotations

from pyvbml.sanitize_special_characters import sanitize_special_characters


def test_does_not_modify_plain_text() -> None:
    """Should not modify text without special characters"""
    text = "abcdefghijklmnopqrstuvwxyz"
    assert sanitize_special_characters(text) == text


def test_replaces_accented_character() -> None:
    """Should replace special characters with their equivalent"""
    assert sanitize_special_characters("Ã") == "a"


def test_handles_sentence() -> None:
    """Should handle a sentence or two"""
    text = "hello world"
    assert sanitize_special_characters(text) == text


def test_handles_mixed_special_characters() -> None:
    """Should handle mixed special characters in text"""
    assert sanitize_special_characters("héllo wôrld") == "hello world"


def test_handles_multiple_special_characters_together() -> None:
    """Should handle multiple special characters together"""
    assert sanitize_special_characters("ëï") == "ei"


def test_replaces_fractions_with_multiple_characters() -> None:
    """Should replace fractions with multiple characters"""
    assert sanitize_special_characters("½") == "1/2"


def test_sanitizes_variation_selector_16_from_heart_emoji() -> None:
    """Should sanitize variation selector-16 (U+FE0F) from ❤️"""
    assert sanitize_special_characters("❤️") == "❤"


def test_sanitizes_variation_selector_16_from_unicode_literal() -> None:
    """Should sanitize variation selector-16 (U+FE0F) from the string literal \\u2764\\uFE0F"""
    assert sanitize_special_characters("\u2764\ufe0f") == "\u2764"


def test_does_not_replace_vestaboard_heart() -> None:
    """Should not replace Vestaboard Note unicode hearts (U+2764)"""
    assert sanitize_special_characters("\u2764") == "❤"


def test_accepts_whitespace_after_heart() -> None:
    """Should accept whitespace after \\u2764 (U+2764)"""
    text = "\u2764 "
    assert sanitize_special_characters(text) == text


def test_preserves_spaces_between_black_hearts() -> None:
    """Should not clear whitespace between black heart unicode characters"""
    test_string = "❤ ❤ ❤ ❤ ❤"
    assert sanitize_special_characters(test_string) == test_string


def test_preserves_space_between_heart_and_latin_glyph() -> None:
    """Should not trim whitespace when \\u2764 is followed by a latin glyph"""
    test_string = "\u2764 A"
    assert sanitize_special_characters(test_string) == test_string


def test_preserves_space_between_heart_and_emoji() -> None:
    """Should not trim whitespace when \\u2764 is followed by an emoji"""
    test_string = "\u2764 🟧"
    assert sanitize_special_characters(test_string) == test_string


def test_converts_unsupported_sequenced_emojis_to_whitespace() -> None:
    """Should convert unsupported, sequenced emojis to whitespace"""
    test_string = "☠️⚠️✅▶️✨⌛️"
    equivalent_whitespace = "\u0020" * 6
    assert sanitize_special_characters(test_string) == equivalent_whitespace


def test_handles_heart_emoji_and_unsupported_emojis() -> None:
    """Should handle the heart emoji and unsupported emojis"""
    test_string = "❤️☠️⚠️✅▶️✨⌛️"
    expectation = "\u2764" + "\u0020" * 6
    assert sanitize_special_characters(test_string) == expectation


def test_sanitizes_german_and_special_characters() -> None:
    """Should sanitize all German and special characters"""
    assert sanitize_special_characters("ä") == "AE"
    assert sanitize_special_characters("Ä") == "AE"
    assert sanitize_special_characters("ö") == "OE"
    assert sanitize_special_characters("Ö") == "OE"
    assert sanitize_special_characters("ü") == "UE"
    assert sanitize_special_characters("Ü") == "UE"
    assert sanitize_special_characters("ß") == "SS"

    assert sanitize_special_characters("ø") == "o"
    assert sanitize_special_characters("å") == "a"

    assert sanitize_special_characters("œ") == "OE"
    assert sanitize_special_characters("æ") == "AE"

    assert sanitize_special_characters("ç") == "c"
    assert sanitize_special_characters("ƒ") == "f"
    assert sanitize_special_characters("µ") == " "  # micro sign → space

    assert sanitize_special_characters("…") == "..."
    assert sanitize_special_characters("–") == "-"
    assert sanitize_special_characters("⁄") == "/"

    all_chars = "äÄöÖüÜßøåœæçƒµ…–⁄∑¡¶¢[]|{}≠¿€®†¨π•±∂©º∆@¥≈√∫~∞"
    result = sanitize_special_characters(all_chars)
    assert result
    assert isinstance(result, str)
    assert not any(c in result for c in "äÄöÖüÜßøåœæçƒµ")


def test_german_text_with_umlauts_in_context() -> None:
    """Should handle German text with umlauts in context"""
    german_text = "Über die Brücke gehen wir für Österreich"
    result = sanitize_special_characters(german_text)
    assert result == "UEber die BrUEcke gehen wir fUEr OEsterreich"


def test_german_sharp_s_in_context() -> None:
    """Should handle German sharp s (ß) in context"""
    assert sanitize_special_characters("Straße") == "StraSSe"


def test_converts_sharp_s_in_all_contexts() -> None:
    """Should convert ß to SS in all contexts"""
    cases = [
        ("ß", "SS"),
        ("Straße", "StraSSe"),
        ("fußball", "fuSSball"),
        ("groß", "groSS"),
        ("weiß", "weiSS"),
    ]
    for text, expected in cases:
        assert sanitize_special_characters(text) == expected
