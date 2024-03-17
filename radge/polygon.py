"""
Generate convex polygons.
"""

import math
import cmath
import random

from .utils import PI, EXP

class Point:
    """Point in the cartesian plane."""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
