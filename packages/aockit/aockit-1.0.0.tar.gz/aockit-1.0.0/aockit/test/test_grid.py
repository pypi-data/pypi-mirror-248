import unittest

from aockit.grid import Grid


class TestGrid(unittest.TestCase):
    def test_get(self):
        g = Grid(5, 5, list(range(25)))

        self.assertEqual(0, g[0, 0])
        self.assertEqual(0, g.get(0, 0))

        self.assertEqual(18, g[3, 3])
        self.assertEqual(18, g.get(3, 3))

        self.assertEqual(24, g[-1, -1])
        self.assertEqual(24, g[-1, -1])

        with self.assertRaises(IndexError):
            _ = g[0, 5]
        with self.assertRaises(IndexError):
            _ = g[5, 0]

    def test_set(self):
        g = Grid(5, 5, list(range(25)))
        g[0, 0] = 15
        g.set(-1, -1, 30)

        self.assertEqual(15, g[0, 0])
        self.assertEqual(30, g[-1, -1])

    def test_col(self):
        g = Grid(5, 5, list(range(25)))

        expected = [0, 5, 10, 15, 20]
        actual = list(g.col(0))
        self.assertEqual(expected, actual)

        expected = [(0, 0, 0), (1, 0, 5), (2, 0, 10), (3, 0, 15), (4, 0, 20)]
        actual = list(g.col_indexed(0))
        self.assertEqual(expected, actual)

    def test_row(self):
        g = Grid(5, 5, list(range(25)))

        expected = [0, 1, 2, 3, 4]
        actual = list(g.row(0))
        self.assertEqual(expected, actual)

        expected = [(0, 0, 0), (0, 1, 1), (0, 2, 2), (0, 3, 3), (0, 4, 4)]
        actual = list(g.row_indexed(0))
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
