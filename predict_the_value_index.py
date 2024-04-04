import pygame
import random
from pymongo import MongoClient
import time
from math import sqrt

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Predict the Value Index")

# MongoDB Atlas Connection
CONNECTION_STRING = "mongodb://localhost:27017"
client = MongoClient(CONNECTION_STRING)
db = client.pdsa
collection = db.user_data

# Define colors
BACKGROUND_COLOR = (240, 240, 240)
BUTTON_COLOR = (64, 128, 255)
BUTTON_HOVER_COLOR = (96, 160, 255)
BUTTON_TEXT_COLOR = (255, 255, 255)
TEXT_COLOR = (64, 64, 64)

# Define fonts
FONT_LARGE = pygame.font.Font(None, 36)
FONT_MEDIUM = pygame.font.Font(None, 24)
FONT_SMALL = pygame.font.Font(None, 18)


# Function to generate random numbers
def generate_random_numbers():
    numbers = [random.randint(1, 1000000) for _ in range(5000)]
    return numbers


# Function to perform binary search
def binary_search(arr, x):
    start = time.time()
    low = 0
    high = len(arr) - 1
    mid = 0

    while low <= high:
        mid = (low + high) // 2

        if arr[mid] < x:
            low = mid + 1

        elif arr[mid] > x:
            high = mid - 1

        else:
            break

    end = time.time()
    return mid, end - start


# Function to perform jump search
def jump_search(arr, x):
    start = time.time()
    n = len(arr)
    step = int(sqrt(n))
    prev = 0

    while arr[min(step, n) - 1] < x:
        prev = step
        step += int(sqrt(n))
        if prev >= n:
            return -1, time.time() - start

    while arr[prev] < x:
        prev += 1
        if prev == min(step, n):
            return -1, time.time() - start

    if arr[prev] == x:
        return prev, time.time() - start

    return -1, time.time() - start


# Function to perform exponential search
def exponential_search(arr, x):
    start = time.time()
    n = len(arr)
    if arr[0] == x:
        return 0, time.time() - start

    i = 1
    while i < n and arr[i] <= x:
        i *= 2

    return binary_search(arr, x)


# Function to perform Fibonacci search
def fibonacci_search(arr, x):
    start = time.time()
    n = len(arr)
    fibM_minus_2 = 0
    fibM_minus_1 = 1
    fibM = fibM_minus_2 + fibM_minus_1

    while fibM < n:
        fibM_minus_2 = fibM_minus_1
        fibM_minus_1 = fibM
        fibM = fibM_minus_2 + fibM_minus_1

    offset = -1

    while fibM > 1:
        i = min(offset + fibM_minus_2, n - 1)

        if arr[i] < x:
            fibM = fibM_minus_1
            fibM_minus_1 = fibM_minus_2
            fibM_minus_2 = fibM - fibM_minus_1
            offset = i

        elif arr[i] > x:
            fibM = fibM_minus_2
            fibM_minus_1 = fibM_minus_1 - fibM_minus_2
            fibM_minus_2 = fibM - fibM_minus_1

        else:
            return i, time.time() - start

    if fibM_minus_1 and arr[offset + 1] == x:
        return offset + 1, time.time() - start

    return -1, time.time() - start


# Function to display the game menu
def display_menu():
    display.fill(BACKGROUND_COLOR)
    title = FONT_LARGE.render("Predict the Value Index", True, TEXT_COLOR)
    display.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 50))

    play_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 25, 200, 50)
    pygame.draw.rect(display, BUTTON_COLOR, play_button)
    play_text = FONT_MEDIUM.render("Play", True, BUTTON_TEXT_COLOR)
    display.blit(play_text, (WINDOW_WIDTH // 2 - play_text.get_width() // 2, WINDOW_HEIGHT // 2 - play_text.get_height() // 2))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button.collidepoint(mouse_pos):
                    play_game()


# Function to display the game
def play_game():
    # Generate random numbers
    numbers = generate_random_numbers()

    # Sort the list for searching
    numbers.sort()

    # Perform searches and record data
    search_data = []
    for search_func in [binary_search, jump_search, exponential_search, fibonacci_search]:
        random_value = random.randint(1, 1000000)
        index, time_taken = search_func(numbers, random_value)
        search_data.append((search_func.__name__, index, time_taken))

    # Select a random value for prediction
    prediction_value = random.randint(1, 1000000)
    prediction_index = binary_search(numbers, prediction_value)[0]

    # Generate prediction choices
    choices = [prediction_index]
    while len(choices) < 4:
        choice = random.randint(0, len(numbers) - 1)
        if choice not in choices:
            choices.append(choice)
    random.shuffle(choices)

    # Display search results and prediction
    display.fill(BACKGROUND_COLOR)
    title = FONT_LARGE.render("Search Results", True, TEXT_COLOR)
    display.blit(title, (50, 50))

    y = 100
    for data in search_data:
        result = FONT_MEDIUM.render(f"{data[0]}: Index = {data[1]}, Time Taken = {data[2]:.6f} seconds", True, TEXT_COLOR)
        display.blit(result, (100, y))
        y += 30

    prediction_text = FONT_LARGE.render(f"Predict the index of value {prediction_value}:", True, TEXT_COLOR)
    display.blit(prediction_text, (50, y + 50))

    y += 100
    for i, choice in enumerate(choices):
        choice_text = FONT_MEDIUM.render(f"{i + 1}. {choice}", True, TEXT_COLOR)
        choice_rect = pygame.Rect(100, y, choice_text.get_width() + 20, choice_text.get_height() + 10)
        pygame.draw.rect(display, BUTTON_COLOR, choice_rect)
        display.blit(choice_text, (105, y + 5))
        y += 50

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, choice in enumerate(choices):
                    choice_rect = pygame.Rect(100, 300 + i * 50, 200, 40)
                    if choice_rect.collidepoint(mouse_pos):
                        if i == choices.index(prediction_index):
                            # User predicted correctly
                            result_text = FONT_LARGE.render("Correct!", True, (0, 200, 0))
                            display.blit(result_text, (WINDOW_WIDTH // 2 - result_text.get_width() // 2, WINDOW_HEIGHT - 100))

                            # Get user name and save data
                            name = FONT_MEDIUM.render("Enter your name:", True, TEXT_COLOR)
                            display.blit(name, (WINDOW_WIDTH // 2 - name.get_width() // 2, WINDOW_HEIGHT - 200))
                            pygame.display.update()

                            user_name = ""
                            while True:
                                event = pygame.event.wait()
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    quit()
                                elif event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_RETURN:
                                        break
                                    elif event.key == pygame.K_BACKSPACE:
                                        user_name = user_name[:-1]
                                    else:
                                        user_name += event.unicode

                                    text = FONT_SMALL.render(user_name, True, TEXT_COLOR)
                                    display.fill(BACKGROUND_COLOR, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 150, 200, 50))
                                    display.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT - 150))
                                    pygame.display.update()

                            collection.insert_one({"name": user_name, "correct_answer": 1})
                        else:
                            # User predicted incorrectly
                            result_text = FONT_LARGE.render("Incorrect!", True, (200, 0, 0))
                            display.blit(result_text, (WINDOW_WIDTH // 2 - result_text.get_width() // 2, WINDOW_HEIGHT - 100))
                            collection.insert_one({"name": "Anonymous", "correct_answer": 0})

                        pygame.display.update()
                        pygame.time.delay(2000)
                        display_menu()


# Start the game
display_menu()

# Close the database connection
client.close()
