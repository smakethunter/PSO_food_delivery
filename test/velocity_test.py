import unittest
from delivery_swarm import *


class VelocityTest(unittest.TestCase):
    @staticmethod
    def test_compute_velocity(self):
        d = DeliveryService(12, 2, 3)
        s = DeliverySwarm(DeliverySwarmGenerator(3, 12, 2, 3))
        print(d.compute_velocity(s.get_best_position(), [0.5, 0.5, 0.5]))


v = VelocityTest
v.test_compute_velocity(v)
