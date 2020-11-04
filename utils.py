from abc import ABC, abstractmethod
from typing import List


class Particle(ABC):
    def __init__(self, starting_position):
        self.best_position = starting_position
        self.position = starting_position
        self.velocity = self.compute_velocity()
        self.swarm_best_position = starting_position
        self.best_fitness = self.fitness()

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def fitness(self):
        pass

    @abstractmethod
    def compute_velocity(self):
        pass

    def update_position(self) -> None:
        if self.fitness() < self.best_fitness:
            self.best_fitness = self.fitness()
            self.best_position = self.position
        pass





class Swarm:

    def __init__(self, starting_position):
        self.best_position: List[Particle] = starting_position
        self.swarm: List[Particle] = starting_position
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
