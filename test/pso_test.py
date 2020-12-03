import unittest
from PSO import PSO
from delivery_swarm import *
class MyTestCase(unittest.TestCase):
    def test_something(self):

        swarm = DeliverySwarm(DeliverySwarmGenerator(nr_particles=100, from_file=True, filename='/home/smaket/PycharmProjects/PSO_food_delivery/cases/przypadek3k200z12r.txt'))
        history = History(swarm.time_table)
        pso = PSO(0.1, 0.1, 0.1)
        print(pso.fit(swarm, 50, history).fitness())
        #history.draw_particles_history()
        history.draw_loss()
        #history.draw_summary()
        #history.draw_path_search()

if __name__ == '__main__':
    unittest.main()
