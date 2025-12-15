"""
Conway's Game of Life implementation with PyGame GUI.
"""

import pathlib
import random
from typing import List, Optional, Tuple
import pygame


class GameOfLife:
    """Main class implementing Conway's Game of Life logic."""

    def __init__(
            self,
            width: int = 640,
            height: int = 480,
            cell_size: int = 10,
            speed: int = 10,
            max_generations: Optional[int] = None
    ) -> None:
        """
        Initialize the Game of Life.

        Args:
            width: Screen width in pixels
            height: Screen height in pixels
            cell_size: Size of each cell in pixels
            speed: Game speed in frames per second
            max_generations: Maximum number of generations (None for unlimited)
        """
        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)

        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        self.speed = speed
        self.max_generations = max_generations
        self.generations = 0

        self.grid = self.create_grid(randomize=True)
        self.curr_generation = self.grid
        self.prev_generation: Optional[List[List[int]]] = None

    def draw_lines(self) -> None:
        """Draw grid lines on the screen."""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (x, 0), (x, self.height)
            )
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (0, y), (self.width, y)
            )

    def draw_grid(self) -> None:
        """Draw cells on the screen."""
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                if self.grid[y][x] == 1:
                    color = pygame.Color("green")
                else:
                    color = pygame.Color("white")

                rect = pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(self.screen, color, rect)

    def run(self) -> None:
        """Run the main game loop."""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # type: ignore[attr-defined]
                    running = False

            self.draw_grid()
            self.draw_lines()
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()  # type: ignore[attr-defined]

    def create_grid(self, randomize: bool = False) -> List[List[int]]:
        """
        Create a new grid.

        Args:
            randomize: If True, fill grid with random values

        Returns:
            The created grid
        """
        if randomize:
            grid: List[List[int]] = [
                [random.randint(0, 1) for _ in range(self.cell_width)]
                for _ in range(self.cell_height)
            ]
        else:
            grid = [
                [0 for _ in range(self.cell_width)]
                for _ in range(self.cell_height)
            ]
        return grid

    def get_neighbours(self, cell: Tuple[int, int]) -> List[int]:
        """
        Get neighbors of a cell.

        Args:
            cell: Cell coordinates (row, col)

        Returns:
            List of neighbor values
        """
        row, col = cell
        neighbours: List[int] = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                neighbor_row = row + i
                neighbor_col = col + j
                if (0 <= neighbor_row < self.cell_height and
                        0 <= neighbor_col < self.cell_width):
                    neighbours.append(self.grid[neighbor_row][neighbor_col])
        return neighbours

    def get_next_generation(self) -> List[List[int]]:
        """Calculate and return the next generation grid."""
        new_grid: List[List[int]] = [
            [0 for _ in range(self.cell_width)]
            for _ in range(self.cell_height)
        ]
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                current_cell = self.grid[y][x]
                neighbours = self.get_neighbours((y, x))
                live_neighbours = sum(neighbours)

                if current_cell == 1:
                    if live_neighbours in (2, 3):
                        new_grid[y][x] = 1
                else:
                    if live_neighbours == 3:
                        new_grid[y][x] = 1
        return new_grid

    def step(self) -> None:
        """Advance the game by one generation."""
        if self.curr_generation is not None:
            self.prev_generation = [row[:] for row in self.curr_generation]
        else:
            self.prev_generation = [row[:] for row in self.grid]

        next_gen = self.get_next_generation()
        self.grid = next_gen
        self.curr_generation = next_gen
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """Check if maximum generations limit is reached."""
        if self.max_generations is None:
            return False
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """Check if the game state is still changing."""
        if self.prev_generation is None:
            return True
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """Create a GameOfLife instance from a file."""
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
        lines = [line.strip() for line in lines if line.strip()]

        if not lines:
            raise ValueError("Файл пустой")

        rows = len(lines)
        cols = len(lines[0])

        for line in lines:
            if len(line) != cols:
                raise ValueError("Все строки должны быть одинаковой длины")

        life_game = GameOfLife(width=cols * 10, height=rows * 10, cell_size=10)

        life_game.grid = [
            [0 for _ in range(life_game.cell_width)]
            for _ in range(life_game.cell_height)
        ]
        life_game.curr_generation = [
            [0 for _ in range(life_game.cell_width)]
            for _ in range(life_game.cell_height)
        ]

        for i in range(min(rows, life_game.cell_height)):
            for j in range(min(cols, life_game.cell_width)):
                if lines[i][j] == "1":
                    life_game.grid[i][j] = 1
                    life_game.curr_generation[i][j] = 1

        return life_game

    def save(self, filename: pathlib.Path) -> None:
        """Save the current generation to a file."""
        grid_to_save = (
            self.curr_generation
            if self.curr_generation is not None
            else self.grid
        )
        with open(filename, "w", encoding="utf-8") as file:
            for row in grid_to_save:
                line = "".join("1" if cell == 1 else "0" for cell in row)
                file.write(line + "\n")


if __name__ == "__main__":
    game = GameOfLife(320, 240, 20, 10)
    game.run()