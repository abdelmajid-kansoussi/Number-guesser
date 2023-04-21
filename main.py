import pygame, sys, joblib, sklearn
import numpy as np
from pygame.locals import *
import warnings

warnings.filterwarnings('ignore')

SQUARE_SIZE = 20
ROWS = 28
COLUMNS = 28
WINDOW_WIDTH = SQUARE_SIZE * ROWS
WINDOW_HEIGHT = SQUARE_SIZE * COLUMNS
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def main():
    global DISPLAY_SURF
    pygame.init()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Number guesser")
    CLOCK = pygame.time.Clock()

    board = get_starting_board()
    is_mouse_pressed = False

    print("Welcome to Number Guesser!")
    print("Usage:") 
    print("- Draw a digit between 0 and 9")
    print("- Press Enter and the program will try to guess the digit you draw")
    print("- Press Backspace to erase the board")


    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP:
                is_mouse_pressed = not is_mouse_pressed


            elif event.type == MOUSEMOTION and is_mouse_pressed:
                paint(event.pos[1], event.pos[0], board)

            elif event.type == KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pred = str(predict(board))
                    print("I guess you draw: " + pred)
                if event.key == pygame.K_BACKSPACE:
                    erase_board(board)
 

        draw_board(board)
        pygame.display.update()
        CLOCK.tick(FPS)


def draw_board(board):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == 0:
                pygame.draw.rect(DISPLAY_SURF, WHITE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            else:
                pygame.draw.rect(DISPLAY_SURF,  BLACK, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def get_clicked_square(left, top):
    row = top // SQUARE_SIZE
    col = left // SQUARE_SIZE
    return (row, col)


def erase_board(board):
    board = get_starting_board()


def predict(board):
    X = np.array(board).reshape((1, ROWS * COLUMNS))
    model = joblib.load("model.pkl")
    pred = model.predict(X)[0]
    return pred


def get_starting_board():
    board = []
    for i in range(ROWS):
        row = []
        for j in range(COLUMNS):
            row.append(0)
        board.append(row)
    return board


def paint(mouse_left, mouse_top, board):
    row, col = get_clicked_square(mouse_left, mouse_top)
    squares = [(row - 1, col - 1), 
               (row - 1, col), 
               (row - 1, col + 1),
               (row, col - 1), 
               (row, col), 
               (row, col + 1),
               (row + 1, col - 1), 
               (row + 1, col), 
               (row + 1, col + 1)]
    for square in squares:
        row, col = square
        if row >= 0 and row < ROWS and col >= 0 and col <= COLUMNS:
            board[row][col] = 1

main()
