"""
Generate various types of strings.
"""

import random

from .utils import ALPHA_LOWER, ALPHA_UPPER


class String:
    """A string made using characters from the given alphabet."""

    def __init__(self, len: int, alpha: str = ALPHA_LOWER + ALPHA_UPPER):
        self.len = len
        self.alpha = alpha
        self.s = "".join(random.choice(alpha) for _ in range(len))

    def __str__(self) -> str:
        """Return the string."""
        return self.s

    def substr(self, len: int) -> str:
        """Return a random substring of given length."""
        if len > self.len:
            raise ValueError(
                "Length of a substring cannot be greater than the length of the string."
            )
        r = random.randint(len - 1, self.len - 1)
        return self.s[(r - len + 1) : (r + 1)]

    def subseq(self, len: int) -> str:
        """Return a random subsequence of given length."""
        if len > self.len:
            raise ValueError(
                "Length of a subsequence cannot be greater than the length of the string."
            )
        pos = sorted(random.sample(range(self.len), len))
        return "".join(self.s[i] for i in pos)
