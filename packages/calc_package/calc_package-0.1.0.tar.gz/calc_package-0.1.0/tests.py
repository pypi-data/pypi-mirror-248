import unittest
from src.calc_package.mycounter import Calculator

calc = Calculator()

class TestAlgebra(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(calc.add(2, 3), 5, 'Answer should be 5')

    def test_sub(self):
        self.assertEqual(calc.sub(10, 2), 8, 'Answer should be 8')

    def test_mul(self):
        self.assertEqual(calc.mul(5, 6), 30, 'Answer should be 30')

    def test_div(self):
        self.assertEqual(calc.div(10, 2), 5, 'Answer should be 5')

    def test_roo(self):
        self.assertEqual(calc.roo(36, 2), 6, 'Answer should be 6')

    def test_memory(self):
        result = calc.add(6, 4)
        self.assertEqual(calc.memory, result, 'Answer should be 10')

if __name__ == '__main__':
    unittest.main()