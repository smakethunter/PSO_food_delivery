from system import *

class DeliveryServiceGenerator:
    def __init__(self, nr_orders, nr_restaurants, nr_rows):
        self.nr_orders = nr_orders
        self.nr_restaurants = nr_restaurants
        self.nr_rows = nr_rows
        table, particle = self.generate_particle()
        self.timetable = table
        self.particle = particle

    def generate_particle(self):
        list_of_points = []
        restaurants = []
        for r in range(self.nr_restaurants):
            restaurant = Restaurant()
            restaurants.append(restaurant)
            list_of_points.append(restaurant)

        order_list = []

        for i in range(self.nr_orders):
            client = Client()
            list_of_points.append(client)
            if i < self.nr_restaurants:
                order = Order(restaurants[i], client, np.random.uniform(0, 18, 1)[0])
                order_list.append(order)
                restaurants[i].add_order(order)
            else:
                chosen_restaurant = np.random.choice(restaurants, 1)[0]
                order = Order(chosen_restaurant, client, np.random.uniform(0, 18, 1)[0])
                order_list.append(order)
                chosen_restaurant.add_order(order)

        particle_starting_point = self.redistribute(order_list)
        timetable = TimeTable(list_of_points)

        return timetable, particle_starting_point

    def redistribute(self, order_list):
        np.random.shuffle(order_list)
        orders_per_particle = self.nr_orders // self.nr_rows
        particle_starting_point = []
        for x in range(self.nr_rows):
            if x + 1 < self.nr_rows:
                particle_starting_point.append(order_list[x * orders_per_particle:(x + 1) * orders_per_particle])
            else:
                particle_starting_point.append(order_list[x * orders_per_particle:])
        return particle_starting_point

    def shuffle_particle(self):
        order_list = list(np.array(self.particle).flatten())

        return self.redistribute(order_list)


class DeliverySwarmGenerator:
    def __init__(self, nr_particles, nr_orders, nr_restaurants, nr_rows):
        table, swarm = self.generate_swarm(nr_particles, nr_orders, nr_restaurants, nr_rows)
        self.swarm = swarm
        self.time_table = table

    @staticmethod
    def generate_swarm(nr_particles, nr_orders, nr_restaurants, nr_rows):
        first_particle = DeliveryServiceGenerator(nr_orders, nr_restaurants, nr_rows)
        swarm = [first_particle.particle]
        for i in range(1, nr_particles):
            swarm.append(first_particle.shuffle_particle())
        return first_particle.timetable, swarm

