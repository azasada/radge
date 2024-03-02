"""
Generate various types of strings.
"""

import random
from typing import Optional

from .utils import ALPHA_LOWER, ALPHA_UPPER

class String:
    """A string made using letters from the given alphabet."""

    def __init__(self, len: int, alpha: str = ALPHA_LOWER + ALPHA_UPPER, mod: int = 1_000_000_033, base: int = 47):
        self.len = len
        self.alpha = alpha
        self.s = "".join(random.choice(alpha) for _ in range(len))
        self.hash = 0

        p = 1
        for i in range(len):
            self.hash = (self.hash + p * (ord(self.s[i]) - ord("A"))) % mod
            p = (p * base) % mod

    def __str__(self) -> str:
        """Return the string."""
        return self.s
