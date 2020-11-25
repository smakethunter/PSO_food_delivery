import unittest
from generators import *


class ParticleGeneratorTest(unittest.TestCase):
    def test_generating_particle(self):
        particle = DeliveryServiceGenerator(12,8,3)
        time_table, particle_ = particle.timetable, particle.particle
        time_table.draw_table()
        print([[x.id for x in f] for f in particle_])
        self.assertEqual(4,len(particle_[-1]))
        print([[x.id for x in f] for f in particle.shuffle_particle()])
        del particle

class SwarmGeneratorTest(unittest.TestCase):
    def test_generating_swarm(self):
        swarm = DeliverySwarmGenerator(3,12,2,3)
        print([[[x.id for x in p] for p in particle] for particle in swarm.swarm])
        swarm.time_table.draw_table()




if __name__ == '__main__':
    unittest.main()
