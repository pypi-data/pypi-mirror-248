import unittest
from mtbp3.util import lsr 


class TestSimple(unittest.TestCase):

    def test_lsr_01(self):
        self.assertEqual(lsr.lsr_tree(''), '')


if __name__ == '__main__':
    unittest.main()



