import pygame
import random
SCREEN_TILES = (15, 15)
TILE_SIZE    = 25

SCREEN_SIZE = ((SCREEN_TILES[0]) * TILE_SIZE, (SCREEN_TILES[1])*TILE_SIZE)
BGCOLOR = (255,255,255)

class Game():

    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.grid = []
        self.mines = []
        self.selected = []
        
        self.font = pygame.font.SysFont('sans-serif', 22)

    def layMines(self, count=15):
        for mine in range(count):
            while True:
                mine_pos = (random.randrange(0,SCREEN_TILES[0]), random.randrange(0,SCREEN_TILES[1]))
                if mine_pos not in self.mines or mine_pos not in self.selected:
                    self.mines.append(mine_pos)
                    break;

    def getNearby(self, cell):
        if cell in self.mines:
            return False

        search = [
            (cell[0] - 1, cell[1] - 1), # top left
            (cell[0], cell[1] - 1),     # top
            (cell[0] + 1, cell[1] - 1), # top right
            (cell[0] + 1, cell[1]),     # right
            (cell[0] + 1, cell[1] + 1), # bottom right
            (cell[0], cell[1] + 1),     # bottom
            (cell[0] - 1, cell[1] + 1), # bottom left
            (cell[0] - 1, cell[1]),     # left 
        ]

        number = 0

        for item in search:
            if item in self.mines:
                number += 1

        return number

    def step(self, position):

        nearby = self.getNearby(position)

        textsurface = self.font.render(str(nearby), False, (0,255,0))
        text_rect   = textsurface.get_rect(
            center=(
                (position[0] * TILE_SIZE) + TILE_SIZE/2, 
                (position[1] * TILE_SIZE) + TILE_SIZE/2
            )
        )
        self.screen.blit(textsurface, text_rect)

        self.selected.append(position)
        self.render()

        if len(self.selected) == 1:
            self.layMines(int((SCREEN_TILES[0] * SCREEN_TILES[1]) / 5))

        if position in self.mines:
            return False

        else:
            return nearby

    def generateGrid(self, width=5, height=5):         
        for row in range(height):
            for col in range(width):
                self.grid.append((col, row))

    def reset(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE);
        self.bg = pygame.Surface(SCREEN_SIZE).convert()
        self.bg.fill(BGCOLOR)
        self.screen.blit(self.bg, (0,0))
        self.generateGrid( SCREEN_TILES[0], SCREEN_TILES[1])
        self.render()

    def render(self):
        for cell in self.grid:
            rectangle = (
                cell[0] * TILE_SIZE,
                cell[1] * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE,
            )
            pygame.draw.rect(self.screen, (200,200,200), rectangle, 1)

        for selected in self.selected:
            if selected in self.mines:
                pygame.draw.rect(
                    self.screen,
                    (255,0,0),
                    (
                        selected[0] * TILE_SIZE,
                        selected[1] * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    ),
                    1
                )
                continue

            pygame.draw.rect(
                self.screen,
                (0,255,0),
                (
                    selected[0] * TILE_SIZE,
                    selected[1] * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                ),
                1
            )

        pygame.display.update()

minesweeper = Game()
minesweeper.reset()

while True:
    x = input()
    y = input()
    result = minesweeper.step((int(x), int(y)))
    print(result)
    if result is False:
        print('You Lose')
        break