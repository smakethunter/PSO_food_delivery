
from system import *

class Courier:

    def __init__(self, order_list):
        self._order_list = order_list
        self.max_bag_weight = 18
        self._bag: List[Order] = []
    pass

    def get_path(self, timetable):
        path, fitness = self.calculate_route(timetable=timetable)
        return path

    def fitness(self, timetable):
        path, fitness = self.calculate_route(timetable=timetable)
        return fitness

    @property
    def order_list(self):
        return self._order_list

    @order_list.setter
    def order_list(self, new_list):
        self.order_list = new_list

    pass

    @property
    def bag(self):
        return self._bag

    @bag.setter
    def bag(self, bag):
        self._bag = bag

    def bag_weight(self):
        return sum([x.weight for x in self.bag])

    def update_delivery_time(self, time):
        if self.bag:
            for order in self.bag:
                order.time_in_bag += time

    def calculate_route(self,timetable):
        """
        Choosing path based on orders order :).
        :param timetable: table containing travel time between points
        :return: Courier path, cost of the path
        TODO:
        Steps:
        1.
        Go to first order source
            add first order to bag
            add as much left orders as possible
        2.
        For each order in a list
        2a.
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
            2b.
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
                                break

                    else:
                        go to order in list source
                        add source to the path
                        add order to the bag
                        add as much left orders as possible
                        update cost




        """


        path: List[Stop] = []
        cost: float = 0
        i=0
        print('start')
        start_order: Order = self._order_list[0]
        self.bag.append(start_order)
        path.append(start_order.source)
        # 1.
        for order_in_source in start_order.source.order_list:
            if order_in_source.id is not start_order.id:
                if self.bag_weight() + order_in_source.weight < self.max_bag_weight:
                    self.bag.append(order_in_source)
        # 2.
        for order_from_list in self._order_list[1:]:
            print(f'taking {str(order_from_list)}')
            print(f' bag before action {[str(x) for x in self.bag]}')
            print('-------------------')

            # 2a
            if order_from_list in self.bag:
                for order_in_bag in self.bag:
                    if order_in_bag.id is not order_from_list.id:
                        step_length = timetable.get_path_time(path[-1].id, order_in_bag.destination.id)
                        path.append(order_in_bag.destination)
                        self.update_delivery_time(step_length)
                        cost += step_length
                        self.bag.remove(order_in_bag)
                        print('action 2a/1')
                        print(cost)

                    else:

                        step_length = timetable.get_path_time(path[-1].id, order_in_bag.destination.id)
                        path.append(order_in_bag.destination)
                        self.update_delivery_time(step_length)
                        cost += step_length
                        self.bag.remove(order_in_bag)
                        print('action 2a/2')
                        print(cost)


            # 2b
            else:
                #1
                if len(self.bag) > 0:
                    print('bag is not none')
                    for order_in_bag in self.bag:
                        order_in_bag_step_length = timetable.get_path_time(path[-1].id, order_in_bag.destination.id)
                        order_in_list_step_length = timetable.get_path_time(path[-1].id, order_from_list.source.id)
                        if order_in_bag_step_length < order_in_list_step_length:
                            path.append(order_in_bag.destination)
                            cost += order_in_bag_step_length
                            self.update_delivery_time(order_in_bag_step_length)
                            self.bag.remove(order_in_bag)
                            print('action 2b/1/1')
                            print(cost)
                        else:
                            if self.bag_weight() + order_from_list.weight < self.max_bag_weight:
                                path.append(order_from_list.source)
                                self.update_delivery_time(order_in_list_step_length)
                                cost += order_in_list_step_length
                                self.bag.append(order_from_list)
                                print('bag appended 2b/1/2')
                                print(cost)
                                for order_in_source in order_from_list.source.order_list:
                                    if order_in_source.id is not order_from_list.id:
                                        if self.bag_weight() + order_in_source.weight < self.max_bag_weight:
                                            self.bag.append(order_in_source)
                                break


                            else:
                                path.append(order_in_bag.destination)
                                cost += order_in_bag_step_length
                                self.update_delivery_time(order_in_bag_step_length)
                                self.bag.remove(order_in_bag)
                                print('bag appended 2b/1/2b')
                                print(cost)

                    if order_from_list not in self.bag:
                        order_in_list_step_length = timetable.get_path_time(path[-1].id, order_from_list.source.id)
                        path.append(order_from_list.source)
                        self.update_delivery_time(order_in_list_step_length)
                        cost += order_in_list_step_length
                        self.bag.append(order_from_list)
                        print('alternative')
                        print(cost)
                        for order_in_source in order_from_list.source.order_list:
                            if order_in_source.id is not order_from_list.id:
                                if self.bag_weight() + order_in_source.weight < self.max_bag_weight:
                                    self.bag.append(order_in_source)


                #2
                else:

                    order_in_list_step_length = timetable.get_path_time(path[-1].id, order_from_list.source.id)
                    path.append(order_from_list.source)
                    cost += order_in_list_step_length
                    self.bag.append(order_from_list)
                    print('bag appended 2b/2')
                    print(cost)
                    for order_in_source in order_from_list.source.order_list:
                        if order_in_source.id is not order_from_list.id:
                            if self.bag_weight() + order_in_source.weight < self.max_bag_weight:
                                self.bag.append(order_in_source)

            print(f'bag after action {[str(x) for x in self.bag]}')
            print([str(x) for x in path])
            print('<<<<<<<<<<step<<<<<<<<<<<')
        print(('loop end'))
        print([str(x) for x in self.bag])

        if len(self.bag) > 0:
            print('zerowanie')
            print([str(x) for x in self.bag])
            for order_in_bag in self.bag:
                order_in_bag_step_length = timetable.get_path_time(path[-1].id, order_in_bag.destination.id)
                path.append(order_in_bag.destination)
                cost += order_in_bag_step_length
                self.update_delivery_time(order_in_bag_step_length)
                print(cost)
                print([str(x) for x in self.bag])
                #self.bag.remove(order_in_bag)
                print([str(x) for x in path])
            self.bag = []
        return path, cost

    def draw_route(self, timetable, ax, index, colour='red'):
        c = 'red' if isinstance(self.get_path(timetable)[0], Restaurant) else "blue"
        ax.scatter(self.get_path(timetable)[0].cords[0], self.get_path(timetable)[0].cords[1], c=c)
        ax.annotate(str(self.get_path(timetable)[0]), (self.get_path(timetable)[0].cords[0], self.get_path(timetable)[0].cords[1]))

        for idx, point in enumerate(self.get_path(timetable)[:-1]):
            c = 'red' if isinstance(point, Restaurant) else "blue"
            ax.scatter(self.get_path(timetable)[idx+1].cords[0], self.get_path(timetable)[idx+1].cords[1], c=c)
            ax.annotate(str(self.get_path(timetable)[idx+1]), (self.get_path(timetable)[idx+1].cords[0], self.get_path(timetable)[idx+1].cords[1]))
            #draw_line(point, self.get_path(timetable)[idx+1], timetable, colour=colour,ax = ax)

        x= [i.cords[0] for i in self.get_path(timetable)]
        y= [i.cords[1] for i in self.get_path(timetable)]
        ax.plot(x,y,label=f'Courier {index}')

        return ax






