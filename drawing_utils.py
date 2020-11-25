import matplotlib.pyplot as plt

def draw_line(point, point_to, time_table, colour):
    if point_to is not point:
        x = [point_to.cords[0], point.cords[0]]
        y = [point_to.cords[1], point.cords[1]]
        plt.plot(x, y, color =colour)
        f = lambda x, a, b: a * x + b
        a = (y[1] - y[0]) / (x[1] - x[0])
        b = y[0] - a * x[0]
        xhalf = (x[0] if x[0] < x[1] else x[1]) + abs(x[1] - x[0]) / 2
        distance = time_table.get_path_time(point.id, point_to.id)
        plt.annotate(f'{distance:.2f}', (xhalf, f(xhalf, a, b)))
class History:
    pass