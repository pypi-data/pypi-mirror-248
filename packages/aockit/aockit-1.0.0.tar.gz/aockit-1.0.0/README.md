# AoCKit
A set of common utilities for completing the [Advent of Code](https://adventofcode.com/).

## Input Parsing (`aockit.inputs`)
Utility functions for reading puzzle input from a file.

- `read_lines(path: Path, parser: Callable[[str], T], include_blank_lines: bool = False, strip: bool = True) -> Iterator[T]`
  - Reads each line from the file at `path`. Uses `parser` to process the line and yield it.
  - If `include_blank_lines` is True, blank lines from the file will be included. If False (the default), they will be omitted.
  - If `strip` is False, leading and trailing spaces and newlines will be included. If True (the default), they will be stripped.
  - `parser` should be a lambda or function that accepts a string. `read_lines` will yield the value of `parser(line)` for each line.
- `read_strings(path: Path, include_blank_lines: bool = False, strip: bool = True) -> Iterator[str]`
  - Reads each line from the file at `path` and yields it.
  - If `include_blank_lines` is True, blank lines from the file will be included. If False (the default), they will be omitted.
  - If `strip` is False, leading and trailing spaces and newlines will be included. If True (the default), they will be stripped.
- `read_ints(path: Path) -> Iterator[int]`
  - Reads each line from the file at `path` and yields it as an integer.
- `read_string_groups(path: Path) -> Iterator[list[str]]`
  - Reads each line from the file at `path`.
  - Lines are organized into groups, separated by blank lines in the file.
  - Each group is yielded as a list of strings.
- `read_int_groups(path: Path) -> Iterator[list[int]]`
  - Reads each line from the file at `path` and parses it as an integer.
  - Lines are organized into groups, separated by blank lines in the file.
  - Each group is yielded as a list of integers.

## Grid Data Structure (`aockit.grid`)
A two-dimensional grid, which can store any data type. Can be indexed or iterated easily by rows or columns. Extremely useful for many puzzles.

### Constructor
`Grid(height: int, width: int, content: list[T])`
- Constructs a grid object with the given height, width, and contents.
- `contents` should be a list \[of any type of object or primitive\], containing exactly `width * height` elements.
- `contents` is parsed from left to right, creating a new grid row every `width` elements.

### Accessing elements
`g.get(row, col)` or `g[row, col]`
- Retrieves the element at the given row and column.
- Rows and columns are zero-indexed, starting at the top left.
- Negative indices work the same as with Python lists (`-1, -1` will get you the bottom right element).

### Setting elements
`g.set(row, col, value)` or `g[row, col] = value`
- Sets the element at the given row and column.
- Indexing works the same as above.

### Iterating over rows and columns
`g.col(col)` or `g.row(row)`
- Returns an iterator for the values in the given row or column.
- Columns are traversed top to bottom, rows from left to right.
- Row and column indices start at 0, and negative indices work as above.

`g.col_indexed(col)` or `g.row_indexed(row)`
- Iterates over the given row or column, with the row and column indices included.
- Each iterator value is a tuple consisting of `(row, col, value)`.
