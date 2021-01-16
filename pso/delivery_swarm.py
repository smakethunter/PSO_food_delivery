import json

from pso.PSO import *
from pso.delivery_service import *
# from system import *
from copy import deepcopy


def flatten(array):
    """

    :param array: N-dimensional array to flatten
    :return: flattened array
    """
    new_array = []
    for x in array:
        new_array.extend(x)
    return new_array


def str_to_float_array(s):
    s = s.lstrip('[')
    s = s.rstrip(']')
    s = s.split(',')
    return [float(x) for x in s]


def sigmoid(x):
    return 1 / (1 + np.exp(-(x - np.median(x))))


def change_with_parameter(comparision, parameter):
    """
    Changes  1's in array `comparision` to 0's randomly, number of 1's to change is given by
    round((1-parameter)*(number of 1's))
    :param comparision: array with 0s and 1s
    :param parameter: what fracton of amount of 1s have to be left unchanged
    :return: changed array
    """
    to_change = list(np.where(comparision != 0)[0])
    nr_positions_to_change = int(np.round((1 - parameter) * len(to_change)))
    positions_to_change = []
    for i in range(nr_positions_to_change):
        pos = np.random.choice(to_change, 1)[0]
        positions_to_change.append(pos)
        to_change.remove(pos)

    to_change = list(int(x) for x in positions_to_change)
    for i in to_change:
        comparision[i] = 0

    return comparision


def get_v(xp, pb, parameter):
    """
    Return positions to be changed in xp elements position according to positions of same elements in pb array
    :param xp: array to modify
    :param pb: array to compare
    :param parameter: level of trust used in `change_with_parameter` function
    :return: array of 1's and 0's informing if the element on this position should be swapped or not
    """
    difference = np.zeros(len(pb))
    for i, x in enumerate(xp):
        difference[i] = (i - (np.where(pb == x)[0]))

    difference = sigmoid(abs(difference))

    boolean = np.random.uniform(0, 1, len(xp))
    comparsion = np.less_equal(boolean, difference).astype(int)

    return change_with_parameter(comparsion, parameter)


def get_distribution(difference, parameter):
    """
    Redistribute elements among list of lists according to difference and parameter
    :param difference: difference between target and source array
    :param parameter: level of trust
    :return:
    """
    difference = sigmoid(abs(difference))

    boolean = np.random.uniform(0, 1, len(difference))
    comparsion = np.less_equal(boolean, difference).astype(int)

    return change_with_parameter(comparsion, parameter)


def LK_swap(origin, target, bool_table):
    """
    Applies LK-swap of the origin taking target on account
    :param origin: array to modify
    :param target: array to compare
    :param bool_table: array determining weather to compare given index of the arrays or not
    :return: modified array
    """
    target_to_swap = np.where(bool_table == 1)[0]
    for t in target_to_swap:
        for i, x in enumerate(origin):
            if x.id == target[t].id:
                origin[t], origin[i] = origin[i], origin[t]

    return origin


class DeliveryServiceGenerator:
    def __init__(self, nr_orders: int = None, nr_restaurants: int = None, nr_rows: int = None, from_file: bool = False,
                 filename: str = None) -> None:
        """

        :param nr_orders: number of orders to handle
        :param nr_restaurants: umber of restaurants engaged
        :param nr_rows: number of couriers in delivery service
        :param from_file: If True the DeliveryService will be generated from json file provided in `filename`,
        if False DeliveryService will be generated randomly based on parameters above
        :param filename: json file containing info about parameters
        """

        if from_file:

            with open( filename) as json_file:
                data = json.load(json_file)

        self.nr_orders: int = nr_orders if nr_orders is not None else data['nr_orders']
        self.nr_restaurants: int = nr_restaurants if nr_restaurants is not None else data['nr_restaurants']
        self.nr_rows: int = nr_rows if nr_orders is not None else data['nr_rows']
        table, particle = self.generate_particle(from_file, filename)
        self.timetable: TimeTable = table
        self._particle: List[Order] = particle

        pass

    @property
    def particle(self):
        return self._particle

    @particle.setter
    def particle(self, new_position):
        self._particle = new_position

    def generate_particle(self, from_file: bool = False, filename: str = None) -> Tuple[TimeTable, List[List[Order]]]:
        """
        Generates particle based on provided parameters in `self` or from file
        :param from_file: If the order list is generated from file specified in `filename` or from `self` attributes
        :param filename: json file containing info about parameters
        :return: timetable and list of orders
        """
        list_of_points = []
        restaurant_list = []
        order_list = []
        if from_file:
            with open(filename) as json_file:
                data = json.load(json_file)
                restaurants = data['Restaurants']
                orders = data['Orders']
                clients = data['Clients']

                for r in restaurants:
                    cords = str_to_float_array(r['cords'])

                    restaurant = Restaurant(id=int(r['id']), restaurant_id=int(r['restaurant_id']), cords=cords)
                    restaurant_list.append(restaurant)
                    list_of_points.append(restaurant)

                for o in orders:
                    client = None
                    for c in clients:
                        if c['id'] == o['destination']:
                            cords = str_to_float_array(c['cords'])
                            client = Client(int(c['id']), int(c['client_id']), cords=cords)
                            list_of_points.append(client)

                    for r in restaurant_list:
                        if r.id == int(o['source']):
                            order = Order(r, client, float(o['weight']), int(o['id']))
                            r.add_order(order)
                            order_list.append(order)

                particle_starting_point = self.redistribute(order_list, shuffle=False)
        else:

            for r in range(self.nr_restaurants):
                restaurant = Restaurant()
                restaurant_list.append(restaurant)
                list_of_points.append(restaurant)

            for i in range(self.nr_orders):
                client = Client()
                list_of_points.append(client)
                if i < self.nr_restaurants:
                    order = Order(restaurant_list[i], client, np.random.uniform(0, 18, 1)[0])
                    order_list.append(order)
                    restaurant_list[i].add_order(order)
                else:
                    chosen_restaurant = np.random.choice(restaurant_list, 1)[0]
                    order = Order(chosen_restaurant, client, np.random.uniform(0, 18, 1)[0])
                    order_list.append(order)
                    chosen_restaurant.add_order(order)

            particle_starting_point = self.redistribute(order_list)
        timetable = TimeTable(list_of_points)
        return timetable, particle_starting_point

    def redistribute(self, order_list: List[Order], shuffle: bool = True) -> List[List[Order]]:
        """
        Apply random size-equal distribution of orders among couriers
        :param order_list: 1D array of `Orders`
        :param shuffle: if order list is to be shuffled
        :return: random size-equal distribution of orders among couriers List of Lists
        """
        if shuffle:
            np.random.shuffle(order_list)
        orders_per_particle = self.nr_orders // self.nr_rows
        particle_starting_point = []
        for x in range(self.nr_rows):
            if x + 1 < self.nr_rows:
                particle_starting_point.append(order_list[x * orders_per_particle:(x + 1) * orders_per_particle])
            else:
                particle_starting_point.append(order_list[x * orders_per_particle:])
        return particle_starting_point

    def shuffle_particle(self) -> List[List[Order]]:
        """
        Aplly redistributing for N-dimensional array
        :return: random size-equal distribution of orders among couriers List of Lists
        """
        order_list = list(np.array(self._particle).flatten())

        return self.redistribute(order_list)


class DeliveryService(Particle):
    def __init__(self, nr_couriers: int = None, nr_orders: int = None, nr_restaurants: int = None,
                 from_file: bool = False, filename: str = None):
        """
                Initialize Delivery service object from file or using `DeliveryServiceGenerator`
                :param nr_orders: number of orders to handle
                :param nr_restaurants: umber of restaurants engaged
                :param nr_couriers: number of couriers in delivery service
                :param from_file: If True the DeliveryService will be generated from json file provided in `filename`,
                if False DeliveryService will be generated randomly based on parameters above
                :param filename: json file containing info about parameters
        """
        super(DeliveryService, self).__init__()

        starting_position = DeliveryServiceGenerator(nr_orders, nr_restaurants, nr_couriers, from_file=from_file,
                                                     filename=filename)
        self.nr_couriers = nr_couriers if nr_couriers is not None else starting_position.nr_rows
        self.best_position: List[Optional] = starting_position.particle
        self.position: List[Optional] = starting_position.particle
        self.time_table = starting_position.timetable
        self.best_fitness = self.fitness()
        self.nr_orders = nr_orders if nr_orders is not None else starting_position.nr_orders
        self.velocity = {'v_lk': np.zeros((2, self.nr_orders)), 'v_d': np.zeros(self.nr_couriers)}
        self.nr_restaurants = starting_position.nr_restaurants
        del starting_position

    def move(self, swarm_best: Particle) -> None:
        """
        Applies particle movement meant as change if delivery order, and redistributing orders among couriers based on
         velocity calculated using `self.compute_velocity()` method. Change orders using LK - swapping
         and random change in distribution using bool vector `self.velocity['v_d']`
        :param swarm_best: best swarm position one of two targets for LK - swapping,together with `self.best_position`
        Algorithm details: https://docs.google.com/document/d/1lzUxZjcf3DzIbYNxZNsbLj9RVE_VxoxeMv6Tvu__2jo
        """
        origin = np.array([x for x in flatten(self.position)])
        target_p = np.array([x for x in flatten(self.best_position)])
        target_g = np.array([x for x in flatten(swarm_best.position)])
        origin = LK_swap(origin, target_p, self.velocity['v_lk'][0])
        origin = LK_swap(origin, target_g, self.velocity['v_lk'][1])
        position_distribution = (np.array([len(x) for x in self.position]) + self.velocity['v_d']).astype(int)
        position = []
        position_sum = 0
        for i, x in enumerate(position_distribution):
            position.append(list(origin[position_sum:position_sum + x]))
            position_sum += x
        self.position = position
        pass

    def compute_velocity(self, swarm_best: Particle, params: Dict[str, float]) -> None:
        """
        Computes velocity meant as changes(LK - swapping and redistribution) to be applied to current state of the object
        based on `swarm best` and `self.best` positions assessed using fitness() method for each particle
        :param swarm_best: best position in the whole `DeliverySwarm`
        :param params: Dictionary containing PSO parameters (`inertia`, `cp`,`cg`) referring to 'the level of trust'
        for `self_velocity`, `self.best_position`, `swarm_best` respectively, while computing new velocity.
        Algorithm details: https://docs.google.com/document/d/1lzUxZjcf3DzIbYNxZNsbLj9RVE_VxoxeMv6Tvu__2jo
        """
        inertia, cp, cg = params['inertia'], params['cp'], params['cg']
        particle_position_ids = np.array([x.id for x in flatten(self.position)])
        particle_best_position_ids = np.array([x.id for x in flatten(self.best_position)])
        swarm_best_position_ids = np.array([x.id for x in flatten(swarm_best.position)])

        def ints_to_ones(x):
            return 0 if x < 1 else 1

        v_lk = np.vstack([[ints_to_ones(x) for x in change_with_parameter(self.velocity['v_lk'][0, :], inertia) +
                           get_v(particle_position_ids, particle_best_position_ids, cp)],
                          [ints_to_ones(x) for x in change_with_parameter(self.velocity['v_lk'][1, :], inertia) +
                           get_v(particle_position_ids, swarm_best_position_ids, cg)]])

        position_distribution = np.array([len(x) for x in self.position])
        best_position_distribution = np.array([len(x) for x in self.best_position])
        swarm_best_distribution = np.array([len(x) for x in swarm_best.position])
        position_best_dist_difference = position_distribution - best_position_distribution
        swarm_position_dist_difference = position_distribution - swarm_best_distribution
        pb_change = get_distribution(position_best_dist_difference, cp)
        pg_change = get_distribution(swarm_position_dist_difference, cg)

        def diff_bool(x):
            return np.array([-1 if i < 0 else 1 for i in x])

        v_dp = pb_change * diff_bool(position_best_dist_difference)

        v_dg = pg_change * diff_bool(swarm_position_dist_difference)

        v_d = change_with_parameter(self.velocity['v_d'], inertia) + v_dp + v_dg

        v_d_plus = list(np.where(v_d > 0)[0])

        v_d_minus = list(np.where(v_d < 0)[0])

        difference_p = len(v_d_plus) - len(v_d_minus)

        if difference_p < 0:
            for i in range(abs(difference_p)):
                remove_idx = np.random.choice(v_d_minus)
                v_d[remove_idx] = 0
                v_d_minus.remove(remove_idx)
        if difference_p > 0:
            for i in range(abs(difference_p)):
                remove_idx = np.random.choice(v_d_plus)
                v_d[remove_idx] = 0
                v_d_plus.remove(remove_idx)
        self.velocity = {'v_lk': v_lk, 'v_d': v_d}

    def fitness(self) -> float:
        """
        Calculates the entire DeliveryService meaning all couriers fitness summed up.
        :return: fitness - the value cost function of all couriers in DeliveryService.
        """
        fitness = 0
        for row in self.position:
            courier = Courier(row)
            fitness += courier.fitness(self.time_table)
        return fitness

    def update_best_position(self) -> bool:
        """
        Checks if actual position is the best position and applies changes to `self.best_position` if true
        :return: If the hypothesis is true or false
        """
        if self.fitness() < self.best_fitness:
            self.best_fitness = self.fitness()
            self.best_position = self.position
            return True
        else:
            return False
        pass

    def shuffle_position(self):
        """
                Aplly redistributing for N-dimensional array
                :return: random size-equal distribution of orders among couriers List of Lists
        """
        order_list = flatten(self.position)

        self.position = self.redistribute(order_list)

    def redistribute(self, order_list, shuffle=True):
        """
                Apply random size-equal distribution of orders among couriers
                :param order_list: 1D array of `Orders`
                :param shuffle: if order list is to be shuffled
                :return: random size-equal distribution of orders among couriers List of Lists
        """
        if shuffle:
            np.random.shuffle(order_list)
        orders_per_particle = self.nr_orders // self.nr_couriers
        particle_starting_point = []
        for x in range(self.nr_couriers):
            if x + 1 < self.nr_couriers:
                particle_starting_point.append(order_list[x * orders_per_particle:(x + 1) * orders_per_particle])
            else:
                particle_starting_point.append(order_list[x * orders_per_particle:])
        return particle_starting_point

    def save_to_file(self, filename: str = None):
        """
        Saves object structure to file
        :param filename: name of the file to save the object to

        """

        orders: List[Order] = flatten(self.position)
        restaurants = set([order.source for order in orders])
        clients = set([order.destination for order in orders])
        output = {'nr_rows': self.nr_couriers, 'nr_orders': len(orders), 'nr_restaurants': len(restaurants),
                  'Orders': [o.dict() for o in orders], 'Restaurants': [r.dict() for r in restaurants],
                  'Clients': [c.dict() for c in clients]}

        with open('../cases/'+filename, 'w') as outfile:
            json.dump(output, outfile)
        del orders
        del restaurants
        del clients


class DeliverySwarmGenerator:
    def __init__(self, nr_particles: int, nr_orders:int = None, nr_restaurants: int = None,
                 nr_rows:int = None, from_file: bool = False, filename: str = None):
        """
        Generates `DeliverySwarm` from file or randomly generating `DeliverySwarm` and randomly
        Shuffling initial position getting new particles
        :param nr_particles: Number of Particles in swarm
        param nr_orders: number of orders to handle
        :param nr_restaurants: umber of restaurants engaged
        :param nr_rows: number of couriers in delivery service
        :param from_file: If True the DeliveryService will be generated from json file provided in `filename`,
        if False DeliveryService will be generated randomly based on parameters above
        :param filename: json file containing info about parameters

        """
        table, swarm = self.generate_swarm(nr_particles, nr_orders, nr_restaurants, nr_rows, from_file, filename)
        self.swarm = swarm
        self.time_table = table

    @staticmethod
    def generate_swarm(nr_particles: int, nr_orders:int = None, nr_restaurants: int = None, nr_rows: int = None,
                       from_file:bool = False, filename: str = None) -> Tuple[TimeTable, List[Particle]]:
        """
                Generates `DeliverySwarm` from file or randomly generating `DeliverySwarm` and randomly
                Shuffling initial position getting new particles
                :param nr_particles: Number of Particles in swarm
                :param nr_orders: number of orders to handle
                :param nr_restaurants: umber of restaurants engaged
                :param nr_rows: number of couriers in delivery service
                :param from_file: If True the DeliveryService will be generated from json file provided in `filename`,
                if False DeliveryService will be generated randomly based on parameters above
                :param filename: json file containing info about parameters

        """
        first_particle = DeliveryService(nr_orders=nr_orders, nr_restaurants=nr_restaurants, nr_couriers=nr_rows,
                                         from_file=from_file, filename=filename)
        swarm = [first_particle]
        for i in range(1, nr_particles):
            next_particle = deepcopy(first_particle)
            next_particle.shuffle_position()
            swarm.append(next_particle)
        return first_particle.time_table, swarm


class DeliverySwarm(Swarm):
    def __init__(self, starting_position: DeliverySwarmGenerator) -> None:
        """
        Generate Sarm using `DeliverySwarmGenerator` injected to constructor
        :param starting_position: `DeliverySwarmGenerator` injected to constructor
        """
        super().__init__(starting_position.swarm)
        self.time_table = starting_position.time_table

    def fitness(self) -> float:
        """

        :return: Swarm best fitness
        """
        fitness = 0
        return min([x.fitness() for x in self.swarm])

        pass

    def update_position(self, particle: Particle) -> bool:
        """
        Applies change to best fitness if fitness of  a given particle is better than `self.best_fitness`
        :param particle: particle to compare
        :return: if true or false
        """
        particle_fitness = particle.fitness()
        if particle_fitness < self.best_fitness:
            self.best_fitness = particle_fitness
            self.best_position = particle
            return True
        else:
            return False
        pass

    def get_best_position(self) -> Particle:
        """

        :return: best position in swarm
        """
        best_particle = self.swarm[0]
        for particle in self.swarm:
            if particle.fitness() < best_particle.fitness():
                best_particle = particle
        return best_particle
