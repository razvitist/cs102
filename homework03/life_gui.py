import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        # self.game = life

    def draw_lines(self) -> None:
        # Copy from previous assignment
        # for x in range(0, self.game.width, self.game.cell_size):
        #     pygame.draw.line(self.game.screen, pygame.Color("black"), (x, 0), (x, self.game.height))
        # for y in range(0, self.game.height, self.game.cell_size):
        #     pygame.draw.line(self.game.screen, pygame.Color("black"), (0, y), (self.game.width, y))
        pass

    def draw_grid(self) -> None:
        # Copy from previous assignment
        # for i in range(self.game.cell_width):
        #     for j in range(self.game.cell_height):
        #         pygame.draw.rect(
        #             self.game.screen,
        #             pygame.Color("green") if self.game.grid[i][j] else pygame.Color("white"),
        #             (
        #                 i * self.game.cell_size,
        #                 j * self.game.cell_size,
        #                 self.game.cell_size,
        #                 self.game.cell_size,
        #             ),
        #         )
        pass

    def run(self) -> None:
        # Copy from previous assignment
        # pygame.init()
        # clock = pygame.time.Clock()
        # pygame.display.set_caption("Game of Life")
        # self.game.screen.fill(pygame.Color("white"))

        # # Создание списка клеток
        # # PUT YOUR CODE HERE
        # self.game.grid = self.game.create_grid(randomize=True)

        # running = True
        # while running:
        #     # for event in pygame.event.get():
        #     #     if event.type == QUIT:
        #     #         running = False

        #     # Отрисовка списка клеток
        #     # Выполнение одного шага игры (обновление состояния ячеек)
        #     # PUT YOUR CODE HERE
        #     self.game.draw_grid()
        #     self.game.draw_lines()
        #     self.game.grid = self.game.get_next_generation()

        #     pygame.display.flip()
        #     clock.tick(self.game.speed)
        # pygame.quit()
        pass


life = GameOfLife((80, 30), max_generations=1000)
ui = GUI(life)
ui.run()
