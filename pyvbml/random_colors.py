"""Random colors.

Port of Vestaboard/vbml/src/randomColors.ts
"""

from __future__ import annotations

import random

from .character_codes import COLOR_CODES, CharacterCode


def random_colors(
    rows: int = 6,
    columns: int = 22,
    colors: list[CharacterCode] | list[int] | None = None,
) -> list[list[int]]:
    """Random colors."""
    if colors is None:
        colors = COLOR_CODES
    return [[random.choice(colors) for _ in range(columns)] for _ in range(rows)]
