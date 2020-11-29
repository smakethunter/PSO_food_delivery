import matplotlib.pyplot as plt
from system import *
from delivery_service import Courier
import sys, os


class History:
    def __init__(self):
        self.history = []
        self._swarm_loss_history = []
    @property
    def swarm_loss_history(self):
        return self._swarm_loss_history

    @swarm_loss_history.setter
    def swarm_loss_history(self, loss_history):
        self._swarm_loss_history = loss_history

    def add_epoch_fitness_state(self, particles_loss):
        self.swarm_loss_history.append(particles_loss)

    def add_best_particle(self, particle):
        self.history.append(particle)

    def draw_summary(self):
        plt.plot([x.fitness() for x in self.history])

    def draw_path_search(self, timetable):
        frames = []
        fig, ax = plt.subplots()
        for delivery_service in self.history:
            i=0
            for courier_path in delivery_service.position:
                courier = Courier(courier_path)
                courier.draw_route(timetable=timetable,ax=ax,colour='red',index=i)
                i+=1
            fig.show()
            frames.append(fig)
        return frames

    def draw_particles_history(self):
        particles_history = np.array(self.swarm_loss_history)
        fig, ax = plt.subplots()
        ax.plot(particles_history)
        fig.show()




    pass


def draw_line(point, point_to, time_table, colour,ax):
    if point_to is not point:
        x = [point_to.cords[0], point.cords[0]]
        y = [point_to.cords[1], point.cords[1]]
        ax.plot(x, y, color =colour)
        f = lambda x, a, b: a * x + b
        a = (y[1] - y[0]) / (x[1] - x[0])
        b = y[0] - a * x[0]
        xhalf = (x[0] if x[0] < x[1] else x[1]) + abs(x[1] - x[0]) / 2
        distance = time_table.get_path_time(point.id, point_to.id)
        ax.annotate(f'{distance:.2f}', (xhalf, f(xhalf, a, b)))


def sigmoid(x: float, k = 1, l = 1):
    return l/(1+np.exp(-k*x))


