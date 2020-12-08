import unittest
from summary import *
class MyTestCase(unittest.TestCase):
    def test_something(self):
        run_pso_and_save_summary('test_json.txt',40,0.1,0.2, 0.3,30)
    with open('../experiments_documentation/test_json.txt','r') as file:
        data = json.load(file)
        print(data['NrChanges'])



if __name__ == '__main__':
    unittest.main()
