
from delivery_swarm import *

lista = [[1, 2, 3, 4]]
fig, ax = plt.subplots()
particle = DeliveryServiceGenerator(8, 4, 2)
time_table, particle_ = particle.timetable, particle.particle
colours = np.random.uniform(0,1,(len(particle_),3))
i=0

for row, colour in zip(particle_, colours):
      courier = Courier(row)
      courier.draw_route(time_table, ax, colour=colour, index=i)
      i += 1
ax.legend()
fig.show()
if __name__ == '__main__':
      s = '[40.08081730912971, 14.748012543556257]'
def str_to_float_array(s):
      s=s.lstrip('[')
      s=s.rstrip(']')
      s=s.split(',')
      return [float(x) for x in s]







