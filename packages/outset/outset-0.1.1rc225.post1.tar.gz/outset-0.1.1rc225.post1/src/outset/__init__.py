"""Top-level package for outset."""

__version__ = "0.1.1""-rc225-post1"

from ._draw_marquee import draw_marquee
from ._inset_outsets import inset_outsets
from ._marqueeplot import marqueeplot
from ._OutsetGrid import OutsetGrid

__all__ = [
    "draw_marquee",
    "inset_outsets",
    "marqueeplot",
    "OutsetGrid",
]
