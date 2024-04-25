"""
Generate numbers with desired properties
"""

import math
import random
import radge.utils as utils


def mpow(a: int, b: int, m: int) -> int:
    """Modular exponentiation."""
    res = 1
    while b > 0:
        if b % 2 == 1:
            res = (res * a) % m
        a = (a * a) % m
        b //= 2

    return res


def random_prime(max_n: int) -> int:
    """Generate a random prime number not greater than max_n."""

    def miller_rabin(n: int) -> bool:
        """Miller-Rabin primality test."""

        def is_composite(n: int, a: int, q: int, s: int) -> bool:
            x = mpow(a, q, n)
            if x == 1 or x == n - 1:
                return False
            for _ in range(1, s):
                x = (x * x) % n
                if x == n - 1:
                    return False

            return True

        if n == 2 or n == 3:
            return True

        s = 0
        q = n - 1
        while q % 2 == 0:
            q //= 2
            s += 1

        for a in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
            if n == a:
                return True
            if is_composite(n, a, q, s):
                return False

        return True

    random.seed(utils.SEED)
    bound, iters = 10 * int(math.log(max_n)), 0
    while iters < bound:
        n = random.randint(2, max_n)
        if miller_rabin(n):
            return n
        iters += 1

    return 2
