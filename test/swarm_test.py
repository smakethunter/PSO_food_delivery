import unittest

from pso.delivery_swarm import *
import os

wd = '/'.join(os.getcwd().split('/')[:-1])


class ParticleGeneratorTest(unittest.TestCase):
    def test_generating_particle(self):
        particle = DeliveryServiceGenerator(12, 8, 3)
        time_table, particle_ = particle.timetable, particle.particle
        time_table.draw_table()
        print([[x.id for x in f] for f in particle_])
        self.assertEqual(4, len(particle_[-1]))
        print([[x.id for x in f] for f in particle.shuffle_particle()])

        del particle

    def test_str(self):
        particle = DeliveryService(nr_couriers=3, nr_orders=200, nr_restaurants=12)
        particle.save_to_file(wd + '/cases/przypadek20k500z12r.txt')
        with open(wd + '/cases/przypadek20k500z12r.txt') as json_file:
            data = json.load(json_file)
            print(data['Orders'])

    def test_from_flie(self):
        particle = DeliveryService(from_file=True, filename='test_json.txt')


class SwarmGeneratorTest(unittest.TestCase):
    def test_generating_swarm(self):
        swarm = DeliverySwarmGenerator(3, 12, 2, 3)
        print([p for p in swarm.swarm])
        swarm.time_table.draw_table()

    def test_swarm_from_file(self):
        swarm = DeliverySwarm(DeliverySwarmGenerator(nr_particles=4, from_file=True, filename='test_json.txt'))
        swarm.time_table.draw_table()
        for particle in swarm.swarm:
            particle.compute_velocity(swarm.best_position, {'inertia': 0, 'cp': 0.5, 'cg': 0.5})
        for particle in swarm.swarm:
            particle.move(swarm.best_position)
            print(particle.velocity)


if __name__ == '__main__':
    unittest.main()
