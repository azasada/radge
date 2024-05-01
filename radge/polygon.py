"""
Generate convex polygons.
"""

from __future__ import annotations
import math
import random
from typing import List

import radge.utils as utils


class Vector:
    """Vector in the cartesian plane."""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __lt__(self, rhs):
        if self.x == rhs.x:
            return self.y < rhs.y
        return self.x < rhs.x

    def __add__(self, rhs):
        return Vector(self.x + rhs.x, self.y + rhs.y)

    def __radd__(self, rhs):
        if rhs == 0:
            return self
        else:
            return self.__add__(rhs)

    def __sub__(self, rhs):
        return Vector(self.x - rhs.x, self.y - rhs.y)

    def __rsub__(self, rhs):
        if rhs == 0:
            return self
        else:
            return self.__sub__(rhs)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __repr__(self):
        return f"[{self.x}, {self.y}]"

    def norm(self) -> float:
        """Return the norm of the vector."""
        return math.sqrt(self.x**2 + self.y**2)

    def dist(self, rhs: Vector) -> float:
        """Return the (squared) distance between two points."""
        return (self - rhs).norm()

    def angle(self) -> float:
        """Return the directed angle (in radians) that the vector makes with the X-axis."""
        return math.atan2(self.y, self.x)

    def cross(self, rhs: Vector) -> int:
        """Return the magnitude of the 2D cross product."""
        return self.x * rhs.y - rhs.x * self.y

    def orient(self, a: Vector, b: Vector) -> int:
        """Return neg/0/pos if this point is to the right/collinear/to the left of line ab."""
        return (a - self).cross(b - self)


def random_convex(n: int) -> List[Vector]:
    """Return a random convex polygon with 3 <= x <= n vertices. Vertices have integer coords."""
    points = [
        Vector(
            random.randint(-utils.MAX_COORD, utils.MAX_COORD),
            random.randint(-utils.MAX_COORD, utils.MAX_COORD),
        )
        for _ in range(n)
    ]
    if n <= 3:
        return points
    points.sort()

    upper = []
    for point in points:
        while len(upper) >= 2 and upper[-2].orient(upper[-1], point) >= 0:
            upper.pop()
        upper.append(point)
    upper.pop()

    lower = []
    for point in reversed(points):
        while len(lower) >= 2 and lower[-2].orient(lower[-1], point) >= 0:
            lower.pop()
        lower.append(point)
    lower.pop()

    return lower + upper
