import matplotlib.pyplot as plt
from system import *
from delivery_service import Courier
import json
class History:
    def __init__(self,timetable):
        self.history = []
        self._swarm_loss_history = []
        self.best_history = []
        self.timetable = timetable
        self._epochs_with_change = []
        self._time_performance = {}
        self._mobility =[]

    @property
    def mobility(self):
        return self._mobility

    @mobility.setter
    def mobility(self, loss_history):
        self._mobility = loss_history
    @property
    def time_performance(self):
        return self._time_performance

    @time_performance.setter
    def time_performance(self, loss_history):
        self._time_performance = loss_history
    @property
    def epochs_with_change(self):
        return self._epochs_with_change

    @epochs_with_change.setter
    def epochs_with_change(self, loss_history):
        self._epochs_with_change = loss_history
        
    @property
    def swarm_loss_history(self):
        return self._swarm_loss_history

    @swarm_loss_history.setter
    def swarm_loss_history(self, loss_history):
        self._swarm_loss_history = loss_history


    def add_epoch_fitness_state(self, particles_loss):
        self.swarm_loss_history.append(particles_loss)

    def add_best_particle(self, particle):
        couriers = []
        for courier_path in particle.position:
            couriers.append(Courier(courier_path))
            self.history.append(couriers)

    # def draw_summary(self):
    #     figure = plt.figure()
    #     plt.plot([sum([x.fitness(self.timetable) for x in courier]) for courier in self.history])
    #     plt.xlabel('Iteracja')
    #     plt.ylabel('Wartość funkcji kosztu')
    #     plt.title('Zmiana wartości funkcji kosztu w liczbie iteracji')
    #     figure.show()
    def draw_path_search(self,filename = None):
        frames = []
        fig, ax = plt.subplots()
        for delivery_service in self.history:
            i=0
            for courier in delivery_service:
                courier.draw_route(timetable=self.timetable,ax=ax,colour='red',index=i)
                i+=1
            fig.show()
            frames.append(fig)
            if filename is not None:
                fig.savefig(filename)
        return frames
    def draw_best_path(self, filename = None):
        fig, ax = plt.subplots()
        i=0
        for courier in self.history[-1]:
            courier.draw_route(timetable=self.timetable, ax=ax, colour='red', index=i)
            i += 1
        fig.show()
        if filename is not None:
            fig.savefig(filename)



    def draw_particles_history(self, filename = None):
        particles_history = np.array(self.swarm_loss_history)
        fig, ax = plt.subplots()
        ax.set(title='Zmiana funkcji kosztu dla wszyskich osobników')
        ax.set(xlabel='Iteracja')
        ax.set(ylabel='Wartość funkcji kosztu')
        ax.plot(particles_history)
        fig.show()
        if filename is not None:
            fig.savefig(filename)
    def draw_avg_swarm_loss(self,filename = None):
        particles_history = np.array(self.swarm_loss_history)
        average = np.average(particles_history,axis=1)
        fig, ax = plt.subplots()
        ax.set(title='Średnia zmiana funkcji kosztu dla wszyskich osobników')
        ax.set(xlabel='Iteracja')
        ax.set(ylabel='Średnia wartość funkcji kosztu')
        ax.plot(average)
        fig.show()
        if filename is not None:
            fig.savefig(filename)
    def draw_loss(self, filename = None):
        fig = plt.figure()
        plt.plot(self.best_history)
        plt.title('Zmiana wartości funkcji kosztu')
        plt.xlabel('Iteracja')
        plt.ylabel('Wartość funkcji kosztu')
        fig.show()
        if filename is not None:
            fig.savefig(filename)

    def draw_changes_per_epoch(self,filename = None):
        fig = plt.figure()
        height = []
        x = []
        for k,v in self.epochs_with_change.items():
            x.append(k)
            height.append(v)
        plt.title('Liczba zmian najlepszego osobnika')
        plt.ylabel('Liczba zmian')
        plt.xlabel('Iteracja')
        plt.bar(x,height)
        plt.xticks([i+1 for i in range(len(self.epochs_with_change))])
        fig.show()
        if filename is not None:
            fig.savefig(filename)
    def draw_mobility_per_epoch(self,filename):
        fig = plt.figure()
        plt.plot(self._mobility)
        plt.title('Ruchliwosc roju')
        plt.xlabel('Iteracja')
        plt.ylabel('Ruchliwość')
        fig.show()
        if filename is not None:
            fig.savefig(filename)




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
