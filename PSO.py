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


class Swarm:
    def __init__(self, starting_position):
        self.swarm: List[Particle] = starting_position
        self.best_position: Particle = self.get_best_position()
        self.best_fitness: float = self.fitness()

    @abstractmethod
    def fitness(self):
        pass

    @abstractmethod
    def get_best_position(self):
        pass

    @abstractmethod
    def update_position(self):
        pass

    pass


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





