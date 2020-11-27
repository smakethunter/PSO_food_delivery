import numpy as np
import matplotlib.animation as animation
from delivery_swarm import *


if __name__ == '__main__':
   lista = [[1,2,3,4],[1,2,4], [2,2,4]]
   fig,ax = plt.subplots()
   particle = DeliveryServiceGenerator(12, 8, 3)
   time_table, particle_ = particle.timetable, particle.particle
   # for row,colour in zip(particle_,['red','blue','green']):
   #    courier = Courier(row)
   #    frame = courier.draw_route(time_table, ax, colour)

   def animate(row):
      courier = Courier(row)
      colour = 'red'
      frame = courier.draw_route(time_table, ax, colour)
      return frame

   ani =animation.FuncAnimation(fig,animate,particle_)
   fig.show()








