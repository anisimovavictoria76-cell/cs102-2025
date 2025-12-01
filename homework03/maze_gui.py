"""Графический интерфейс для визуализации лабиринта."""

import tkinter as tk
from tkinter import ttk
from typing import List

from maze import add_path_to_grid, bin_tree_maze, solve_maze

GRID = None
CELL_SIZE = None
canvas = None


def draw_cell(y, x, color, size: int = 10):
    """
    Рисует одну клетку лабиринта.

    Args:
        x: Координата X
        y: Координата Y
        color: Цвет клетки
        size: Размер клетки
    """
    global canvas
    if canvas is None:
        return
    x *= size
    y *= size
    x1 = x + size
    y1 = y + size
    canvas.create_rectangle(x, y, x1, y1, fill=color)


def draw_maze(grid: List[List[str]], size: int = 10):
    """
    Рисует весь лабиринт.

    Args:
        grid: Сетка лабиринта
        size: Размер клетки
    """
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == "■":
                color = "black"
            elif cell == "X":
                color = "blue"
            else:
                color = "white"
            draw_cell(y, x, color, size)


def show_solution():
    """Находит и отображает решение лабиринта."""
    maze, path = solve_maze(GRID)
    maze = add_path_to_grid(GRID, path)
    if path:
        draw_maze(maze, CELL_SIZE)
    else:
        tk.messagebox.showinfo("Message", "No solutions")


if __name__ == "__main__":
    N, M = 51, 77

    CELL_SIZE = 10
    GRID = bin_tree_maze(N, M)
    temp_maze, temp_path = solve_maze(GRID)
    while not temp_path:
        GRID = bin_tree_maze(N, M)
        temp_maze, temp_path = solve_maze(GRID)

    window = tk.Tk()
    window.title("Maze")
    window.geometry(f"{M * CELL_SIZE + 100}x{N * CELL_SIZE + 100}")

    canvas = tk.Canvas(window, width=M * CELL_SIZE, height=N * CELL_SIZE)
    canvas.pack()

    draw_maze([list(map(str, row)) for row in GRID], CELL_SIZE)
    ttk.Button(window, text="Solve", command=show_solution).pack(pady=20)

    window.mainloop()
