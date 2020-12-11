from abc import ABC, abstractmethod
from typing import *
from drawing_utils import *
import time


class Particle:

    @abstractmethod
    def generate_starting_position(self, initial_set):
        pass

    @abstractmethod
    def move(self, swarm_best):
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
    def update_position(self, particle):
        pass

    pass


class PSO:
    def __init__(self, inertia, cp, cg, num_epochs, history: History = None):
        self._inertia = inertia
        self._cp = cp
        self._cg = cg
        self.history = history
        self.num_epochs = num_epochs
    
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

    def fit(self, swarm: Swarm):
        execution_performance = {}
        fit_time = time.time()
        loss_history = []
        epochs_with_change = {i:0 for i in range(1,self.num_epochs+1)}
        move_time = []
        compute_velocity_time=[]
        epoch_time = []
        update_position_time = []
        for i in range(self.num_epochs):
            particles_fitness=[]
            epoch_start = time.time()

            for particle in swarm.swarm:

                velocity_start = time.time()
                particle.compute_velocity(swarm.best_position,
                                          {'inertia': self.inertia, 'cp': self.cp, 'cg': self.cg})
                compute_velocity_time.append(-velocity_start+time.time())
                move_start = time.time()
                particle.move(swarm.best_position)
                move_time.append(-move_start+time.time())
                update_position_start = time.time()
                particle.update_best_position()
                update_position_time.append(time.time()-update_position_start)
                if swarm.update_position(particle):
                    epochs_with_change[i+1] +=1
                particles_fitness.append(particle.fitness())
            epoch_time.append(-epoch_start+time.time())
            if self.history is not None:
                self.history.add_best_particle(swarm.best_position)

            if self.history is not None:
                self.history.add_epoch_fitness_state(particles_fitness)
            loss_history.append(swarm.best_position.fitness())


        execution_performance['PSO_time'] = -fit_time + time.time()
        execution_performance['avg_v_computation'] = sum(compute_velocity_time)/len(compute_velocity_time)
        execution_performance['avg_move_time'] = sum(move_time)/len(move_time)
        execution_performance['avg_epoch_time'] = sum(epoch_time)/len(epoch_time)
        execution_performance['avg_fitness_calculation_time'] = sum(update_position_time)/len(update_position_time)
        if self.history is not None:
            self.history.best_history = loss_history
            self.history.epochs_with_change = epochs_with_change
            self.history.time_performance = execution_performance
        return swarm.best_position

    def to_file(self, filename=None):
        nr_changes = 0
        for _,v in self.history.epochs_with_change.items():
            nr_changes+=v
        output = {'TimeScore' : self.history.time_performance, 'Loss' : self.history.swarm_loss_history[-1],
                  'EpochsWithChange': self.history.epochs_with_change,'NrChanges': nr_changes, 'PSO_Parameters':{'inertia': self.inertia,
                                                                                         'cp': self.cp, 'cg':self.cg,
                                                                                         'n_epochs':self.num_epochs},
                  'BestPath': [[order.id for order in courier.order_list] for courier in self.history.history[-1]]}
        with open(filename, 'w') as file:
            json.dump(output, file)








