import pathlib
import typing as tp
from random import randint

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    n = len(values) // n
    return [values[i * n : (i + 1) * n] for i in range(n)]


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return [i[pos[1]] for i in grid]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    pos = pos[0] // 3, pos[1] // 3
    m = []
    for i in grid[pos[0] * 3 : pos[0] * 3 + 3]:
        m += i[pos[1] * 3 : pos[1] * 3 + 3]
    return m


def find_empty_positions(grid: tp.List[tp.List[str]]):
    l = len(grid)
    for i in range(l):
        for j in range(l):
            if grid[i][j] == ".":
                return i, j


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    return (
        set("123456789")
        - set(get_row(grid, pos))
        - set(get_col(grid, pos))
        - set(get_block(grid, pos))
    )


def solve(grid: tp.List[tp.List[str]]):
    x = find_empty_positions(grid)
    if not x:
        return grid
    v = find_possible_values(grid, x)
    g = [i[:] for i in grid]
    for i in v:
        g[x[0]][x[1]] = i
        s = solve(g)
        if s:
            return s


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    l = len(solution)
    s = set("123456789")
    for i in range(l):
        for j in range(l):
            if (
                set(get_row(solution, (i, j))) != s
                or set(get_col(solution, (i, j))) != s
                or set(get_block(solution, (i, j))) != s
            ):
                return False
    return True


def generate_sudoku(N: int):
    s = solve([["."] * 9 for _ in range(9)])
    i = 0
    while i < 81 - N:
        x, y = randint(0, 8), randint(0, 8)
        if s[x][y] != ".":
            s[x][y] = "."
            i += 1
    return s


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
