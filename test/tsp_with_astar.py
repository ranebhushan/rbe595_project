from queue import PriorityQueue

def search(locations, start):
    pq = PriorityQueue()
    pq.put((0, [start]))
    visited = set()
    while not pq.empty():
        # path : is list of all visited nodes beginning with the start node
        _, path = pq.get()
        current = path[-1] # get the last node in path which will be our current node
        
        if len(path) == len(locations):
            # If all nodes are visited TSP is solved
            return path
        if current in visited:
            # Skip if current is already visited
            continue

        visited.add(current)
        
        for neighbor in locations:
            # pick up the next location from the given list of locations
            if neighbor == current:
                continue
            
            if neighbor in visited:
                continue
            
            new_path = path + [neighbor]
            
            priority = cost(new_path) + heuristic(locations, neighbor)
            
            pq.put((priority, new_path))
    return None


def cost(path):
    # Calculate the total current cost form the start till current node
    total = 0
    for i in range(len(path) - 1):
        total += distance(path[i], path[i+1])
    return total


def heuristic(locations, current):
    # Calculates the heuristic based on the unvisited nodes
    # My heuristic is calculated by checking the minimium distance from current node to the unvisited locations
    unvisited = [location for location in locations if location != current]
    if unvisited:
        closest = min(unvisited, key=lambda x: distance(x, current))
        return distance(current, closest) + cost([closest] + unvisited)
    else:
        return 0


def distance(a, b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2)**0.5

locations = [(0,0), (1,1), (2,2), (3,3), (4,4)]
start = (0,0)
expected_path = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]

# Test the search function
result = search(locations, start)
print(result)
# assert result == expected_path, f"Expected {expected_path}, but got {result}"

# # Test the cost function
# result = cost(expected_path)
# assert result == 6.0, f"Expected 6.0, but got {result}"

# # Test the distance function
# result = distance((0,0), (3,3))
# assert result == 4.242640687119285, f"Expected 4.242640687119285, but got {result}"

# # Test the heuristic function
# result = heuristic(locations, start)
# assert result == 11.65685424949238, f"Expected 11.65685424949238, but got {result}"

