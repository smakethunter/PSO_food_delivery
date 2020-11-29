from abc import ABC
from PSO import *
from copy import deepcopy
from drawing_utils import *
from scipy.special import softmax


class DeliveryServiceGenerator:
    def __init__(self, nr_orders, nr_restaurants, nr_rows):
        self.nr_orders = nr_orders
        self.nr_restaurants = nr_restaurants
        self.nr_rows = nr_rows
        table, particle = self.generate_particle()
        self.timetable = table
        self._particle = particle

    @property
    def particle(self):
        return self._particle

    @particle.setter
    def particle(self,new_position):
        self._particle = new_position

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
        order_list = list(np.array(self._particle).flatten())

        return self.redistribute(order_list)


class DeliveryService(Particle):
    def __init__(self, nr_couriers, nr_orders, nr_restaurants):
        super(DeliveryService, self).__init__()
        self.nr_couriers = nr_couriers
        starting_position = DeliveryServiceGenerator(nr_orders, nr_restaurants, nr_couriers)
        self.best_position: List[Optional] = starting_position.particle
        self.position: List[Optional] = starting_position.particle
        self.velocity: List[Optional] = []
        self.swarm_best_position = starting_position
        self.time_table = starting_position.timetable
        self.best_fitness = self.fitness()
        self.nr_orders = nr_orders

    # TODO: implementacja ruchu
    def move(self):
        pass

    # TODO: implementacja oblicznia predkosci
    def compute_velocity(self, swarm_best: Particle, params) -> [List, np.array]:
        w, c_p, c_g = [PSO.inertia, PSO.cp, PSO.cg]
        best_position = np.array(self.best_position).flatten()
        position = np.array(self.position).flatten()
        position_ids = np.array([x.id for x in position])
        best_position_ids = np.array([x.id for x in best_position])

        p_d = []
        for best_pos, pos in zip(best_position, position):
            p_d.append(np.where(position_ids == best_pos.id)[0][0] - np.where(position_ids == pos.id)[0][0])

        mean_pd = np.mean(p_d)
        p_d = sigmoid(np.abs(p_d - mean_pd))
        p_g = [self.swarm_best_position.particle[i] - position[i] for
               i, position in
               zip(range(len(self.position)), self.position)]
        mean_pg = np.mean(p_g)
        p_g = sigmoid(np.abs(p_g - mean_pg))
        v_lk = w*self.velocity[0]+c_p*p_d+c_g*p_g
        v_lk = softmax(v_lk)
        p = np.random.uniform(size=len(v_lk))
        v_lk = [0 if v_lk[i] < p[i] else 1 for i in range(len(v_lk))]

        p_d2 = [len(self.velocity[1][i]) - len(self.best_position[i]) for i in range(len(self.velocity[1]))]
        p_g2 = [len(self.velocity[1][i]) - len(self.swarm_best_position.particle[i]) for i in range(len(self.velocity[1]))]
        v_d = w*self.velocity[1]+c_p*p_d2+c_g*p_g2

        return [v_lk, v_d]

    def fitness(self):
        fitness = 0
        for row in self.position:
            courier = Courier(row)
            fitness += courier.fitness(self.time_table)
        return fitness

    def update_best_position(self) -> None:
        if self.fitness() < self.best_fitness:
            self.best_fitness = self.fitness()
            self.best_position = self.position
        pass

    def shuffle_position(self):
        order_list = list(np.array(self.position).flatten())

        self.position = self.redistribute(order_list)

    def redistribute(self, order_list):
        np.random.shuffle(order_list)
        orders_per_particle = self.nr_orders // self.nr_couriers
        particle_starting_point = []
        for x in range(self.nr_couriers):
            if x + 1 < self.nr_couriers:
                particle_starting_point.append(order_list[x * orders_per_particle:(x + 1) * orders_per_particle])
            else:
                particle_starting_point.append(order_list[x * orders_per_particle:])
        return particle_starting_point


class DeliverySwarmGenerator:
    def __init__(self, nr_particles, nr_orders, nr_restaurants, nr_rows):
        table, swarm = self.generate_swarm(nr_particles, nr_orders, nr_restaurants, nr_rows)
        self.swarm = swarm
        self.time_table = table

    @staticmethod
    def generate_swarm(nr_particles, nr_orders, nr_restaurants, nr_rows) -> Tuple[TimeTable, List[Particle]]:
        first_particle = DeliveryService(nr_orders=nr_orders, nr_restaurants=nr_restaurants, nr_couriers=nr_rows)
        swarm = [first_particle]
        for i in range(1, nr_particles):
            next_particle = deepcopy(first_particle)
            next_particle.shuffle_position()
            swarm.append(next_particle)
        return first_particle.time_table, swarm


class DeliverySwarm(Swarm):
    def __init__(self, starting_position: DeliverySwarmGenerator):
        super().__init__(starting_position.swarm)
        self.timetable = starting_position.time_table

    def fitness(self) -> float:
        return max([x.fitness() for x in self.swarm])

    def update_position(self, particle: Particle) -> None:
        particle_fitness = particle.fitness()
        if particle_fitness < self.best_fitness:
            self.best_fitness = particle_fitness
            self.best_position = particle
        pass

    def get_best_position(self) -> Particle:
        best_particle = self.swarm[0]
        for particle in self.swarm:
            if particle.fitness() < best_particle.fitness():
                best_particle = particle
        return best_particle

