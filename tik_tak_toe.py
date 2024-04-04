import pygame
import sys
import random
import math
from datetime import datetime
from pymongo import MongoClient

# Initialize Pygame
pygame.init()

# Set up the game window
WINDOW_SIZE = (600, 600)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Tic Tac Toe")

# Define colors
BACKGROUND_COLOR = (36, 36, 36)
GRID_COLOR = (200, 200, 200)
X_COLOR = (255, 153, 51)  # Orange
O_COLOR = (51, 204, 51)   # Green
WINNER_COLOR = (255, 102, 102)
TEXT_COLOR = (255, 255, 255)
INPUT_COLOR = (240, 240, 240)
INPUT_BORDER_COLOR = (100, 100, 100)
SHADOW_COLOR = (100, 100, 100)

# Define the game board
board = [' ' for _ in range(9)]

# Define the players
HUMAN = 'X'
COMPUTER = 'O'

# Define the game state
GAME_OVER = False
WINNER = None

# Define the font
FONT = pygame.font.Font(None, 72)
SMALL_FONT = pygame.font.Font(None, 36)

# MongoDB Atlas Connection
CONNECTION_STRING = "mongodb://localhost:27017"
client = MongoClient(CONNECTION_STRING)
db = client.pdsa
collection = db.tictactoe

# Function to draw the game board
def draw_board():
    WINDOW.fill(BACKGROUND_COLOR)
    cell_width = WINDOW_SIZE[0] // 3
    cell_height = WINDOW_SIZE[1] // 3

    # Draw vertical lines
    for i in range(1, 3):
        pygame.draw.line(WINDOW, GRID_COLOR, (i * cell_width, 0), (i * cell_width, WINDOW_SIZE[1]), 5)

    # Draw horizontal lines
    for i in range(1, 3):
        pygame.draw.line(WINDOW, GRID_COLOR, (0, i * cell_height), (WINDOW_SIZE[0], i * cell_height), 5)

    # Draw X's and O's
    for i in range(9):
        x = (i % 3) * cell_width + cell_width // 2
        y = (i // 3) * cell_height + cell_height // 2
        if board[i] == 'X':
            draw_x(x, y, X_COLOR, cell_width, cell_height)
        elif board[i] == 'O':
            draw_o(x, y, O_COLOR)

# Function to draw an X
def draw_x(x, y, color, cell_width, cell_height):
    line_width = 18
    pygame.draw.line(WINDOW, color, (x - cell_width // 3, y - cell_height // 3), (x + cell_width // 3, y + cell_height // 3), line_width)
    pygame.draw.line(WINDOW, color, (x + cell_width // 3, y - cell_height // 3), (x - cell_width // 3, y + cell_height // 3), line_width)

# Function to draw an O
def draw_o(x, y, color):
    pygame.draw.circle(WINDOW, color, (x, y), 36, 18)

# Function to check for a winner
def check_winner():
    global WINNER, GAME_OVER
    # Check rows
    for i in range(0, 9, 3):
        if board[i] == board[i + 1] == board[i + 2] != ' ':
            WINNER = board[i]
            GAME_OVER = True
            return WINNER
    # Check columns
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] != ' ':
            WINNER = board[i]
            GAME_OVER = True
            return WINNER
    # Check diagonals
    if board[0] == board[4] == board[8] != ' ':
        WINNER = board[0]
        GAME_OVER = True
        return WINNER
    if board[2] == board[4] == board[6] != ' ':
        WINNER = board[2]
        GAME_OVER = True
        return WINNER
    # Check for a tie
    if ' ' not in board:
        GAME_OVER = True
        return None

def minimax(board, depth, is_maximizing):
    # Check for a winner or a tie
    result = check_winner()
    if result != None:
        if result == 'X':
            return -1
        elif result == 'O':
            return 1
        else:
            return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = COMPUTER
                score = minimax(board, depth + 1, False)
                board[i] = ' '
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == ' ':
                board[i] = HUMAN
                score = minimax(board, depth + 1, True)
                board[i] = ' '
                best_score = min(best_score, score)
        return best_score

def computer_move():
    # Implement an intelligent move by considering corners, center, and edges
    corners = [0, 2, 6, 8]
    edges = [1, 3, 5, 7]
    center = 4

    # Prioritize corner, center, and edges moves
    for move in [corners, [center], edges]:
        for pos in move:
            if board[pos] == ' ':
                board[pos] = COMPUTER
                return

def run_tic_tac_toe():
    global GAME_OVER, WINNER, board
    username = ''
    input_active = True
    input_rect = pygame.Rect(150, 300, 300, 50)  # Input box rect

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode

        WINDOW.fill(BACKGROUND_COLOR)

        # Draw input box
        pygame.draw.rect(WINDOW, INPUT_BORDER_COLOR, input_rect, 3, border_radius=15)
        pygame.draw.rect(WINDOW, INPUT_COLOR, input_rect, border_radius=15)
        input_surface = SMALL_FONT.render(username, True, TEXT_COLOR)
        input_surface_rect = input_surface.get_rect(midleft=(input_rect.x + 15, input_rect.centery))  # Adjusted position
        WINDOW.blit(input_surface, input_surface_rect)

        # Add shadow effect to input box
        shadow_rect = input_rect.move(5, 5)
        pygame.draw.rect(WINDOW, SHADOW_COLOR, shadow_rect, border_radius=15)

        text_surface = SMALL_FONT.render("Enter your username:", True, TEXT_COLOR)
        WINDOW.blit(text_surface, (150, 250))
        pygame.display.update()

    while not GAME_OVER:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row = y // (WINDOW_SIZE[1] // 3)
                col = x // (WINDOW_SIZE[0] // 3)
                index = row * 3 + col
                if board[index] == ' ':
                    board[index] = HUMAN
                    check_winner()
                    if not GAME_OVER:
                        computer_move()
                        check_winner()

        draw_board()

        if GAME_OVER:
            if WINNER is None:
                message = "It's a tie!"
            else:
                message = f"{WINNER} wins!"
                # Save the winner
                # Save the winner's username and correct response in the database
                timestamp = datetime.now()
                data = {
                    "username": username,
                    "correct_response": WINNER,
                    "timestamp": timestamp
                }
                try:
                    collection.insert_one(data)
                    print("Data inserted successfully!")
                except Exception as e:
                    print("Error inserting data:", e)
            text = FONT.render(message, True, WINNER_COLOR)
            text_rect = text.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
            WINDOW.blit(text, text_rect)

            # Fade effect for the winner message
            alpha = 255
            while alpha > 0:
                text.set_alpha(alpha)
                WINDOW.blit(text, text_rect)
                pygame.display.update()
                alpha -= 5
                pygame.time.delay(10)

            # Reset the game
            board = [' ' for _ in range(9)]
            GAME_OVER = False
            WINNER = None

        pygame.display.update()

# Run the game
run_tic_tac_toe()
