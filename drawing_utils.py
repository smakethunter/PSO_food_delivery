import matplotlib.pyplot as plt
from system import *
from delivery_swarm import *
from PSO import *
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
                courier.draw_route(timetable=timetable,ax=ax,colour='red')
            fig.show()
            frames.append(fig)
        return frames





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
