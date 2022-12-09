import pygame, sys
from pygame.locals import QUIT
from sudoku_generator import *
from board import Board
from cell import Cell
from constants import *

bg = pygame.image.load("silly_cat2.jpg")


# game_diff = 0
def draw_welcome_screen(screen):
    screen.blit(bg, (0, 0))
    start_title_font = pygame.font.Font(None, 125)
    button_font = pygame.font.Font(None, 75)

    title_surf = start_title_font.render("Silly Cat Sudoku!", 0, BG_COLOR)
    title_rect = title_surf.get_rect(center=(WIDTH // 2, (HEIGHT // 2) - 350))
    screen.blit(title_surf, title_rect)

    easy_text = button_font.render("EASY", 0, LINE_COLOR)
    medium_text = button_font.render("MEDIUM", 0, LINE_COLOR)
    hard_text = button_font.render("SILLY!!!", 0, LINE_COLOR)

    easy_surf = pygame.Surface((easy_text.get_size()[0] + 20, easy_text.get_size()[1] + 20))
    easy_surf.fill(BG_COLOR)
    easy_surf.blit(easy_text, (10, 10))

    medium_surf = pygame.Surface((medium_text.get_size()[0] + 20, medium_text.get_size()[1] + 20))
    medium_surf.fill(BG_COLOR)
    medium_surf.blit(medium_text, (10, 10))

    hard_surf = pygame.Surface((hard_text.get_size()[0] + 20, hard_text.get_size()[1] + 20))
    hard_surf.fill(BG_COLOR)
    hard_surf.blit(hard_text, (10, 10))

    easy_rect = easy_surf.get_rect(
        center=(WIDTH // 2 - 300, HEIGHT // 2 + 150))
    medium_rect = medium_surf.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 + 150))
    hard_rect = hard_surf.get_rect(
        center=(WIDTH // 2 + 300, HEIGHT // 2 + 150))

    screen.blit(easy_surf, easy_rect)
    screen.blit(medium_surf, medium_rect)
    screen.blit(hard_surf, hard_rect)

    while True:  # makes the menu buttons interactable, need to link these to the difficulty
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(event.pos):
                    game_diff = 30
                    return game_diff
                elif medium_rect.collidepoint(event.pos):
                    game_diff = 40
                    return game_diff
                elif hard_rect.collidepoint(event.pos):
                    game_diff = 50
                    return game_diff
        pygame.display.update()


def draw_game_over(screen):
    print("you lose!")
    screen.blit(bg, (0,0))
    button_font = pygame.font.Font(None, 75)
    lose_text_font = pygame.font.Font(None, 125)
    title_surf = lose_text_font.render("Game Over :(", 0, (255,0,0))
    title_rect = title_surf.get_rect(center=(WIDTH // 2, (HEIGHT // 2) - 350))
    screen.blit(title_surf, title_rect)

    restart_text = button_font.render("RESTART", 0, LINE_COLOR)
    restart_surf = pygame.Surface((restart_text.get_size()[0] + 20, restart_text.get_size()[1] + 20))
    restart_surf.fill(BG_COLOR)
    restart_surf.blit(restart_text, (10, 10))

    restart_rect = restart_surf.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 + 150))

    screen.blit(restart_surf, restart_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_rect.collidepoint(event.pos):
                    return
        pygame.display.update()

def draw_game_won(screen):
    print("you won!")
    screen.blit(bg, (0,0))
    button_font = pygame.font.Font(None, 75)
    win_text_font = pygame.font.Font(None, 125)
    win_surf = win_text_font.render("Game Won!", 0, (0,255,0))
    win_rect = win_surf.get_rect(center=(WIDTH // 2, (HEIGHT // 2) - 350))
    screen.blit(win_surf, win_rect)

    win_text = button_font.render("EXIT", 0, LINE_COLOR)
    win_surf = pygame.Surface((win_text.get_size()[0] + 20, win_text.get_size()[1] + 20))
    win_surf.fill(BG_COLOR)
    win_surf.blit(win_text, (10, 10))

    win_rect = win_surf.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 + 150))

    screen.blit(win_surf, win_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit
            if event.type == pygame.MOUSEBUTTONDOWN:
                if win_rect.collidepoint(event.pos):
                    pygame.quit()
        pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Silly Cat Sudoku")

    game_diff = draw_welcome_screen(screen)

    screen.fill(BG_COLOR)

    sudoku = generate_sudoku(9, game_diff)
    print(sudoku)

    board = Board(WIDTH, HEIGHT, screen, game_diff)
    board.draw()

    game_over = False



while True:
    # screen.blit(bg,(0,0))
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos
            row, col = board.click(x, y)
            board.select(row, col)
            board.draw()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                board.sketch(1)
            if event.key == pygame.K_2:
                board.sketch(2)
            if event.key == pygame.K_3:
                board.sketch(3)
            if event.key == pygame.K_4:
                board.sketch(4)
            if event.key == pygame.K_5:
                board.sketch(5)
            if event.key == pygame.K_6:
                board.sketch(6)
            if event.key == pygame.K_7:
                board.sketch(7)
            if event.key == pygame.K_8:
                board.sketch(8)
            if event.key == pygame.K_9:
                board.sketch(9)
            if event.key == pygame.K_RETURN:
                board.place_number()
            if event.key == pygame.K_BACKSPACE:
                board.clear()

            if event.key == pygame.K_r:
              board.board = board.og_board
              board.cells = [[Cell(board.board[i][j], i, j, screen)for j in range(board.width)] for i in range(board.height)]
              print(board.complete_board)
              board.draw
              


            if event.key == pygame.K_m:
              game_diff = draw_welcome_screen(screen)
              
              screen.fill(BG_COLOR)
          
              sudoku = generate_sudoku(9, game_diff)
              print(sudoku)
              
              board = Board(WIDTH, HEIGHT, screen, game_diff)
              board.draw()

            if event.key == pygame.K_w:
              draw_game_won(screen)

              
            elif event.key == pygame.K_l:
              pygame.quit()

            

              
        if board.is_full():
          board.update_board()
          
          if board.check_board():
            
              game = draw_game_won(screen)
              game_over = True
            
          else:
              game = draw_game_over(screen)

              game_diff = draw_welcome_screen(screen)

              screen.fill(BG_COLOR)
          
              sudoku = generate_sudoku(9, game_diff)
              print(sudoku)
          
              board = Board(WIDTH, HEIGHT, screen, game_diff)
              board.draw()
            
              
              game_over = False

          
          
          
    pygame.display.update()

