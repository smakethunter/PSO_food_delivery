from abc import ABC, abstractmethod
from typing import List


class Particle(ABC):

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def fitness(self):
        pass




class Swarm:

    def __init__(self, starting_position):
        self.best_position = starting_position
        self.swarm: List[Particle] = starting_position
        self.fitness = self.fitness()

    def fitness(self):
        fitness = 0
        for x in self.swarm:
            fitness += x.fitness()
            return fitness
        pass
