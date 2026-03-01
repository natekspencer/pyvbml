"""Index.

Port of Vestaboard/vbml/src/index.ts

Main entry point. Exposes the `vbml` namespace object and re-exports
all public types.
"""

from __future__ import annotations

from typing import cast

from .calendar import make_calendar
from .character_codes_to_ascii import character_codes_to_ascii
from .character_codes_to_string import character_codes_to_string
from .classic import classic
from .copy_character_codes import copy_character_codes
from .create_empty_board import create_empty_board
from .has_special_characters import has_special_characters
from .layout_components import layout_components
from .parse_calendar_component import parse_calendar_component
from .parse_component import parse_absolute_component, parse_component
from .sanitize_special_characters import sanitize_special_characters
from .types import IVBML, IVBMLComponent

# Flagship board dimensions
_BOARD_ROWS = 6
_BOARD_COLUMNS = 22


def _parse(input_data: IVBML) -> list[list[int]]:
    """Parse."""
    style = input_data.get("style") or {}
    height = style.get("height") or _BOARD_ROWS
    width = style.get("width") or _BOARD_COLUMNS
    props = input_data.get("props") or {}

    empty_board = create_empty_board(height, width)

    raw_components = input_data.get("components", [])

    def _has_abs(c: IVBMLComponent) -> bool:
        return bool((c.get("style") or {}).get("absolutePosition"))

    # Flow components (no absolute position, not a calendar)
    flow_components = [
        parse_component(height, width, props, c)
        for c in raw_components
        if not _has_abs(c) and "calendar" not in c
    ]

    # Absolute-positioned components (not calendars)
    absolute_components = [
        parse_absolute_component(height, width, props, c)
        for c in raw_components
        if _has_abs(c) and "calendar" not in c
    ]

    # Calendar components
    calendar_components = []
    for c in raw_components:
        if "calendar" not in c:
            continue
        cal_data = c["calendar"]
        x = cast(
            dict, cast(dict, c.get("style") or {}).get("absolutePosition") or {}
        ).get("x", 0)

        cal = make_calendar(
            month=cal_data["month"],
            year=cal_data["year"],
            default_day_color=cal_data.get("defaultDayColor"),
            highlighted_days=cal_data.get("days", {}),
            hide_day_of_week=cal_data.get("hideSMTWTFS", False),
            hide_dates=cal_data.get("hideDates", False),
            hide_month_year=cal_data.get("hideMonthYear", False),
        )
        calendar_components.append(parse_calendar_component(cal, x))

    return layout_components(
        empty_board, flow_components, absolute_components, calendar_components
    )


class VBML:
    """
    Namespace object mirroring the `export const vbml = { ... }` in index.ts.

    Usage:
        from vbml.src import vbml
        board = vbml.parse({"components": [{"template": "Hello!"}]})
        print(vbml.character_codes_to_ascii(board))
    """

    parse = staticmethod(_parse)
    character_codes_to_string = staticmethod(character_codes_to_string)
    character_codes_to_ascii = staticmethod(character_codes_to_ascii)
    copy_character_codes = staticmethod(copy_character_codes)
    classic = staticmethod(classic)
    has_special_characters = staticmethod(has_special_characters)
    sanitize_special_characters = staticmethod(sanitize_special_characters)
