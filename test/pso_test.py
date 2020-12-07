import unittest
from PSO import PSO
from delivery_swarm import *
import os
main_path = '/'.join(os.getcwd().split('/')[:-1])
best_path_dir = main_path+'/best_path_plots/'
class MyTestCase(unittest.TestCase):
    def test_something(self):

        swarm = DeliverySwarm(DeliverySwarmGenerator(nr_particles=40, from_file=True, filename='test_json.txt'))
        history = History(swarm.time_table)
        pso = PSO(0.1, 0.2, 0.2,40,history)
        print(pso.fit(swarm))
        history.draw_particles_history(main_path+'/swarm_loss_plots/'+'test.png')
        print(pso.history.time_performance)
        history.draw_loss(main_path+'/loss_history_plots/'+'test.png')
        #history.draw_path_search()
        print(pso.history.epochs_with_change)
        pso.history.draw_best_path(best_path_dir+'test.png')
        pso.to_file(main_path+'/experiments_documentation/'+'pso_json.txt')
        pso.history.draw_changes_per_epoch(main_path+'/changes_per_epoch_plots/'+'test.png')
if __name__ == '__main__':
    unittest.main()
