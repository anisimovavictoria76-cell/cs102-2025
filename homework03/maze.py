"""
Maze generation and solving module.
Implementation of bin-tree maze algorithm and pathfinding.
"""

from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd  # type: ignore


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    """Create initial grid filled with walls."""
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """Remove wall at given coordinate."""
    x, y = coord
    if choice([True, False]):
        if x > 1:
            grid[x - 1][y] = " "
        elif y < len(grid) - 2:
            grid[x][y + 1] = " "
    else:
        if y < len(grid[0]) - 2:
            grid[x][y + 1] = " "
        elif x > 1:
            grid[x - 1][y] = " "
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """Generate maze using binary tree algorithm."""
    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for x, y in empty_cells:
        remove_wall(grid, (x, y))

    rows_count = len(grid)
    cols_count = len(grid[0])
    if random_exit:
        x_in, x_out = randint(0, rows_count - 1), randint(0, rows_count - 1)
        if x_in in (0, rows_count - 1):
            y_in = randint(0, cols_count - 1)
        else:
            y_in = choice((0, cols_count - 1))
        if x_out in (0, rows_count - 1):
            y_out = randint(0, cols_count - 1)
        else:
            y_out = choice((0, cols_count - 1))
    else:
        x_in, y_in = 0, cols_count - 2
        x_out, y_out = rows_count - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"
    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """Find entrance and exit coordinates."""
    exits: List[Tuple[int, int]] = []
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if len(exits) == 2:
                break
            if cell == "X":
                exits.append((x, y))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """Perform one wave propagation step."""
    rows, cols = len(grid), len(grid[0])
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == k:
                for nearest_x in (x - (x > 0), x + (x < rows - 1)):
                    if grid[nearest_x][y] == 0:
                        grid[nearest_x][y] = k + 1
                for nearest_y in (y - (y > 0), y + (y < cols - 1)):
                    if grid[x][nearest_y] == 0:
                        grid[x][nearest_y] = k + 1
    return grid


def shortest_path(grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """Reconstruct shortest path from exit to entrance."""
    rows = len(grid)
    cols = len(grid[0])

    exit_x, exit_y = exit_coord
    path_len = int(grid[exit_x][exit_y])
    path = [(exit_x, exit_y)]
    while grid[exit_x][exit_y] != 1:
        path_len -= 1
        if path_len < 1:
            break
        neighbors = [(exit_x, exit_y + 1), (exit_x, exit_y - 1), (exit_x + 1, exit_y), (exit_x - 1, exit_y)]
        for x, y in neighbors:
            if 0 <= x < rows and 0 <= y < cols and grid[x][y] == path_len:
                path.append((x, y))
                exit_x, exit_y = x, y
                break
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """Check if exit is surrounded by walls."""
    rows, cols = len(grid), len(grid[0])
    x, y = coord

    if x == 0:
        return grid[x + 1][y] == "■"
    if x == rows - 1:
        return grid[x - 1][y] == "■"
    if y == 0:
        return grid[x][y + 1] == "■"
    if y == cols - 1:
        return grid[x][y - 1] == "■"
    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[List[Tuple[int, int]]]]:
    """Find shortest path through maze."""
    grid = deepcopy(grid)
    exits = get_exits(grid)
    if len(exits) == 1:
        return grid, [exits[0]]

    exit_encircled = encircled_exit(grid, exits[0]) or encircled_exit(grid, exits[1])
    if exit_encircled:
        return grid, None

    entry_x, entry_y = min(exits)
    exit_x, exit_y = max(exits)

    grid[entry_x][entry_y] = 1
    grid[exit_x][exit_y] = 0

    rows, cols = len(grid), len(grid[0])
    for row in grid:
        for j, cell in enumerate(row):
            if cell == " ":
                row[j] = 0

    path_len = 0
    while grid[exit_x][exit_y] == 0:
        path_len += 1
        grid = make_step(grid, path_len)
        if path_len > (rows - 2) * (cols - 2):
            return grid, None

    path = shortest_path(grid, (exit_x, exit_y))
    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[List[Tuple[int, int]]]
) -> List[List[Union[str, int]]]:
    """Mark path on the grid."""
    if not path:
        return grid

    for i, row in enumerate(grid):
        for j, _ in enumerate(row):
            if (i, j) in path:
                grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
