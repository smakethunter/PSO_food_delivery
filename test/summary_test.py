import unittest
from summary import *
class MyTestCase(unittest.TestCase):
    def test_something(self):
        run_pso_and_save_summary('test_json.txt',40,0.1,0.2, 0.3,30)
        with open('../experiments_documentation/test_json.txt','r') as file:
            data = json.load(file)
            print(data['NrChanges'])
    def test_gridsearch(self):
        test_dict = {'nr_particles':[10,20,40],'inertia':[0.1,0.2,0.5], 'cg':[0.1,0.3,0.5], 'cp':[0.1,0.3,0.5],
                     'nr_epochs':[20,40,50]}
        GridSearchPSO('test_json.txt', test_dict)


if __name__ == '__main__':
    unittest.main()
