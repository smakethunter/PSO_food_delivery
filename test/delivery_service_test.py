import unittest
from delivery_service import *


class TestCourierMethods(unittest.TestCase):

    def test_property(self):
        c1 = Client()
        r1 = Restaurant([])
        o1 = Order(r1,c1,1)
        r1 = Restaurant()
        time_table = TimeTable([r1,c1])
        k1 = Courier([o1])
        self.assertEqual(k1._order_list[0].id, 0)



time_table = TimeTable()
class TestPathAssignment(unittest.TestCase):
    def test_delivery_weight_not_exceeded_one_order_restaurant(self):
        r1 = Restaurant()
        r2 = Restaurant()
        r3 = Restaurant()
        c1 = Client()
        c2 = Client()
        c3 = Client()
        o1 = Order(r1, c1, 12)
        o2 = Order(r2, c2, 6)
        o3 = Order(r3, c3, 5)
        r1.order_list.append(o1)
        r3.order_list.append(o3)
        r2.order_list.append(o2)
        for x in [r1, r2, r3, c1, c2, c3]:
            time_table.add_element(x)
        courier = Courier([o1, o2, o3])
        cost = sum([time_table.get_path_time(r1.id, c1.id),
                    time_table.get_path_time(c1.id, r2.id),
                    time_table.get_path_time(r2.id, c2.id),
                    time_table.get_path_time(c2.id, r3.id),
                    time_table.get_path_time(r3.id, c3.id)])
        print('___test____')
        print(cost)
        print(courier.fitness(time_table))
        print([str(x) for x in courier.get_path(time_table)])
        courier.draw_route(time_table)
        del courier
        del r1
        del r2
        del r3
        del c1
        del c2
        del c3
        del o1
        del o2
        del o3


    def test_delivery_weight_exceeded_one_order_restaurant(self):
            r1 = Restaurant()
            r2 = Restaurant()
            r3 = Restaurant()
            c1 = Client()
            c2 = Client()
            c3 = Client()
            o1 = Order(r1, c1, 12)
            o2 = Order(r2, c2, 6)
            o3 = Order(r3, c3, 5)
            r1.order_list.append(o1)
            r3.order_list.append(o3)
            r2.order_list.append(o2)
            for x in [r1, r2, r3, c1, c2, c3]:
                time_table.add_element(x)
            courier = Courier([o1, o2, o3])
            cost = sum([time_table.get_path_time(r1.id, c1.id),
                        time_table.get_path_time(c1.id, r2.id),
                        time_table.get_path_time(r2.id, c2.id),
                        time_table.get_path_time(c2.id, r3.id),
                        time_table.get_path_time(r3.id, c3.id)])
            print('___test____')
            print(cost)
            print(courier.fitness(time_table))
            print([str(x) for x in courier.get_path(time_table)])
            courier.draw_route(time_table)


if __name__ == '__main__':
    unittest.main()
