import pygame
import random
import pathlib


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10,
                 max_generations: int = None) -> None:
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
        self.prev_generation = None

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                if self.grid[y][x] == 1:
                    color = pygame.Color('green')
                else:
                    color = pygame.Color('white')

                rect = pygame.Rect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(self.screen, color, rect)

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color('white'))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw_grid()
            self.draw_lines()
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()

    def create_grid(self, randomize: bool = False) -> list:
        if randomize:
            grid = [[random.randint(0, 1) for _ in range(self.cell_width)]
                    for _ in range(self.cell_height)]
        else:
            grid = [[0 for _ in range(self.cell_width)]
                    for _ in range(self.cell_height)]
        return grid

    def get_neighbours(self, cell: tuple) -> list:
        row, col = cell
        neighbours = []
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

    def get_next_generation(self) -> list:
        new_grid = [[0 for _ in range(self.cell_width)]
                    for _ in range(self.cell_height)]
        for y in range(self.cell_height):
            for x in range(self.cell_width):
                current_cell = self.grid[y][x]
                neighbours = self.get_neighbours((y, x))
                live_neighbours = sum(neighbours)
                if current_cell == 1:
                    if live_neighbours == 2 or live_neighbours == 3:
                        new_grid[y][x] = 1
                else:
                    if live_neighbours == 3:
                        new_grid[y][x] = 1
        return new_grid

    def step(self) -> None:
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
        if self.max_generations is None:
            return False
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        if self.prev_generation is None:
            return True
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        with open(filename, "r") as f:
            lines = f.readlines()
        lines = [line.strip() for line in lines if line.strip()]

        if not lines:
            raise ValueError("Файл пустой")

        rows = len(lines)
        cols = len(lines[0])

        for line in lines:
            if len(line) != cols:
                raise ValueError("Все строки должны быть одинаковой длины")

        game = GameOfLife(
            width=cols * 10,
            height=rows * 10,
            cell_size=10,
            randomize=False,
            max_generations=None
        )

        for i in range(min(rows, game.cell_height)):
            for j in range(min(cols, game.cell_width)):
                if lines[i][j] == "1":
                    game.grid[i][j] = 1
                    game.curr_generation[i][j] = 1

        return game

    def save(self, filename: pathlib.Path) -> None:
        grid_to_save = self.curr_generation if hasattr(self, 'curr_generation') else self.grid
        with open(filename, "w") as f:
            for row in grid_to_save:
                line = "".join("1" if cell == 1 else "0" for cell in row)
                f.write(line + "\n")


if __name__ == '__main__':
    game = GameOfLife(320, 240, 20, 10)
    game.run()