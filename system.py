import numpy as np
from typing import *
import itertools


class Stop:
    id_iter = itertools.count()

    def __init__(self):
        self._id = next(Stop.id_iter)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new):
        self.id = new


class Restaurant(Stop):

    def __init__(self, order_list, *args, **kwargs):
        super().__init__()
        self.order_list = order_list
        


    def orders_weight(self):
        return sum([x.weight for x in self.order_list])

    pass


class Client(Stop):
    def __init__(self, *args, **kwargs):
        super(Client, self).__init__()

    pass


class Order:
    id_iter = itertools.count()

    def __init__(self, restaurant, client, weight):
        self.source = restaurant
        self.destination = client
        self.weight = weight
        self.id = next(Order.id_iter)
        self._time_in_bag = 0

    @property
    def time_in_bag(self):
        return self._time_in_bag

    @time_in_bag.setter
    def time_in_bag(self, time):
        self.time_in_bag = time

    pass


class TimeTable:
    def __init__(self, table):
        self.table: np.array = np.array(table)

    def get_path_time(self, source, destination):
        return self.table[source, destination]
