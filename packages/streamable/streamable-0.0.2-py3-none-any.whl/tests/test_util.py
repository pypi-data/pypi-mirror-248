import unittest

from streamable._util import sidify


class TestUtil(unittest.TestCase):
    def test_sidify(self):
        f = lambda x: x**2
        self.assertEqual(f(2), 4)
        self.assertEqual(sidify(f)(2), 2)

        # test decoration
        @sidify
        def f(x):
            return x**2

        self.assertEqual(f(2), 2)
