import pygame
import random
import time
import math
from pymongo import MongoClient
import bisect

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 87, 87)
GREEN = (0, 255, 123)
GRAY = (189, 189, 189)
BLUE = (0, 179, 229)

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Predict the Value Index")

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Game variables
numbers = []
random_number = None
correct_index = None
text_input = ""
active = False
choices = []
search_results = {}

# MongoDB setup
CONNECTION_STRING = "mongodb://localhost:27017"
client = MongoClient(CONNECTION_STRING)
db = client.pdsa
collection = db.tictactoe

# Function to display text on screen
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Function to display buttons
def draw_button(text, font, color, x, y, width, height):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)

# Function to draw text input box
def draw_input_box(text, font, color, x, y, width, height):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)

# Event handling
def handle_input(events):
    global text_input
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                text_input = text_input[:-1]
            elif event.key == pygame.K_RETURN:
                return True
            else:
                text_input += event.unicode
    return False

# Search functions
def binary_search(arr, x):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] < x:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def jump_search(arr, x):
    n = len(arr)
    step = int(math.sqrt(n))
    prev = 0
    while arr[min(step, n) - 1] < x:
        prev = step
        step += int(math.sqrt(n))
        if prev >= n:
            return -1
    while arr[prev] < x:
        prev += 1
        if prev == min(step, n):
            return -1
    if arr[prev] == x:
        return prev
    return -1

def exponential_search(arr, x):
    n = len(arr)
    if arr[0] == x:
        return 0
    i = 1
    while i < n and arr[i] <= x:
        i *= 2
    return binary_search(arr[:min(i, n)], x)

def fibonacci_search(arr, x):
    fib_m_minus_2 = 0
    fib_m_minus_1 = 1
    fib_curr = fib_m_minus_1 + fib_m_minus_2

    while fib_curr < len(arr):
        fib_m_minus_2 = fib_m_minus_1
        fib_m_minus_1 = fib_curr
        fib_curr = fib_m_minus_1 + fib_m_minus_2

    offset = -1
    while fib_curr > 1:
        i = min(offset + fib_m_minus_2, len(arr) - 1)
        if arr[i] < x:
            fib_curr = fib_m_minus_1
            fib_m_minus_1 = fib_m_minus_2
            fib_m_minus_2 = fib_curr - fib_m_minus_1
            offset = i
        elif arr[i] > x:
            fib_curr = fib_m_minus_2
            fib_m_minus_1 -= fib_m_minus_2
            fib_m_minus_2 = fib_curr - fib_m_minus_1
        else:
            return i
    if fib_m_minus_1 and arr[offset + 1] == x:
        return offset + 1
    return -1

# Function to perform search and record results
def perform_search(search_type, numbers, random_number):
    start_time = time.time()
    index = globals()[search_type](numbers, random_number)
    end_time = time.time()
    search_time = end_time - start_time
    search_results[search_type] = (search_time, index)
    collection.insert_one({"search_type": search_type, "time": search_time, "index": index})

# Main game loop
running = True
while running:
    screen.fill(BLUE)

    # Event handling
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Draw UI elements
    draw_text("Predict the Value Index", font, WHITE, WIDTH // 2, 50)
    draw_button("Play", font, GREEN, 150, 400, 200, 50)
    draw_button("Exit", font, RED, 450, 400, 200, 50)

    # Handle user input
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if 150 <= mouse[0] <= 350 and 400 <= mouse[1] <= 450 and click[0] == 1:
        numbers = sorted(random.sample(range(1, 1000001), 5000))
        random_number = random.randint(1, 1000000)
        correct_index = bisect.bisect_left(numbers, random_number)
        choices = [correct_index, random.randint(0, len(numbers) - 1),
                   random.randint(0, len(numbers) - 1), random.randint(0, len(numbers) - 1)]
        random.shuffle(choices)
        active = True
        search_results = {}  # Reset search results for each round

    elif 450 <= mouse[0] <= 650 and 400 <= mouse[1] <= 450 and click[0] == 1:
        running = False

    # Perform searches if playing
    if active:
        for search_type in ["binary_search", "jump_search", "exponential_search", "fibonacci_search"]:
            perform_search(search_type, numbers.copy(), random_number)  # Use a copy to avoid modifying original list

        # Draw choices
        for i, choice in enumerate(choices):
            draw_text(f"{i + 1}. {choice}", font, WHITE, 250, 200 + i * 50)

        # Draw text input box
        draw_input_box(text_input, small_font, WHITE, WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        if handle_input(events):
            if text_input.isdigit() and 1 <= int(text_input) <= 4:
                user_choice = int(text_input) - 1
                if choices[user_choice] == correct_index:
                    user_name = text_input
                    correct_response = choices[user_choice]
                    print("Your name and correct response have been recorded.")
                    for search_type, (search_time, index) in search_results.items():
                        print(f"{search_type}: Time = {search_time:.4f}, Index = {index}")
                    collection.insert_one({"search_type": "User Input", "time": 0, "index": user_choice})
                else:
                    print("Sorry, incorrect choice.")
            text_input = ""  # Clear text input after processing

    # Update display
    pygame.display.update()

# Quit Pygame
pygame.quit()
