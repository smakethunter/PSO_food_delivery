from abc import ABC, abstractmethod
from typing import List,Optional
from system import  *
from delivery_service import *


class Particle:

    @abstractmethod
    def generate_starting_position(self, initial_set):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def fitness(self):
        pass

    @abstractmethod
    def compute_velocity(self, swarm_best):
        pass

    @abstractmethod
    def update_position(self) -> None:
        pass


class ParticleGenerator:
    def __init__(self,nr_orders, nr_restaurants, nr_rows):
        self.nr_orders = nr_orders
        self.nr_restaurants = nr_restaurants
        self.nr_rows = nr_rows
        table, particle = self.generate_particle()
        self.timetable = table
        self.particle = particle
        
    def generate_particle(self) -> Tuple[TimeTable,List[List[Order]]]:
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
                order = Order(restaurants[i], client, np.random.uniform(0,18,1)[0])
                order_list.append(order)
                restaurants[i].add_order(order)
            else:
                chosen_restaurant = np.random.choice(restaurants,1)[0]
                order = Order(chosen_restaurant, client, np.random.uniform(0, 18, 1)[0])
                order_list.append(order)
                chosen_restaurant.add_order(order)

        particle_starting_point = self.redistribute(order_list)

        return TimeTable(list_of_points), particle_starting_point

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


class SwarmGenerator:
    def __init__(self, nr_particles, nr_orders, nr_restaurants, nr_rows):
        table, swarm = self.generate_swarm(nr_particles, nr_orders, nr_restaurants, nr_rows)
        self.swarm = swarm
        self.timetable = table

    @staticmethod
    def generate_swarm(nr_particles, nr_orders, nr_restaurants, nr_rows):
        first_particle = ParticleGenerator(nr_orders, nr_restaurants, nr_rows)
        swarm = [first_particle.particle]
        for i in range(1, nr_particles):
            swarm.append(first_particle.shuffle_particle())
        return first_particle.timetable, swarm



class Swarm:

    def __init__(self, starting_position):
        self.timetable = starting_position.time_table
        self.swarm: List[Particle] = starting_position.swarm
        self.best_position: Particle = self.get_best_position()
        self.best_fitness: float = self.fitness()

    def fitness(self) -> float:
        fitness = 0
        for x in self.swarm:
            fitness += x.fitness()
            return fitness
        pass

    def update_position(self) -> None:
        for particle in self.swarm:
            particle.move()
            particle.update_position()
        if self.fitness() < self.best_fitness:
            self.best_fitness = self.fitness()
            self.best_position = self.swarm
        pass

    def get_best_position(self) -> Particle:
        best_particle = self.swarm[0]
        for particle in self.swarm:
            if particle.fitness() < best_particle.fitness():
                best_particle = particle
        return best_particle


class PSO:
    def __init__(self, inertia, cp, cg):
        self._inertia = inertia
        self._cp = cp
        self._cg = cg
    
    @property
    def inertia(self):
        return self._inertia 
    
    @inertia.setter
    def inertia(self, inertia):
        self._inertia = inertia

    @property
    def cp(self):
        return self._cp

    @cp.setter
    def cp(self, cp):
        self._cp = cp

    @property
    def cg(self):
        return self._cg

    @cg.setter
    def cg(self, cg):
        self._cg = cg

    #def fit(self, swarm: Swarm):





