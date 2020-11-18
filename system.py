import numpy as np
from swarm import Particle
from typing import *
from unittest import TestCase, main
import itertools


class Restaurant:
    id_iter = itertools.count()
    
    def __init__(self, order_list):
        self.id = next(Restaurant.id_iter)
        self.order_list = order_list
        
    def orders_weight(self):
        return sum([x.weight for x in self.order_list])
    pass


class Client:
    id_iter = itertools.count()

    def __init__(self, order_list):
        self.id = next(Client.id_iter)
    pass


class Order:

    id_iter = itertools.count()

    def __init__(self, restaurant, client, weight):
        self.source = restaurant
        self.destination = client
        self.weight = weight
        self.id = next(Order.id_iter)

    pass







