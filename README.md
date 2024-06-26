# Eight Queens Puzzle

## 3.1.1. Explain the Program Logic used to solve the problem

The program uses a recursive backtracking algorithm to solve the Eight Queens Puzzle. The `solve_queens` function is responsible for finding all possible solutions. It starts by placing a queen in the first column and recursively tries to place the remaining queens in the subsequent columns. The `is_safe` function checks if a queen can be placed on a given position by ensuring that it does not conflict with any previously placed queens in the same row, column, or diagonal.

![Eight Queens Puzzle UI](assets/eight_queens_puzzle.gif)

## 3.1.4. Explain the Validations and Exception Handling in this application.

The application performs input validation to ensure that the player enters a valid name. It also handles the `pygame.QUIT` event to gracefully exit the application when the user closes the window. Additionally, it catches any exceptions that may occur during the game loop and handles them appropriately.

## 3.1.5. Code Segment screenshots: unit Testing

[Test](https://github.com/sahanruwantha/PDSA_ASSIGNMENT/blob/main/tests/test_eight_queens_puzzle.py)

## 3.1.6. Indicate the Data Structures used and Explain its purpose

The program uses a 2D list (`board`) to represent the chessboard. Each element in the list represents a square on the board, and its value is either 0 (empty) or 1 (queen placed). The `solutions` list is used to store all the valid solutions found by the backtracking algorithm.


# 3.2. Tic-Tac-Toe

## 3.2.1. Explain the Program Logic used to solve the problem

The program implements a Tic-Tac-Toe game where the player competes against an AI opponent. The AI uses the Minimax algorithm with alpha-beta pruning to make optimal moves. The algorithm recursively explores all possible game states and evaluates the best move based on a scoring system (-1 for a loss, 0 for a tie, and 1 for a win).

![Tic-Tac-Toe GIF](assets/tik_tak_toe.gif)

## 3.2.4. Explain the Validations and Exception Handling in this application.

The application validates the user's input for the username and handles the `pygame.QUIT` event to gracefully exit the application. It also catches any exceptions that may occur during the game loop or database operations and handles them appropriately.

## 3.2.5. Code Segment screenshots: unit Testing

[Test](https://github.com/sahanruwantha/PDSA_ASSIGNMENT/blob/main/tests/test_tic_tac_toe.py)

## 3.2.6. Indicate the Data Structures used and purpose

The program uses a list (`board`) to represent the Tic-Tac-Toe board. Each element in the list corresponds to a cell on the board and can have a value of ' ' (empty), 'X' (player's move), or 'O' (computer's move).

## 3.2.7. Screenshot of the Normalized DB Table Structure used for this Game Option

# 3.3. Identify Shortest Path

## 3.3.1. Explain the Program Logic used to solve the problem

The program generates a random set of cities with randomly assigned distances between them. It then allows the player to select two cities by clicking on them. The program uses Dijkstra's algorithm to calculate the shortest path between the selected cities. The player is prompted to enter the correct shortest distance, and their response is recorded.

![Identify Shortest Path GIF](assets/identify_shortest_path.gif)


## 3.3.4. Explain the Validations and Exception Handling in this application.

The application handles the `pygame.QUIT` event to gracefully exit the application. It also validates the player's input for the shortest distance and handles any non-numeric input appropriately.

## 3.3.5. Code Segment screenshots: unit Testing

[Test](https://github.com/sahanruwantha/PDSA_ASSIGNMENT/blob/main/tests/test_identify_shortest_path.py)

## 3.3.6. Indicate the Data Structures used with its purpose

The program uses a dictionary (`distances`) to store the distances between cities. The keys of the dictionary are the city names, and the values are nested dictionaries containing the distances to other cities.


## 3.3.8. Compare the Shortest path identifying algorithms (logic/complexity, which scenarios are best to use it, etc.)

## 3.3.8. Compare the Shortest path identifying algorithms (logic/complexity, which scenarios are best to use it, etc.)

**1. Dijkstra's Algorithm**:
- **Logic**: Dijkstra's algorithm is a greedy algorithm that finds the shortest path between a single source node and all other nodes in a weighted graph. It works by maintaining a set of visited nodes and a priority queue of unvisited nodes. At each iteration, the algorithm selects the unvisited node with the smallest distance from the source and marks it as visited. It then updates the distances to all unvisited neighbors of the current node.
- **Time Complexity**: The time complexity of Dijkstra's algorithm is O((V+E) log V), where V is the number of vertices (cities), and E is the number of edges (connections between cities). This complexity assumes the use of a binary heap or Fibonacci heap for the priority queue.
- **Best Scenarios**: Dijkstra's algorithm is suitable for graphs with non-negative edge weights (distances). It is commonly used in various applications, such as network routing, GPS navigation, and social network analysis.

**2. Bellman-Ford Algorithm**:
- **Logic**: The Bellman-Ford algorithm is a dynamic programming algorithm that finds the shortest path between a single source node and all other nodes in a weighted graph. It works by repeatedly updating the distances to all nodes based on the distances of their neighbors. The algorithm performs V-1 iterations, where V is the number of vertices.
- **Time Complexity**: The time complexity of the Bellman-Ford algorithm is O(VE), where V is the number of vertices (cities), and E is the number of edges (connections between cities).
- **Best Scenarios**: The Bellman-Ford algorithm can handle graphs with negative edge weights, making it suitable for scenarios where negative distances are possible, such as in network routing with link costs or currency arbitrage problems. However, it cannot handle graphs with negative cycles (a cycle with an overall negative weight).

**3. Floyd-Warshall Algorithm**:
- **Logic**: The Floyd-Warshall algorithm is a dynamic programming algorithm that finds the shortest paths between all pairs of nodes in a weighted graph. It works by iteratively updating a distance matrix, considering all possible intermediate nodes between each pair of nodes.
- **Time Complexity**: The time complexity of the Floyd-Warshall algorithm is O(V^3), where V is the number of vertices (cities).
- **Best Scenarios**: The Floyd-Warshall algorithm is useful when you need to find the shortest paths between all pairs of nodes in a graph. It is commonly used in applications such as routing in computer networks, image processing, and data mining.

# 3.4. Remember the Value Index

![Remember the Value Index GIF](assets/remember_the_value_index.gif)

## 3.4.1. UI screenshot allowing game players to provide answers

![Value Index Input](value_index_input.jpg)

## 3.4.4. Compare the sorting techniques (e.g., explain the logic used in the sorting Techniques, determine their complexity, which scenarios are best to use it, etc.).


1. **Bubble Sort**: Compares adjacent elements and swaps them if they are in the wrong order. It has a time complexity of O(n^2), making it inefficient for large datasets.

2. **Insertion Sort**: Builds the final sorted array one element at a time by inserting each element into its correct position in the sorted portion of the array. It has a time complexity of O(n^2) in the worst case and O(n) in the best case when the array is already sorted.

3. **Merge Sort**: Divide the unsorted list into n sublists, each containing one element, and then repeatedly merge the sublists to produce new sorted sublists until there is only one sublist remaining. It has a time complexity of O(n log n) in all cases.

4. **Radix Sort**: Sorts the elements by first grouping them by their most significant digit, then by their second most significant digit, and so on. It has a time complexity of O(kn), where k is the number of digits in the maximum element.

5. **Shell Sort**: An optimization of Insertion Sort that allows the exchange of elements that are far apart. It has a time complexity of O(n^2) in the worst case and O(n log n) in the best case.

6. **Quick Sort**: Selects a "pivot" element from the array and partitions the other elements into two sub-arrays, according to whether they are less than or greater than the pivot. The sub-arrays are then sorted recursively. It has an average time complexity of O(n log n), but a worst-case time complexity of O(n^2) when the array is already sorted or reverse-sorted.

7. **Tim Sort**: A combination of Insertion Sort and Merge Sort. It uses Insertion Sort for small arrays and Merge Sort for larger arrays. It has a time complexity of O(n log n) in the worst case and performs well on sorted and partially sorted data.

The choice of sorting algorithm depends on the size and characteristics of the dataset, as well as the time and space complexity requirements of the application.

# 3.5. Predict the Value Index

![Predict Value Index](assets/predict_the_value_index.gif)

## 3.5.4. Compare the search techniques (e.g., explain the logic used in the search Techniques, determine their complexity, which scenarios are best to use it, etc.).

1. **Binary Search**: Repeatedly divides the search interval in half based on whether the target value is higher or lower than the middle element. It has a time complexity of O(log n) in the average and best cases, but requires the input array to be sorted.

2. **Jump Search**: Jumps ahead by a fixed step size and then performs a linear search around the nearest element to the target value. It has a time complexity of O(√n) in the best case and O(n) in the worst case.

3. **Exponential Search**: Finds a range where the target value might exist by exponentially increasing the search range until it exceeds the target value. It then performs a binary search on the found range. Its time complexity is O(log n) in the best case and O(log n) in the worst case.

4. **Fibonacci Search**: Similar to Binary Search, but uses Fibonacci numbers to determine the next search interval instead of dividing the interval in half. It has a time complexity of O(log n) in the average and best cases, but requires the input array to be sorted.

The choice of search technique depends on the characteristics of the dataset, such as whether it is sorted or unsorted, and the time complexity requirements of the application. Binary Search and Fibonacci Search are efficient for sorted arrays, while Jump Search and Exponential Search can be useful for partially sorted or unsorted arrays.
