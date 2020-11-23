from abc import ABC, abstractmethod
from typing import List,Optional


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


class Swarm:

    def __init__(self, starting_position):

        self.swarm: List[Particle] = starting_position
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



