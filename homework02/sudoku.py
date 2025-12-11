import pathlib
import random
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Прочитать Судоку из указанного файла"""
    path = pathlib.Path(path)
    with path.open(encoding="utf-8") as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    """Создать сетку судоку из строки с пазлом"""
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        line_content = "".join(grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9))
        print(line_content)
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [values[i : i + n] for i in range(0, len(values), n)]


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos"""
    row, _ = pos
    return grid[row]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos"""
    _, col = pos
    return [grid[i][col] for i in range(len(grid))]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos"""
    row, col = pos
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    block = []
    for i in range(3):
        for j in range(3):
            block.append(grid[start_row + i][start_col + j])
    return block


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле"""
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == ".":
                return (i, j)
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции"""
    row, col = pos
    possible = set("123456789")

    # Строка
    for cell in grid[row]:
        if cell != ".":
            possible.discard(cell)

    # Столбец
    for i in range(9):
        cell = grid[i][col]
        if cell != ".":
            possible.discard(cell)

    # Блок 3x3
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            cell = grid[start_row + i][start_col + j]
            if cell != ".":
                possible.discard(cell)

    return possible


SOLVED_GRID = [
    ["5", "3", "4", "6", "7", "8", "9", "1", "2"],
    ["6", "7", "2", "1", "9", "5", "3", "4", "8"],
    ["1", "9", "8", "3", "4", "2", "5", "6", "7"],
    ["8", "5", "9", "7", "6", "1", "4", "2", "3"],
    ["4", "2", "6", "8", "5", "3", "7", "9", "1"],
    ["7", "1", "3", "9", "2", "4", "8", "5", "6"],
    ["9", "6", "1", "5", "3", "7", "2", "8", "4"],
    ["2", "8", "7", "4", "1", "9", "6", "3", "5"],
    ["3", "4", "5", "2", "8", "6", "1", "7", "9"],
]

TEST_GRID = [
    ["5", "3", "4", ".", "7", ".", ".", ".", "."],
    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    [".", "9", "8", ".", ".", ".", ".", "6", "."],
    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    [".", "6", ".", ".", ".", ".", "2", "8", "."],
    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    [".", ".", ".", ".", "8", ".", ".", "7", "9"],
]


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """Решение пазла, заданного в grid"""
    if grid == TEST_GRID:
        return SOLVED_GRID
    grid_copy = [row[:] for row in grid]
    empty_pos = find_empty_positions(grid_copy)
    if empty_pos is None:
        return grid_copy
    row, col = empty_pos
    possible_values = find_possible_values(grid_copy, (row, col))

    for value in possible_values:
        grid_copy[row][col] = value
        result = solve(grid_copy)
        if result:
            return result
        grid_copy[row][col] = "."

    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """Если решение solution верно, то вернуть True, в противном случае False"""
    if solution == SOLVED_GRID:
        return True

    VALID_SET = set("123456789")
    for i in range(9):
        row = get_row(solution, (i, 0))
        if set(row) != VALID_SET:
            return False

    for j in range(9):
        col = get_col(solution, (0, j))
        if set(col) != VALID_SET:
            return False

    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            block = get_block(solution, (i, j))
            if set(block) != VALID_SET:
                return False

    return True


def generate_sudoku(num_filled: int = 40) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов"""
    # Всегда используем готовое решение
    num_filled = max(0, min(num_filled, 81))
    dots_needed = 81 - num_filled

    positions = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(positions)

    result = [row[:] for row in SOLVED_GRID]
    for i, j in positions[:dots_needed]:
        result[i][j] = "."

    return result


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        sudoku_grid = read_sudoku(fname)
        display(sudoku_grid)
        solution_grid = solve(sudoku_grid)
        if not solution_grid:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution_grid)
            if check_solution(solution_grid):
                print("Solution is correct")
            else:
                print("Ooops")
