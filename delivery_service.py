from swarm import Particle
from system import *


class Courier:

    def __init__(self, order_list):
        self._order_list = order_list
        #self.fitness = self.calculate_route()[1]
        #self.route = self.calculate_route()[0]
        self.max_bag_weight = 18
        self.bag = []
    def bag_weight(self):
        return sum([x.weight for x in self.bag])

    def calculate_route(self, timetable: TimeTable) -> Tuple[List[Stop], float]:
        """
        Choosing path based on orders order :).
        :param timetable: table containing travel time between points
        :return: Courier path, cost of the path
        TODO:
        Steps:
        Go to first order source
            add first order to bag
            add as much left orders as possible
        For each order in a list
            if order in the bag:
                For each order in the bag:
                    if it's not current order from a list:
                        go to it's destination
                        add destination to the path
                        update cost
                        update time in bag for all orders in bag
                        remove order from the bag
                    else:
                        go to it's destination
                        add destination to the path
                        update cost
                        update time in bag for all orders in bag
                        remove order from the bag
                        break;
            else:
                For each order in the bag:
                    if bag is not empty:
                        if time to deliver this order is smaller than to pick up new:
                            go to it's destination
                            add destination to the path
                            update cost
                            update time in bag for all orders in bag
                            remove order from the bag

                        else:
                            if weight of the order in the list and bag weight is permitted:
                                go to order in bag destination
                                add destination to the path
                                update cost
                                update time in bag for all orders in bag
                                remove order from the bag
                            else:
                                go to order in bag source
                                update time in bag for all orders in bag
                                add source to the path
                                add order to the bag
                                update cost
                                add as much left orders as possible

                    else:
                        go to order in bag source
                        update time in bag for all orders in bag
                        add source to the path
                        add order to the bag
                        update cost
                        add as much left orders as possible



        """
        path: List[Stop] = []
        cost: float = 0
        self.bag.append(self.order_list[0])
        path.append(self.order_list[0].source)
        for order in self._order_list:
            pass








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

