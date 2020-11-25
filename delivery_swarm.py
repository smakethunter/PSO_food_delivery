from PSO import *
from generators import *


class DeliveryService(Particle):
    def __init__(self, nr_couriers, nr_orders, nr_restaurants):
        super(DeliveryService, self).__init__()
        self.nr_couriers = nr_couriers
        starting_position = DeliveryServiceGenerator(nr_orders, nr_restaurants, nr_couriers)
        self.best_position: List[Optional] = starting_position.particle
        self.position: List[Optional] = starting_position.particle
        self.velocity: List[Optional] = []
        self.swarm_best_position = starting_position
        self.best_fitness = self.fitness()

    # TODO: implementacja ruchu
    def move(self):
        pass
    #TODO: implementacja oblicznia predkosci
    def compute_velocity(self, swarm_best: Particle):
        pass

    def fitness(self):
        fitness = 0
        for row in self.position:
            courier = Courier(row)
            fitness += courier.fitness
        return fitness

    def update_position(self) -> None:
        if self.fitness() < self.best_fitness:
            self.best_fitness = self.fitness()
            self.best_position = self.position
        pass


class DeliverySwarm(Swarm):
    def __init__(self, starting_position: DeliverySwarmGenerator):
        super().__init__(starting_position.swarm)
        self.timetable = starting_position.time_table

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

