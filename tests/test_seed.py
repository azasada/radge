import unittest

import radge.utils as utils
import radge.sequences as seq

class TestSeed(unittest.TestCase):
    def test_is_same(self):
        """Test if a random sequence is the same if it's generated using the same seed twice."""
        TESTS = 100
        MAX_N = 10**4
        for _ in range(TESTS):
            start_seed = utils.SEED
            seq1 = seq.seq(MAX_N, range(1, MAX_N))
            utils.seed(2137)
            utils.seed(start_seed)
            seq2 = seq.seq(MAX_N, range(1, MAX_N))

            self.assertTrue(seq1 == seq2)

