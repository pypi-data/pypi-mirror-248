import unittest
from pathlib import Path

from aockit import inputs

asset_path = Path(__file__).parent.joinpath('assets')


class TestInputs(unittest.TestCase):
    def test_string_inputs(self):
        path = asset_path.joinpath('input_strings.txt')

        expected = ['foo', 'bar', 'baz', 'bap']
        actual = list(inputs.read_strings(path))
        self.assertEqual(expected, actual, 'Should skip blank lines by default')

        expected = ['foo', 'bar', '', 'baz', 'bap']
        actual = list(inputs.read_strings(path, include_blank_lines=True))
        self.assertEqual(expected, actual, 'Should include blank lines when specified')

        expected = ['foo\n', 'bar\n', '\n', 'baz\n', 'bap\n']
        actual = list(inputs.read_strings(path, include_blank_lines=True, strip=False))
        self.assertEqual(expected, actual, 'Should prevent stripping when specified')

    def test_int_inputs(self):
        path = asset_path.joinpath('input_ints.txt')

        expected = [1000, 2000, 3000, 4000, 5000]
        actual = list(inputs.read_ints(path))
        self.assertEqual(expected, actual, 'Should parse integers')

    def test_custom_parser(self):
        path = asset_path.joinpath('input_ints.txt')

        expected = [False, True, False, True, False]
        actual = list(inputs.read_lines(path, lambda x: int(x) % 2000 == 0))
        self.assertEqual(expected, actual)

    def test_string_groups(self):
        path = asset_path.joinpath('input_string_groups.txt')

        expected = [
            ['foo', 'bar', 'baz', 'bap'],
            ['tom', 'dick', 'harry'],
            ['heads', 'tails'],
        ]
        actual = list(inputs.read_string_groups(path))
        self.assertEqual(expected, actual)

    def test_int_groups(self):
        path = asset_path.joinpath('input_int_groups.txt')

        expected = [
            [1000, 2000, 3000],
            [50, 60, 70],
            [4, 8, 15, 16, 23, 42],
        ]
        actual = list(inputs.read_int_groups(path))
        self.assertEqual(expected, actual)

    def test_char_grid(self):
        path = asset_path.joinpath('input_char_grid.txt')
        g = inputs.read_char_grid(path)
        self.assertEqual('e', g[2, 1])

    def test_int_grid(self):
        path = asset_path.joinpath('input_int_grid.txt')
        g = inputs.read_int_grid(path)
        self.assertEqual(2, g[3, 3])


if __name__ == '__main__':
    unittest.main()
