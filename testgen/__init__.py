"""
TestGen: a Python library for generating test cases for algorithmic problems.
The name is only temporary.
"""

from __future__ import absolute_import
import random

from .graph import *


def init(s):
    """Initialize the RNG."""
    random.seed(s)
