from swarm import Particle
from system import *


class Courier:

    def __init__(self, order_list):
        self._order_list = order_list
        #self.fitness = self.calculate_route()[1]
        #self.route = self.calculate_route()[0]
        self.max_bag_weight = 18

    def calculate_route(self) -> Tuple[List[float], float]:
        pass

    @property
    def order_list(self):
        return self._order_list

    @order_list.setter
    def order_list(self, new_list):
        self.order_list = new_list

    pass


class DeliveryService(Particle):
    def __init__(self, nr_couriers, min_nr_orders, max_nr_orders, order_list):
        super(DeliveryService, self).__init__(order_list)
        self.nr_couriers = nr_couriers
        self.min_nr_orders = min_nr_orders
        self.max_nr_orders = max_nr_orders

    # TODO: ustalenie startowej dystrybucji zamówień na kurierów
    def generate_starting_position(self, order_list):
        pass

    def move(self):
        pass

    def compute_velocity(self):
        pass

    def fitness(self):
        fitness = 0
        for row in self.position:
            courier = Courier(row)
            fitness += courier.fitness
        return fitness

