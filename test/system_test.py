import unittest
from system import Order, TimeTable, Stop, Restaurant, Client


class TestId(unittest.TestCase):
    def test_id_assignment(self):
        client = Client()
        restaurant = Restaurant([1, 2, 3])
        restaurant2 = Restaurant([1, 2, 2])
        self.assertEqual(1, restaurant.id)
        self.assertEqual(0, client.id)
        self.assertEqual(restaurant2.id, 2)


class TestOrderMethods(unittest.TestCase):
    def test_nr_assignment(self):
        order_list = []
        for x in range(10):
            order_list.append(Order(1, 2, 3))
        self.assertEqual(4, order_list[4].id)


class TestTimeTable(unittest.TestCase):
    def test_table(self):
        table = TimeTable([[1,2],[3,4]])
        self.assertEqual(table.get_path_time(1,1),1)


if __name__ == '__main__':
    unittest.main()
