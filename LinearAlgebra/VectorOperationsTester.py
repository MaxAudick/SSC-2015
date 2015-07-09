__author__ = 'max'

import unittest
import VectorOperations as Vo

class TestVectorOperations(unittest.TestCase):

    def setUp(self):
        self.matrix1 = Vo.rand_matrix(5, 5, -5, 5)
        self.matrix2 = Vo.rand_matrix(5, 1, -5, 5)
        self.identity = Vo.get_identity(5)

    def test_rand_matrix(self):
        a = self.matrix1
        self.assertTrue(len(a) == 5 and len(a[0]) == 5)
        for r in range(5):
            for val in a[r]:
                self.assertTrue(-5 <= val <= 5)

    def test_gaussian_solve(self):
        solved = Vo.gaussian_solve(self.matrix1, self.matrix2)
        solved = Vo.multiply_matrices(self.matrix1, solved)
        for i in range(5):
            self.assertAlmostEqual(solved[i][0], self.matrix2[i][0])



def main():
    unittest.main()
