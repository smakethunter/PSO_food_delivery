import unittest
from PSO import PSO
from delivery_swarm import *
class MyTestCase(unittest.TestCase):
    def test_something(self):
        history = History()
        swarm = DeliverySwarm(DeliverySwarmGenerator(nr_particles=4, from_file=True, filename='test_json.txt'))
        pso = PSO(0.1, 0.1, 0.1)
        print(pso.fit(swarm, 20, history).fitness())
        history.draw_particles_history()
        history.draw_summary()

if __name__ == '__main__':
    unittest.main()
