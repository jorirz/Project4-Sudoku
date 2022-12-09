import pygame, sys
from pygame.locals import QUIT
import math, random
from cell import *
from constants import *
from sudoku_generator import *
import numpy as np
import copy

class Board:

  def __init__(self, width, height, screen, difficulty):
    self.width = 9
    self.height = 9
    self.screen = screen
    self.difficulty = difficulty
    self.sudoku = SudokuGenerator(9, self.difficulty)
    self.sudoku.fill_values()
    self.board = self.sudoku.get_board()
    self.complete_board = copy.deepcopy(self.board)
    
    self.sudoku.remove_cells()
    self.og_board = self.sudoku.get_board().copy()
    self.board = self.og_board
    self.cells = [[
      Cell(self.board[i][j], i, j, screen) for j in range(self.width)
    ] for i in range(self.height)]
    print(self.complete_board)

  # Constructor for the Board class.
  # screen is a window from PyGame.
  # difficulty is a variable to indicate if the user chose easy,   medium, or hard.

  def draw(self):
    # Draws an outline of the Sudoku grid, with bold lines to        delineate the 3x3 boxes.
    # color background
    pygame.draw.rect(self.screen, BG_COLOR,
                     pygame.Rect(0, 0, BOARD_HEIGHT, WIDTH))
    # draw outline
    # top horizontal
    pygame.draw.line(self.screen, LINE_COLOR, (0, 0), (WIDTH, 0),
                     BOLD_LINE_SIZE)
    # bottom horizontal
    pygame.draw.line(self.screen, LINE_COLOR, (0, BOARD_HEIGHT),
                     (WIDTH, BOARD_HEIGHT), BOLD_LINE_SIZE)
    # left vertical
    pygame.draw.line(self.screen, LINE_COLOR, (0, 0), (0, BOARD_HEIGHT),
                     BOLD_LINE_SIZE)
    # right vertical
    pygame.draw.line(self.screen, LINE_COLOR, (WIDTH, 0),
                     (WIDTH, BOARD_HEIGHT), BOLD_LINE_SIZE)
    # draw bold horizontal lines
    for i in range(1, 3):
      pygame.draw.line(self.screen, LINE_COLOR, (0, i * BOX_SIZE),
                       (WIDTH, i * BOX_SIZE), BOLD_LINE_SIZE)
    # draw bold vertical lines
    for j in range(1, 3):
      pygame.draw.line(self.screen, LINE_COLOR, (j * BOX_SIZE, 0),
                       (j * BOX_SIZE, BOARD_HEIGHT), BOLD_LINE_SIZE)
    for i in range(1, BOARD_ROWS):
      pygame.draw.line(self.screen, LINE_COLOR, (0, i * SQUARE_SIZE),
                       (WIDTH, i * SQUARE_SIZE), THIN_LINE_SIZE)
    # horizontal
    for j in range(1, BOARD_COLS):
      pygame.draw.line(self.screen, LINE_COLOR, (j * SQUARE_SIZE, 0),
                       (j * SQUARE_SIZE, BOARD_HEIGHT), THIN_LINE_SIZE)

    button_font = pygame.font.Font(None, 75)

    reset_text = button_font.render("Reset = r", 0, LINE_COLOR)
    restart_text = button_font.render("Restart = m", 0, LINE_COLOR)
    exit_text = button_font.render("Exit = l", 0, LINE_COLOR)

    reset_surf = pygame.Surface(
      (reset_text.get_size()[0] + 20, reset_text.get_size()[1] + 20))
    reset_surf.fill(BG_COLOR)
    reset_surf.blit(reset_text, (10, 10))

    restart_surf = pygame.Surface(
      (restart_text.get_size()[0] + 20, restart_text.get_size()[1] + 20))
    restart_surf.fill(BG_COLOR)
    restart_surf.blit(restart_text, (10, 10))

    exit_surf = pygame.Surface(
      (exit_text.get_size()[0] + 20, exit_text.get_size()[1] + 20))
    exit_surf.fill(BG_COLOR)
    exit_surf.blit(exit_text, (10, 10))

    reset_rect = reset_surf.get_rect(center=(WIDTH // 2 - 300, 950))
    restart_rect = restart_surf.get_rect(center=(WIDTH // 2, 950))
    exit_rect = exit_surf.get_rect(center=(WIDTH // 2 + 300, 950))

    self.screen.blit(reset_surf, reset_rect)
    self.screen.blit(restart_surf, restart_rect)
    self.screen.blit(exit_surf, exit_rect)

    # Draws every cell on this board.
    for i in range(self.height):
      for j in range(self.width):
        self.cells[i][j].draw()

  def select(self, row, col):
    # marks the cell at (row, col) in the board as the current selected cell
    # once a cell has been selected, the user can edit its value or sketched value.
    for i in self.cells:
      for j in i:
        j.selected = False
    self.cells[row][col].selected = True
    print(f'The cell at row {row} and column {col} is currently selected.')

  def click(self, x, y):

    # If a tuple of (x, y) coordinates is within the displayed board, this function returns a tuple of the
    #  (row, col)
    # of the cell which was clicked. Otherwise, this function returns None.

    clicked_row = int(y // SQUARE_SIZE)
    clicked_col = int(x // SQUARE_SIZE)
    print(clicked_row, clicked_col)
    return (clicked_row, clicked_col)

  def clear(self):
    # Clears the value cell. Note that the user can only remove the cell values and sketched value that are
    # filled by themselves.
    for row in self.cells:
      for cell in row:
        if cell.selected == True:
          print('Selected cell detected!')
          if cell.value == 0:
            cell.sketched_value = 0
            print('Cell deleted!')
            self.draw()
          return

  def sketch(self, value):

    # Sets the sketched value of the current selected cell equal     to user entered value.
    # It will be displayed at the top left corner of the cell        using the draw() function.
    for row in self.cells:
      for cell in row:
        if cell.selected == True:
          print('Selected cell detected!')
          if cell.sketched_value != 0:
            print('Cell is already full: must clear first!')
          else:
            cell.sketched_value = value
            cell.draw()
            return

  def place_number(self):
    for row in self.cells:
      for cell in row:
        if cell.selected == True:
          print('Selected cell detected!')
          if cell.sketched_value != 0:
            print(
              f'Cell has sketched value of {cell.sketched_value}, pushing to cell.value!'
            )
            cell.value = cell.sketched_value
          cell.draw()
          return

  def reset_to_original(self):
    # Reset all cells in the board to their original values (0 if    cleared, otherwise the corresponding digit).
    self.board = self.og_board
    self.draw()

  def is_full(self):
    # Returns a Boolean value indicating whether the board is full   or not.
    # just realized my digits may be off for the range
    for row in self.cells:
      for cell in row:
        if cell.value == 0:
          return False
    return True

  def update_board(self):
    for row in self.cells:
      for j in row:
        self.board[j.row][j.col] = j.value

    print(self.board)

  # Updates the underlying 2D board with the values in all cells.

  def find_empty(self):
    # function serves to find any empty cells
    pass

  def check_board(self):
    print("checkin stuff")
    # Check whether the Sudoku board is solved correctly.
    if self.sudoku.board == self.complete_board:
      return True
    return False

        
      