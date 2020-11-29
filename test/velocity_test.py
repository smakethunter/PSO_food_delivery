import unittest
from delivery_swarm import *


class VelocityTest(unittest.TestCase):
    @staticmethod
    def test_compute_velocity(self):
        d = DeliveryService(3, 12, 2)
        s = DeliverySwarm(DeliverySwarmGenerator(3, 12, 2, 3))
        params = PSO(1, 1, 1) #?
        print(d.compute_velocity(s.get_best_position(), params))

v = VelocityTest
v.test_compute_velocity(v)
