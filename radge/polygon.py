"""
Generate convex polygons.
"""

import math
import random
from typing import List

import radge.utils as utils

class Vector:
    """Vector in the cartesian plane."""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

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

    def angle(self) -> float:
        """Return the directed angle (in radians) that the vector makes with the X-axis."""
        return math.atan2(self.y, self.x)

# TODO: change this to finding the convex hull of a random set of points.
def random_convex(n: int, max_coord: int = 1000) -> List[Vector]:
    """Return a random convex polygon with n >= 3 vertices, such that none of its vertices have a coordinate bigger than max_coord."""
    # note: degenerate polygons are possible (for example a "triangle" with 3 colinear points)
    if n < 3:
        raise ValueError("n must be at least 3")
    random.seed(utils.SEED)
    max_r = random.randint(2, 2 + max_coord // n)

    vecs = []
    cur = Vector(0, 0)
    for _ in range(n - 1):
        new_p = cur
        while new_p == cur:
            new_p = Vector(
                random.randint(cur.x - max_r, cur.x + max_r),
                random.randint(cur.y - max_r, cur.y + max_r),
            )
        vecs.append(new_p - cur)
        cur = new_p
    vecs.append(-cur)
    vecs.sort(key=lambda v: v.angle())

    start = Vector(random.randint(-utils.NOISE, utils.NOISE), random.randint(-utils.NOISE, utils.NOISE))
    points = [start]
    for vec in vecs:
        points.append(points[-1] + vec)
    points.pop()

    return points
