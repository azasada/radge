"""
Utility functions, constants and the global RNG seed
"""

import time

SEED = int(time.time())
NOISE = 4
PI = 3.14159265358979323846
EXP = 2.71828182845904523536

ALPHA_LOWER = "abcdefghijklmnopqrstuvwxyz"
ALPHA_UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def seed(seed: int) -> None:
    """Set global RNG seed."""
    global SEED
    SEED = seed
