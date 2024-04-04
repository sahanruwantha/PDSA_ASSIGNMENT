import pygame
import sys
import time

# Initialize Pygame font module
pygame.font.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLUE = (65, 105, 225)  # Updated color
ORANGE = (255, 165, 0)  # Updated color
RED = (255, 0, 0)

# Define font
FONT = pygame.font.Font(None, 36)

# Define board size
BOARD_SIZE = 8
SQUARE_SIZE = 0  # Initialize to 0, will be set later

# Define solutions
solutions = []
max_solutions = 92  # Maximum number of solutions for the Eight Queens' Puzzle
solved_solutions = []  # List to store solved solutions and player names

def input_text(prompt, board):  # Added board as an argument
    text = ""
    input_rect = pygame.Rect(240, 200, 320, 50)  # Adjust the size and position as needed
    active = False

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif event.key == pygame.K_RETURN:
                        return text
                    else:
                        text += event.unicode

        SCREEN.fill(WHITE)
        draw_board()
        draw_queens(board)  # board is now passed as an argument

        # Render the prompt
        prompt_text = FONT.render(prompt, True, BLACK)
        SCREEN.blit(prompt_text, (240, 150))

        # Render the text input box
        color = BLACK if active else GRAY
        pygame.draw.rect(SCREEN, color, input_rect, 2)
        text_surface = FONT.render(text, True, BLACK)  # Text color is black
        SCREEN.blit(text_surface, (input_rect.x + 10, input_rect.y + 10))

        pygame.display.update()

# Define function to draw the board
def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = WHITE if (row + col) % 2 == 0 else GRAY
            pygame.draw.rect(
                SCREEN,
                color,
                (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                border_radius=5,  # Rounded corners for a modern look
            )

# Define function to draw the queens
def draw_queens(board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == 1:
                x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                pygame.draw.circle(SCREEN, BLUE, (x, y), SQUARE_SIZE // 4)  # Change color to blue

# Define function to check if a queen can be placed on the board
def is_safe(board, row, col):
    # Check the row on the left side
    for i in range(col):
        if board[row][i] == 1:
            return False

    # Check the upper diagonal on the left side
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    # Check the lower diagonal on the left side
    for i, j in zip(range(row, BOARD_SIZE, 1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    return True

# Define function to solve the Eight Queens' Puzzle
def solve_queens(board, col):
    global solutions
    # Base case: If all queens are placed, return True
    if col == BOARD_SIZE:
        solutions.append([row[:] for row in board])
        return True

    # Consider this column and try placing this queen in all rows one by one
    result = False
    for row in range(BOARD_SIZE):
        if is_safe(board, row, col):
            board[row][col] = 1
            # Recur to place rest of the queens
            result = solve_queens(board, col + 1) or result
            # If placing queen in board[row][col] doesn't lead to a solution, remove the queen
            board[row][col] = 0

    return result

# Define function to display a message
def display_message(text, color):
    message = FONT.render(text, True, color)
    message_rect = message.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    pygame.draw.rect(SCREEN, WHITE, message_rect.inflate(10, 10))  # White background for the message
    SCREEN.blit(message, message_rect)
    pygame.display.update()
    time.sleep(0.5)  # Message will fade away after 3 seconds

# Define function to handle user input
def handle_input(board):
    global solutions, solved_solutions
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            row = mouse_y // SQUARE_SIZE
            col = mouse_x // SQUARE_SIZE
            if board[row][col] == 0:
                board[row][col] = 1
                solutions = []  # Reset the solutions list
                solve_queens(board, 0)  # Find new solutions
                if len(solutions) == max_solutions:
                    display_message("Congratulations! You've found all solutions.", BLUE)  # Change color to blue
                    # Clear the flag for solved solutions
                    solved_solutions.clear()
                else:
                    # Check if the current solution is already solved
                    board_str = ''.join(map(str, sum(board, [])))
                    if board_str in [s[0] for s in solved_solutions]:
                        display_message("This solution has already been solved.", RED)
                    else:
                        display_message("Solution accepted! Player: " + player_name, ORANGE)  # Change color to orange
                        solved_solutions.append((board_str, player_name))
            else:
                board[row][col] = 0
                solutions = []  # Reset the solutions list

# Define function to initialize module
def initialize_module(main_window):
    global SCREEN, WINDOW_WIDTH, WINDOW_HEIGHT, player_name
    SCREEN = main_window
    WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_surface().get_size()
    global SQUARE_SIZE
    SQUARE_SIZE = WINDOW_WIDTH // BOARD_SIZE
    player_name = input_text("Enter your name: ", [[0]*8]*8)

# Define function to run the Eight Queens puzzle
def run_eight_queens(window):
    initialize_module(window)

    # Create an empty board
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    # Game loop
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)  # Limit the frame rate to 60 FPS
        SCREEN.fill(WHITE)
        draw_board()
        draw_queens(board)
        handle_input(board)
        pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    WINDOW_WIDTH = 800  # Set your desired window width
    WINDOW_HEIGHT = 800  # Set your desired window height
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Eight Queens Puzzle")
    run_eight_queens(SCREEN)
