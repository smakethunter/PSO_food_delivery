import numpy as np
from typing import *
import itertools
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from drawing_utils import draw_line


class Stop:
    id_iter = itertools.count()

    def __init__(self):
        self._id = next(Stop.id_iter)
        self.cords = np.array([np.random.uniform(40., 50.), np.random.uniform(13., 15.)])

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new):
        self.id = new


class Restaurant(Stop):
    id_iter = itertools.count()

    def __init__(self, *args, **kwargs):
        super().__init__()
        self._order_list = []
        self.restaurant_id = next(Restaurant.id_iter)

    def __str__(self):
        return f'Restaurant {self.restaurant_id}'

    def orders_weight(self):
        return sum([x.weight for x in self.order_list])

    @property
    def order_list(self):
        return self._order_list

    @order_list.setter
    def order_list(self, order_list):
        self.order_list = order_list

    pass

    def add_order(self, order):
        self._order_list.append(order)

class Client(Stop):
    id_iter = itertools.count()

    def __init__(self, *args, **kwargs):
        super(Client, self).__init__()
        self.client_id = next(Client.id_iter)

    def __str__(self):
        return f'Client {self.client_id}'

    pass


class Order:
    id_iter = itertools.count()

    def __init__(self, restaurant, client, weight):
        self.source = restaurant
        self.destination = client
        self.weight = weight
        self.id = next(Order.id_iter)
        self._time_in_bag = 0

    def __str__(self):
        return f'Order {self.id}'

    @property
    def time_in_bag(self):
        return self._time_in_bag

    @time_in_bag.setter
    def time_in_bag(self, time):
        self._time_in_bag = time

    pass


class TimeTable:
    def __init__(self, point_list = None):
        self.table= TimeTable.create_time_table(point_list) if point_list is not None else []
        self.point_list = point_list if point_list is not None else []

    def get_path_time(self, source, destination):
        return self.table[source][destination]

    @staticmethod
    def get_time(source, destination):
        distance = np.linalg.norm((source - destination))
        velocity = 1.
        time = distance / velocity
        return time

    @staticmethod
    def create_time_table(points: List[Stop]):
        time_table = []
        for source in points:
            time_source_to_dest = []
            for destination in points:
                if source.id == destination.id:
                    time_source_to_dest.append(0)
                else:
                    time_source_to_dest.append(TimeTable.get_time(source.cords, destination.cords))
            time_table.append(time_source_to_dest)
        return time_table

    def add_element(self, point):
        if len(self.point_list) > 0:
            self.point_list.append(point)
            self.table.append([self.get_time(point.cords, dest.cords) for dest in self.point_list])
            for i, row in enumerate(self.table):
                row.append(self.get_time(point.cords, self.point_list[i].cords))

        else:
            self.point_list.append(point)
            self.table.append([self.get_time(point.cords, point.cords)])
        print(self.table)
        pass

    def draw_table(self, draw_distances=False):
        plt.figure("points")
        for point in self.point_list:
            c = 'red' if isinstance(point, Restaurant) else "blue"
            plt.scatter(point.cords[0], point.cords[1], c=c)
            plt.annotate(str(point), (point.cords[0], point.cords[1]))
            if draw_distances:
                for point_to in self.point_list:
                    draw_line(point, point_to, self, 'red')

        plt.show()



