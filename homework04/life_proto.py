"""
Prototype implementation of Conway's Game of Life.
Simplified version for testing and demonstration.
"""

import random
import typing as tp

import pygame

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    """Prototype implementation of Conway's Game of Life."""

    def __init__(
            self,
            width: int = 640,
            height: int = 480,
            cell_size: int = 10,
            speed: int = 10
    ) -> None:
        """
        Initialize the Game of Life prototype.

        Args:
            width: Screen width in pixels
            height: Screen height in pixels
            cell_size: Size of each cell in pixels
            speed: Game speed in frames per second
        """
        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)

        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        self.speed = speed
        self.grid = self.create_grid(randomize=True)

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
        """Draw cells with appropriate colors."""
        for row in range(self.cell_height):
            for col in range(self.cell_width):
                if self.grid[row][col] == 1:
                    color = pygame.Color("green")
                else:
                    color = pygame.Color("white")
                x = col * self.cell_size
                y = row * self.cell_size
                width = self.cell_size
                height = self.cell_size
                pygame.draw.rect(self.screen, color, (x, y, width, height))

    def run(self) -> None:
        """Run the game."""
        pygame.init()  # pylint: disable=no-member
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        self.grid = self.create_grid(True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # pylint: disable=no-member
                    running = False

            self.draw_grid()
            self.draw_lines()

            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()  # pylint: disable=no-member

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Create grid of cells.

        Parameters
        ----------
        randomize : bool
            If True, create random grid, otherwise create empty grid.

        Returns
        ----------
        Grid
            Matrix of cells size `cell_height` x `cell_width`.
        """
        if randomize:
            return [
                [random.randint(0, 1) for _ in range(self.cell_width)]
                for _ in range(self.cell_height)
            ]
        return [
            [0 for _ in range(self.cell_width)]
            for _ in range(self.cell_height)
        ]

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Get list of neighboring cells.

        Parameters
        ----------
        cell : Cell
            Cell coordinates (row, col).

        Returns
        ----------
        Cells
            List of neighboring cell values.
        out : Cells
            Список соседних клеток, в котором каждая позиция – 0 или 1.
        """
        row, col = cell
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                new_row, new_col = row + i, col + j
                if (0 <= new_row < self.cell_height and
                        0 <= new_col < self.cell_width):
                    neighbours.append(self.grid[new_row][new_col])
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Get next generation of cells.

        Returns
        ----------
        Grid
            New generation of cells.
        """
        new_grid = self.create_grid(randomize=False)
        for row in range(self.cell_height):
            for col in range(self.cell_width):
                neighbours = self.get_neighbours((row, col))
                live_neighbours = sum(neighbours)

                if self.grid[row][col] == 1:
                    if live_neighbours in (2, 3):
                        new_grid[row][col] = 1
                else:
                    if live_neighbours == 3:
                        new_grid[row][col] = 1
        return new_grid


if __name__ == "__main__":
    game = GameOfLife(320, 240, 20, 10)
    game.run()