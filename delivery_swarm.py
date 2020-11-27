from abc import ABC
from PSO import *
from generators import *
from drawing_utils import *
from scipy.special import softmax


class DeliveryService(Particle):
    def __init__(self, nr_couriers, nr_orders, nr_restaurants):
        super(DeliveryService, self).__init__()
        self.nr_couriers = nr_couriers
        starting_position = DeliveryServiceGenerator(nr_orders, nr_restaurants, nr_couriers)
        self.best_position: List[Optional] = starting_position.particle
        self.position: List[Optional] = starting_position.particle
        self.velocity: List[Optional] = []
        self.swarm_best_position = starting_position
        self.time_table = starting_position.timetable
        self.best_fitness = self.fitness()

    # TODO: implementacja ruchu
    def move(self):
        pass

    # TODO: implementacja oblicznia predkosci
    def compute_velocity(self, swarm_best: Particle, params) -> [List, np.array]:
        w, c_p, c_g = params

        p_d = [best_position[i][0].id - position[i][0].id for
               i, best_position, position in
               zip(range(max(len(self.best_position), len(self.position))-1), self.best_position, self.position)]
        mean_pd = np.mean(p_d)
        p_d = sigmoid(np.abs(p_d - mean_pd))
        p_g = [self.swarm_best_position.particle[i] - position[i] for
               i, position in
               zip(range(len(self.position)), self.position)]
        mean_pg = np.mean(p_g)
        p_g = sigmoid(np.abs(p_g - mean_pg))
        v_lk = w*self.velocity[0]+c_p*p_d+c_g*p_g
        v_lk = softmax(v_lk)
        p = np.random.uniform(size=len(v_lk))
        v_lk = [0 if v_lk[i] < p[i] else 1 for i in range(len(v_lk))]

        p_d2 = [len(self.velocity[1][i]) - len(self.best_position[i]) for i in range(len(self.velocity[1]))]
        p_g2 = [len(self.velocity[1][i]) - len(self.swarm_best_position.particle[i]) for i in range(len(self.velocity[1]))]
        v_d = w*self.velocity[1]+c_p*p_d2+c_g*p_g2

        return [v_lk, v_d]

    def fitness(self):
        fitness = 0
        for row in self.position:
            courier = Courier(row)
            fitness += courier.fitness(self.time_table)
        return fitness

    def update_best_position(self) -> None:
        if self.fitness() < self.best_fitness:
            self.best_fitness = self.fitness()
            self.best_position = self.position
        pass


class DeliverySwarm(Swarm):
    def __init__(self, starting_position: DeliverySwarmGenerator):
        super().__init__(starting_position.swarm)
        self.timetable = starting_position.time_table

    def fitness(self) -> float:
        return max([x.fitness() for x in self.swarm])

    def update_position(self, particle: Particle) -> None:
        particle_fitness = particle.fitness()
        if particle_fitness < self.best_fitness:
            self.best_fitness = particle_fitness
            self.best_position = particle
        pass

    def get_best_position(self) -> Particle:
        best_particle = self.swarm[0]
        for particle in self.swarm:
            if particle.fitness() < best_particle.fitness():
                best_particle = particle
        return best_particle

