"""Core package for the file organizer."""

from .organizer import (
    DEFAULT_RULES,
    MovePlanItem,
    OrganizerError,
    apply_moves,
    plan_moves,
)

__version__ = "0.1.0"

__all__ = [
    "DEFAULT_RULES",
    "MovePlanItem",
    "OrganizerError",
    "apply_moves",
    "plan_moves",
]
