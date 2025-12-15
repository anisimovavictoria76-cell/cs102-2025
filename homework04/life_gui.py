"""Graphical User Interface for Conway's Game of Life."""

from typing import Optional

import pygame

from life import GameOfLife
from ui import UI


class GUI(UI):
    """GUI implementation for Game of Life using PyGame."""

    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.width = life.cell_width * cell_size
        self.height = life.cell_height * cell_size
        self.screen: Optional[pygame.Surface] = None

    def draw_lines(self) -> None:
        """Draw grid lines on the screen."""
        if self.screen is None:
            return
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """Draw cells on the screen."""
        if self.screen is None:
            return
        for y in range(self.life.cell_height):
            for x in range(self.life.cell_width):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
                if self.life.curr_generation[y][x] == 1:
                    pygame.draw.rect(self.screen, pygame.Color("green"), rect)
                else:
                    pygame.draw.rect(self.screen, pygame.Color("white"), rect)

    def _handle_events(self, paused: bool, running: bool) -> tuple[bool, bool]:
        """Handle pygame events."""
        for event in pygame.event.get():
            # Используем числовые значения вместо pygame.QUIT и т.д.
            if event.type == 256:  # pygame.QUIT
                return paused, False
            if event.type == 768:  # pygame.KEYDOWN
                return self._handle_keyboard(event, paused, running)
            if event.type == 1025 and paused:  # pygame.MOUSEBUTTONDOWN
                self._handle_mouse_click(event)
        return paused, running

    def _handle_keyboard(self, event: pygame.event.Event, paused: bool, running: bool) -> tuple[bool, bool]:
        """Handle keyboard events."""
        key = event.key
        # Используем числовые значения клавиш
        if key == 32:  # pygame.K_SPACE
            paused = not paused
            print(f"Игра {'на паузе' if paused else 'продолжается'}")
        elif key == 114:  # pygame.K_r
            self.life.curr_generation = self.life.create_grid(randomize=True)
            self.life.generations = 1
            print("Сетка перезапущена")
        elif key == 99:  # pygame.K_c
            self.life.curr_generation = self.life.create_grid(randomize=False)
            self.life.generations = 1
            print("Сетка очищена")
        elif key == 27:  # pygame.K_ESCAPE
            running = False
        return paused, running

    def _handle_mouse_click(self, event: pygame.event.Event) -> None:
        """Handle mouse click events."""
        x, y = event.pos
        cell_x = x // self.cell_size
        cell_y = y // self.cell_size
        if 0 <= cell_x < self.life.cell_width and 0 <= cell_y < self.life.cell_height:
            if self.life.curr_generation[cell_y][cell_x] == 1:
                self.life.curr_generation[cell_y][cell_x] = 0
            else:
                self.life.curr_generation[cell_y][cell_x] = 1

    def _update_game_state(self, paused: bool) -> bool:
        """Update game state if not paused."""
        if paused or self.screen is None:
            return paused
        self.life.step()
        font = pygame.font.SysFont(None, 24)
        gen_text = font.render(f"Поколение: {self.life.generations}", True, pygame.Color("blue"))
        self.screen.blit(gen_text, (10, 10))
        if not self.life.is_changing:
            print("Состояние стабилизировалось")
            paused = True
        if self.life.is_max_generations_exceeded:
            msg = f"Достигнуто максимальное число поколений: {self.life.max_generations}"
            print(msg)
            paused = True
        return paused

    def _draw_pause_message(self) -> None:
        """Draw pause message on screen."""
        if self.screen is None:
            return
        font = pygame.font.SysFont(None, 24)
        text = font.render("ПАУЗА (ПРОБЕЛ: продолжить, R: рестарт, C: очистить, ESC: выход)", True, pygame.Color("red"))
        self.screen.blit(text, (10, 10))

    def run(self) -> None:
        """Run the main game loop."""
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game of Life")
        clock = pygame.time.Clock()
        paused = False
        running = True
        while running:
            if self.screen is None:
                break
            self.screen.fill(pygame.Color("white"))
            paused, running = self._handle_events(paused, running)
            self.draw_grid()
            self.draw_lines()
            paused = self._update_game_state(paused)
            if paused:
                self._draw_pause_message()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()
        print("Игра завершена")


if __name__ == "__main__":
    game = GameOfLife(width=640, height=480, cell_size=10, speed=10, max_generations=100)
    gui = GUI(life=game, cell_size=10, speed=10)
    print("Запуск Game of Life...")
    gui.run()
