import unittest
from delivery_service import *


class TestCourierMethods(unittest.TestCase):

    def test_property(self):
        k1 = Courier([1, 2, 3])
        self.assertEqual(k1._order_list[0], 1)

    def test_setter(self):
        k1 = Courier([1, 2, 3])
        k1._order_list = [1, 3, 4]
        self.assertEqual(k1.order_list[1], 3)


if __name__ == '__main__':
    unittest.main()
