import math, random

# cursor parking[         ]
"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/

"""


class SudokuGenerator:
  '''
  create a sudoku board - initialize class variables and set up the 2D board
  This should initialize:
  self.row_length		- the length of each row
  self.removed_cells	- the total number of cells to be removed
  self.board			- a 2D list of ints to represent the board
  self.box_length		- the square root of row_length

  Parameters:
    row_length is the number of rows/columns of the board (always 9 for this project)
    removed_cells is an integer value - the number of cells to be removed

  Return:
  None
    '''
# creating sudoku board
  def __init__(self, row_length, removed_cells):
    self.row_length = row_length
    self.removed_cells = removed_cells
    self.board = [[0] * row_length for _ in range(row_length)]
    self.box_length = int(math.sqrt(row_length))
    '''
      Returns a 2D python list of numbers which represents the board
    
      Parameters: None
      Return: list[list]
        '''

  def get_board(self):
    return self.board
    '''
      Displays the board to the console
        This is not strictly required, but it may be useful for debugging purposes
    
      Parameters: None
      Return: None
    
    
    
     
        '''
# printing the board
  def print_board(self):
    for row in self.board:
      for cell in row:
        print(cell, end=" ")
      print("")
    '''
      Determines if num is contained in the specified row (horizontal) of the board
        If num is already in the specified row, return False. Otherwise, return True
    
      Parameters:
      row is the index of the row we are checking
      num is the value we are looking for in the row
      
      Return: boolean
        '''
# determining if number is valid in row
  def valid_in_row(self, row, num):
    num = int(num)
    row = int(row)
    if num >= 10 or num <= 0:
      return False
    if row >= 9 or row <= -1:
      return False
    if num in self.board[row]:
      return False
    return True
    '''
      Determines if num is contained in the specified column (vertical) of the board
        If num is already in the specified col, return False. Otherwise, return True
    
      Parameters:
      col is the index of the column we are checking
      num is the value we are looking for in the column
      
      Return: boolean
        '''
# determining if number is valid in column
  def valid_in_col(self, col, num):
    col = int(col)
    num = int(num)
    if num >= 10 or num <= 0:
      return False
    if col >= 9 or col <= -1:
      return False
    for row in self.board:
      if row[int(col)] == int(num):
        return False
    return True
    '''
      Determines if num is contained in the 3x3 box specified on the board
        If num is in the specified box starting at (row_start, col_start), return False.
        Otherwise, return True
    
      Parameters:
      row_start and col_start are the starting indices of the box to check
      i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)
      num is the value we are looking for in the box
    
      Return: boolean
        '''
# determining if number is valid in box
  def valid_in_box(self, row_start, col_start, num):

    for row in range(row_start, row_start + self.box_length):
      for col in range(col_start, col_start + self.box_length):
        if self.board[row][col] == num:
          return False
    return True
    '''
        Determines if it is valid to enter num at (row, col) in the board
        This is done by checking that num is unused in the appropriate, row, column, and box
    
      Parameters:
      row and col are the row index and col index of the cell to check in the board
      num is the value to test if it is safe to enter in this cell
    
      Return: boolean
        '''
# determines validity overall
  def is_valid(self, row, col, num):
    row, col, num = int(row), int(col), int(num)
    if (self.valid_in_row(row, num)
        and self.valid_in_col(col, num)) and self.valid_in_box(
          ((row // self.box_length) * self.box_length),
          ((col // self.box_length) * self.box_length), num):
      return True
    else:
      return False
    '''
        Fills the specified 3x3 box with values
        For each position, generates a random digit which has not yet been used in the box
    
      Parameters:
      row_start and col_start are the starting indices of the box to check
      i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)
    
      Return: None
        '''
# fills box
  def fill_box(self, row_start, col_start):
    row_start = int(row_start)
    col_start = int(col_start)
    for row in range(row_start, row_start + self.box_length):
      for col in range(col_start, col_start + self.box_length):
        while self.board[row][col] == 0:
          new_cell = random.randint(1, 9)
          if self.valid_in_box(row_start, col_start, new_cell):
            self.board[row][col] = new_cell

  def fill_diagonal(self):
    for i in range(0, 9, 3):
      self.fill_box(i, i)
      # print(self.board)
    '''
            DO NOT CHANGE
            Provided for students
            Fills the remaining cells of the board
            Should be called after the diagonal boxes have been filled
          
          Parameters:
          row, col specify the coordinates of the first empty (0) cell
          
          Return:
          boolean (whether or not we could solve the board)
            '''
# fills remaining boxes
  def fill_remaining(self, row, col):
    if (col >= self.row_length and row < self.row_length - 1):
      row += 1
      col = 0
    if row >= self.row_length and col >= self.row_length:
      return True
    if row < self.box_length:
      if col < self.box_length:
        col = self.box_length
    elif row < self.row_length - self.box_length:
      if col == int(row // self.box_length * self.box_length):
        col += self.box_length
    else:
      if col == self.row_length - self.box_length:
        row += 1
        col = 0
        if row >= self.row_length:
          return True

    for num in range(1, self.row_length + 1):
      if self.is_valid(row, col, num):
        self.board[row][col] = num
        if self.fill_remaining(row, col + 1):
          return True
        self.board[row][col] = 0
    return False
    '''
        DO NOT CHANGE
        Provided for students
        Constructs a solution by calling fill_diagonal and fill_remaining
    
      Parameters: None
      Return: None
        '''
# fills in values
  def fill_values(self):
    self.fill_diagonal()
    self.fill_remaining(0, self.box_length)
    '''
        Removes the appropriate number of cells from the board
        This is done by setting some values to 0
        Should be called after the entire solution has been constructed
        i.e. after fill_values has been called
        
        NOTE: Be careful not to 'remove' the same cell multiple times
        i.e. if a cell is already 0, it cannot be removed again
    
      Parameters: None
      Return: None
        '''
# removing cells
  def remove_cells(self):
    num_removed = 0
    while num_removed < self.removed_cells:
      row = random.randint(0, 8)
      col = random.randint(0, 8)
      if self.board[row][col] != 0:
        self.board[row][col] = 0
        num_removed += 1
        # print(self.board)


'''
DO NOT CHANGE
Provided for students
Given a number of rows and number of cells to remove, this function:
1. creates a SudokuGenerator
2. fills its values and saves this as the solved state
3. removes the appropriate number of cells
4. returns the representative 2D Python Lists of the board and solution

Parameters:
size is the number of rows/columns of the board (9 for this project)
removed is the number of cells to clear (set to 0)

Return: list[list] (a 2D Python list to represent the board)
'''

# helps generate sudoku game
def generate_sudoku(size, removed):
  sudoku = SudokuGenerator(size, removed)
  sudoku.fill_values()
  board = sudoku.get_board()
  # print(board)
  sudoku.remove_cells()
  # sudoku.print_board()
  board = sudoku.get_board()
  return board


def remove_num_cells(board, num):
  num_removed = 0
  while num_removed < num:
    row = random.randint(0, 8)
    col = random.randint(0, 8)
    if board[row][col] != 0:
      board[row][col] = 0
      num_removed += 1
      # print(self.board)


# print(generate_sudoku(9, 30))
