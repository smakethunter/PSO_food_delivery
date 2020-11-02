from abc import ABC, abstractmethod
from typing import List


class Individual(ABC):
    @abstractmethod
    def pair(self):
        pass

    @abstractmethod
    def mutate(self):
        pass

    @abstractmethod
    def fitness(self):
        pass
    pass


class Population:
    def __init__(self, _population: List[Individual]):
        self.population = _population

    def get_parents(self, nr_offsprings):
        self.population.sort(key=lambda x: x.fitness())
        mothers = self.population[len(self.population)-2*nr_offsprings: len(self.population)-nr_offsprings]
        fathers = self.population[len(self.population)-nr_offsprings::]
        return [(mother, father) for mother, father in zip(mothers, fathers)]
        pass

    def change_population(self, nr_offspring):

        pass

    pass


class Evolution:
    def make_offspring(self):
        pass

    def evolution_step(self):
        pass
    pass

