import unittest
from delivery_service import Courier
from system import Order


class TestOrderMethods(unittest.TestCase):
    def test_nr_assignment(self):
        order_list=[]
        for x in range(10):
            order_list.append(Order(1, 2, 3))
        self.assertEqual(4, order_list[4].id)


if __name__ == '__main__':
    unittest.main()
