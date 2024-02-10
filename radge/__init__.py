"""
Radge: a Python library for generating test cases for algorithmic problems.
"""

from __future__ import absolute_import
import random
import time

from .graph import *


def init(s: int = time.time_ns()):
    """Initialize the RNG."""
    random.seed(s)
