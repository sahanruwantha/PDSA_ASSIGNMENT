import pygame
import random
import time
import pymongo

# MongoDB Atlas Connection
CONNECTION_STRING = "mongodb://localhost:27017"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.pdsa
collection = db.predict_value_index

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 30)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Predict the Value Index")

# Function to generate random numbers
def generate_random_numbers():
    return [random.randint(1, 1000) for _ in range(100)]

# Function to perform sorting (e.g., using quicksort)
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

# Function to perform bubble sort
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr  # Return the sorted list

# Function to draw bars representing numbers with smoothing animation
def draw_bars(numbers, color, x_offset, y_offset):
    max_number = max(numbers)
    bar_width = (SCREEN_WIDTH // 2) // len(numbers)
    for i, number in enumerate(numbers):
        bar_height = (number / max_number) * (SCREEN_HEIGHT - 150)
        for height in range(0, int(bar_height), 10):
            pygame.draw.rect(screen, color, (x_offset + i * bar_width, SCREEN_HEIGHT - height - y_offset, bar_width, height))
            pygame.display.flip()
            pygame.time.delay(10)

# Function to record search results in MongoDB
def record_search_result(algorithm, time_taken, index):
    collection.insert_one({
        "algorithm": algorithm,
        "time_taken": time_taken,
        "index": index
    })

# Function to display text on screen
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

# Function to display options for predicting the index
def display_prediction_options(correct_index):
    options = random.sample(range(100), 4)
    options[random.randint(0, 3)] = correct_index
    return options

# Main game loop
def main():
    numbers = generate_random_numbers()
    sorted_numbers_quick = numbers.copy()  # Sort the generated numbers using quicksort
    sorted_numbers_bubble = numbers.copy()  # Sort the generated numbers using bubble sort

    running = True
    while running:
        screen.fill(WHITE)
        draw_text("Predict the Value Index", font, BLACK, SCREEN_WIDTH // 4, 50)
        draw_text("Sorting using Quick Sort", font, BLACK, SCREEN_WIDTH // 4, 100)
        draw_text("Sorting using Bubble Sort", font, BLACK, 3 * SCREEN_WIDTH // 4, 100)

        # Draw bars representing sorted numbers with smoothing animation
        draw_bars(quicksort(sorted_numbers_quick), BLUE, 0, 0)
        draw_bars(bubble_sort(sorted_numbers_bubble), RED, SCREEN_WIDTH // 2, 0)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Select a random number
                target_value = random.choice(numbers)
                correct_index = numbers.index(target_value)

                # Display prediction options
                options = display_prediction_options(correct_index)
                option_texts = [f"{i+1}. Index {option}" for i, option in enumerate(options)]

                # Display target value and prediction options
                screen.fill(WHITE)
                draw_text(f"Target Value: {target_value}", font, BLACK, SCREEN_WIDTH // 2, 50)
                draw_text("Predict the index:", font, BLACK, SCREEN_WIDTH // 2, 150)
                for i, text in enumerate(option_texts):
                    draw_text(text, small_font, BLACK, SCREEN_WIDTH // 2, 200 + i * 50)
                pygame.display.flip()

                # Wait for user input
                prediction = None
                while prediction is None:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            prediction = -1
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_1:
                                prediction = options[0]
                            elif event.key == pygame.K_2:
                                prediction = options[1]
                            elif event.key == pygame.K_3:
                                prediction = options[2]
                            elif event.key == pygame.K_4:
                                prediction = options[3]

                # Check if prediction is correct
                if prediction == correct_index:
                    draw_text("Correct!", font, GREEN, SCREEN_WIDTH // 2, 400)
                else:
                    draw_text("Incorrect!", font, RED, SCREEN_WIDTH // 2, 400)

                # Record the result
                pygame.display.flip()
                pygame.time.delay(2000)

                # Wait for a key press to continue to the next round
                wait_for_key = True
                while wait_for_key:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            wait_for_key = False
                        elif event.type == pygame.KEYDOWN:
                            wait_for_key = False

if __name__ == "__main__":
    main()