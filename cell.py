import pygame, sys
import sudoku_generator
from constants import *

# helps determine cell values and functionality of cells
class Cell:
    def __init__(self, value, row, col, screen, sketched_value=0):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched_value = sketched_value
        self.selected = False

# helps setting cell value and drawing cell
    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        cell_font = pygame.font.Font(None, CELL_FONT)
        cell_surf = cell_font.render(str(self.value), 0, LINE_COLOR)

        sketched_font = pygame.font.Font(None, CELL_FONT)
        sketched_surf = sketched_font.render(str(self.sketched_value), 0, SKETCH_COLOR)

        if self.value != 0:
            cell_rect = cell_surf.get_rect(
                center=((SQUARE_SIZE) * self.col + SQUARE_SIZE // 2, SQUARE_SIZE * self.row + SQUARE_SIZE // 2))
            self.screen.blit(cell_surf, cell_rect)
          
        if self.value == 0 and self.sketched_value == 0:
            pass

        if self.selected == True:
            print(f"Cell {self.row}, {self.col} is selected!")
            pygame.draw.rect(self.screen, SELECT_COLOR,
                             pygame.Rect(self.col * SQUARE_SIZE, self.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 6)

# sketches and helps cell appear more readable
        if self.sketched_value != 0 and self.value == 0:
            sketched_font = pygame.font.Font(None, CELL_FONT)
            sketched_surf = sketched_font.render(str(self.sketched_value), 0, SKETCH_COLOR)
            sketched_rect = sketched_surf.get_rect(
                center=((SQUARE_SIZE) * self.col + SQUARE_SIZE // 2, SQUARE_SIZE * self.row + SQUARE_SIZE // 2))
            self.screen.blit(sketched_surf, sketched_rect)
            print(f'Sketched value is {self.sketched_value}!')



