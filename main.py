
from delivery_swarm import *
from drawing_utils import History
if __name__ == '__main__':
      history = History()
      for i in range(10):
         xd = list(np.random.uniform(0,10,3))
         print(xd)
         history.add_epoch_fitness_state(xd)
      history.draw_particles_history()









