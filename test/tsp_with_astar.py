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
    unvisited = [location for location in locations if location != current]
    
    if not unvisited:
        return distance(current, start)
    
    return min(distance(current, location) for location in unvisited)         


def distance(a, b):
    """Calculate the Euclidean distance between two points."""
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5

locations = [(0,0), (1,1), (2,2), (3,3), (4,4)]
start = (0,0)
expected_path = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]

# Test the search function
result = a_star_tsp(locations, start)
print(result, cost(result))
assert result == expected_path, f"Expected {expected_path}, but got {result}"

# Test the distance function
result = distance((0,0), (3,3))
assert result == 4.242640687119285, f"Expected 4.242640687119285, but got {result}"

# Test the heuristic function
result = heuristic(locations, start, start)
assert result == 11.65685424949238, f"Expected 11.65685424949238, but got {result})"
