"""
Generate convex polygons.
"""

import math
import random
from typing import List

from .utils import PI, EXP, NOISE


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


def random_convex(n: int, max_coord: int = 60) -> List[Vector]:
    """Return a random convex polygon with n >= 3 vertices, such that none of its vertices have a coordinate bigger than max_coord."""
    if n < 3:
        raise ValueError("n must be at least 3")
    max_r = random.randint(2, max_coord // n)

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

    start = Vector(random.randint(-NOISE, NOISE), random.randint(-NOISE, NOISE))
    points = [start]
    for vec in vecs:
        points.append(points[-1] + vec)
    points.pop()
    random.shuffle(points)

    return points
