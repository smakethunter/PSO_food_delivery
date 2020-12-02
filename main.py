
from delivery_swarm import *
import numpy as np
from scipy.special import softmax,expit
if __name__ == '__main__':
      def sigmoid(x):
            return 1/(1+np.exp(-(x-np.median(x))))

      partilce_position_ids = np.array([x for x in range(10)])
      particle_best_position_ids = deepcopy(partilce_position_ids)
      np.random.shuffle(particle_best_position_ids)

      difference=np.zeros(len(particle_best_position_ids))
      for i,x in enumerate(partilce_position_ids):
            difference[i]=(i-np.where(particle_best_position_ids == x)[0])
      difference=sigmoid(abs(difference))
      boolean = np.random.uniform(0, 1, len(partilce_position_ids))
      comparsion = np.less_equal(boolean, difference).astype(int)
      to_change = np.where(comparsion == 1)

      nr_positions_to_change = int(np.round((1 - 0.8) * len(to_change[0])))


      index_to_change = np.random.choice(comparsion, int(nr_positions_to_change))

      for i in index_to_change:
            comparsion[i] = 0
      print(comparsion)





