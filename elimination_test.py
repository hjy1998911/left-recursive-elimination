import unittest

from leftrecursiveelimination import eliminateLeftRecursive

class MyTestCase(unittest.TestCase):
    def test_left_recursive_elimination(self):
        eliminateLeftRecursive("./production")

    def test_expression_elimination(self):
        eliminateLeftRecursive("./expression", "./expression.out")
if __name__ == '__main__':
    unittest.main()
