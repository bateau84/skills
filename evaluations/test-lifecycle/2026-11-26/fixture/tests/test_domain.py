import unittest
from orders import qualifies

class MinimumOrderTests(unittest.TestCase):
    def test_minimum_order_rule(self):
        for amount, expected in [(9, False), (11, True)]:
            with self.subTest(amount=amount):
                self.assertEqual(qualifies(amount, 10), expected)
