from queue import PriorityQueue

def a_star_tsp(locations, start):
    """Find the shortest path that visits all locations exactly once."""

    pq = PriorityQueue()
    pq.put((0, [start]))
    
    while not pq.empty():
        
        # path : is list of all visited nodes beginning with the start node
        current_cost, path = pq.get()
        
        if len(path) == len(locations):
            # If all nodes are visited TSP is solved
            path.append(start)
            return path
        
        
        for neighbor in locations:
            # pick up the next location from the given list of locations
            if neighbor not in path:
            
                new_path = path + [neighbor]
                priority = current_cost + distance(path[-1], neighbor) + heuristic(locations, neighbor, start)
                pq.put((priority, new_path))
    
    return None


def cost(path):
    """Calculate the total current cost form the start till current node"""
    total = 0
    for i in range(len(path) - 1):
        total += distance(path[i], path[i+1])
    # Add distance from last node back to start node
    total += distance(path[-1], path[0])
    return total


def heuristic(locations, current, start):
    """
    Calculates the heuristic based on the unvisited nodes
    My heuristic is calculated by checking the minimium distance from current node to the unvisited locations
    """
    unvisited = locations[:]
    unvisited.remove(current)
    unvisited.remove(start)
    return distance(current, start) + sum(min(distance(current, location) for location in unvisited) for current in [start, current])

def distance(a, b):
    """Calculate the Euclidean distance between two points."""
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2) ** 0.5


import matplotlib.pyplot as plt

def visualize_path(locations, path):
    """
    Visualizes the final path on a 2D plane.
    """
    x_coords = [location[0] for location in locations]
    y_coords = [location[1] for location in locations]
    labels = [str(i) for i in range(len(locations))]
    
    # plot locations as circles with labels
    fig, ax = plt.subplots()
    ax.scatter(x_coords, y_coords)
    for i, label in enumerate(labels):
        ax.annotate(label, (x_coords[i], y_coords[i]))
    
    # plot final path as lines connecting circles
    for i in range(len(path) - 1):
        ax.plot([path[i][0], path[i+1][0]], [path[i][1], path[i+1][1]], 'r')
    ax.plot([path[-1][0], path[0][0]], [path[-1][1], path[0][1]], 'r')
    
    plt.show()

def test_complex_search():
    # Define a test case with a more complex graph
    start = (0, 0)
    nodes = [(1, 1), (2, 3), (4, 2), (3, 5), (5, 5), (6, 1), (8, 3)]
    expected_path = [(0, 0), (1, 1), (4, 2), (2, 3), (3, 5), (5, 5), (8, 3), (6, 1), (0, 0)]
    expected_cost = 23.79226040123602
    # Run the A* search algorithm on the test case
    result = a_star_tsp(start, nodes)
    # Assert that the result matches the expected path and cost
    assert result == expected_path and cost(result) == expected_cost, f"Expected ({expected_path}, {expected_cost}), but got ({result}, {cost(result)})"

def test_long_search():
    # Define a test case with a larger number of nodes
    start = (0, 0)
    nodes = [(i, i**2) for i in range(1, 21)]
    expected_path = [(0, 0), (1, 1), (2, 4), (3, 9), (4, 16), (5, 25), (6, 36), (7, 49), (8, 64), (9, 81), (10, 100), (11, 121), (12, 144), (13, 169), (14, 196), (15, 225), (16, 256), (17, 289), (18, 324), (19, 361), (20, 400), (0, 0)]
    expected_cost = 483.34268976007935
    # Run the A* search algorithm on the test case
    result = a_star_tsp(start, nodes)
    # Assert that the result matches the expected path and cost
    assert result == expected_path and cost(result) == expected_cost, f"Expected ({expected_path}, {expected_cost}), but got ({result}, {cost(result)})"

def test_repeated_nodes():
    # Define a test case with repeated nodes
    start = (0, 0)
    nodes = [(1, 1), (1, 1), (2, 3), (4, 2), (4, 2), (3, 5)]
    expected_path = [(0, 0), (1, 1), (2, 3), (4, 2), (3, 5), (0, 0)]
    expected_cost = 11.398040756314787
    # Run the A* search algorithm on the test case
    result = a_star_tsp(start, nodes)
    # Assert that the result matches the expected path and cost
    assert result == expected_path and cost(result) == expected_cost, f"Expected ({expected_path}, {expected_cost}), but got ({result}, {cost(result)})"


locations = [(1,1), (0,0), (2,2), (3,3), (4,4)]
start = (0,0)
expected_path = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (0,0)]

# Test the search function
result = a_star_tsp(locations, start)

# visualize_path(locations, result)
print(result)
print(result, cost(result))
assert result == expected_path, f"Expected {expected_path}, but got {result}"

# Test the distance functionit 
result = distance((0,0), (3,3))
assert result == 4.242640687119285, f"Expected 4.242640687119285, but got {result}"

nodes = [(0, 0), (1, 2), (3, 1), (5, 4)]
start = (0, 0)

# Expected output: [(0, 0), (1, 2), (3, 1), (5, 4), (0, 0)]
print(a_star_tsp(nodes, start))
start = (0, 0)
nodes = [(1, 1), (2, 3), (4, 2), (3, 5), (5, 5), (6, 1), (8, 3), (0,0)]
expected_path = [(0, 0), (1, 1), (4, 2), (2, 3), (3, 5), (5, 5), (8, 3), (6, 1), (0, 0)]
result = a_star_tsp(nodes, start)

visualize_path(nodes, result)
# assert result == expected_path, f"Expected {expected_path}, but got {result}" 
# test_complex_search()
# test_long_search()
# test_repeated_nodes()