from abc import ABC, abstractmethod
from typing import List,Optional
from delivery_service import *
from system import *


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
    def compute_velocity(self, swarm_best, params):
        pass

    @abstractmethod
    def update_best_position(self):
        pass


class Swarm:
    def __init__(self, starting_position_swarm):
        self.swarm: List[Particle] = starting_position_swarm
        self.best_fitness: float = self.fitness()
        self.best_position: Particle = self.get_best_position()

    @abstractmethod
    def fitness(self):
        pass

    @abstractmethod
    def get_best_position(self):
        pass

    @abstractmethod
    def update_position(self, particle):
        pass

    pass


class History:
    def __init__(self):
        self.history = []

    def add_particle(self, particle):
        self.history.append(particle)

    def draw_summary(self):
        plt.plot([x.fitness() for x in self.history])

    def draw_path_search(self, timetable):
        frames = []
        fig, ax = plt.subplots()
        for delivery_service in self.history:
            for courier_path in delivery_service.position:
                courier = Courier(courier_path)
                courier.draw_route(timetable=timetable, ax=ax, colour='red')
            fig.show()
            frames.append(fig)
        return frames


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

    def fit(self, swarm: Swarm, num_epochs, history: History = None):

        for i in range(num_epochs):
            for particle in swarm.swarm:
                particle.compute_velocity(swarm.best_position,
                                          {'inertia': self.inertia, 'cp': self.cp, 'cg': self.cg})
                particle.move()
                particle.update_best_position()
                swarm.update_position(particle)
            if history is not None:
                history.add_particle(swarm.best_position)

        return swarm.best_position









