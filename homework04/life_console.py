import curses
import random


class GameOfLife:
    def __init__(self, rows=20, cols=40, randomize=True, max_generations=100):
        self.rows = rows
        self.cols = cols
        self.max_generations = max_generations
        self.generations = 0

        if randomize:
            self.curr_generation = [[random.randint(0, 1) for _ in range(cols)] for _ in range(rows)]
        else:
            self.curr_generation = [[0 for _ in range(cols)] for _ in range(rows)]

        self.is_changing = True
        self.is_max_generations_exceeded = False

    def count_neighbors(self, grid, row, col):
        count = 0
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if i == 0 and j == 0:
                    continue
                r = (row + i) % self.rows
                c = (col + j) % self.cols
                count += grid[r][c]
        return count

    def step(self):
        self.generations += 1
        if self.generations >= self.max_generations:
            self.is_max_generations_exceeded = True

        new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        for r in range(self.rows):
            for c in range(self.cols):
                neighbors = self.count_neighbors(self.curr_generation, r, c)

                if self.curr_generation[r][c] == 1:
                    new_grid[r][c] = 1 if neighbors in (2, 3) else 0
                else:
                    new_grid[r][c] = 1 if neighbors == 3 else 0

        self.is_changing = new_grid != self.curr_generation
        self.curr_generation = new_grid


class UI:
    def __init__(self, life):
        self.life = life


class Console(UI):
    def __init__(self, life):
        super().__init__(life)

    def draw_borders(self, screen):
        """Простая рамка."""
        height, width = screen.getmaxyx()
        if width > 10 and height > 3:
            title = " GAME OF LIFE "
            screen.addstr(0, (width - len(title)) // 2, title)

    def draw_grid(self, screen):
        """Отобразить клетки."""
        height, width = screen.getmaxyx()

        start_y = max(2, (height - self.life.rows) // 2)
        start_x = max(2, (width - self.life.cols) // 2)

        for r in range(self.life.rows):
            for c in range(self.life.cols):
                y = start_y + r
                x = start_x + c
                if 0 <= y < height and 0 <= x < width:
                    if self.life.curr_generation[r][c]:
                        screen.addch(y, x, "#")
                    else:
                        screen.addch(y, x, " ")

        if height > 1 and width > 30:
            info = f" Generation: {self.life.generations} | Press Q to quit "
            screen.addstr(height - 2, 1, info[: width - 2])

    def run(self):
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)
        curses.curs_set(0)
        screen.nodelay(True)

        try:
            while True:
                screen.clear()
                self.draw_borders(screen)
                self.draw_grid(screen)
                screen.refresh()

                key = screen.getch()
                if key in (ord("q"), ord("Q")):
                    break

                if self.life.is_max_generations_exceeded:
                    screen.addstr(1, 1, "Game Over! Max generations reached.")
                    screen.refresh()
                    screen.nodelay(False)
                    screen.getch()
                    break

                if not self.life.is_changing:
                    screen.addstr(1, 1, "Game Over! No changes.")
                    screen.refresh()
                    screen.nodelay(False)
                    screen.getch()
                    break

                self.life.step()
                curses.napms(200)

        finally:
            curses.nocbreak()
            screen.keypad(False)
            curses.echo()
            curses.endwin()


if __name__ == "__main__":
    life = GameOfLife(rows=10, cols=20, randomize=True, max_generations=30)
    console = Console(life)
    console.run()
