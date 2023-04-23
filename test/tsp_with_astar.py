from queue import PriorityQueue
import matplotlib.pyplot as plt
import os
import sys
import numpy as np

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
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)**0.5

locations = [
[0.29190999 ,0.83956842 ,0.28643755],
[0.35204709 ,0.62705444 ,0.79186177],
[0.75419566 ,0.85640268 ,0.43189559],
[0.06949494 ,0.4099236  ,0.19524355],
[0.26728267 ,0.92283424 ,0.70410629],
[0.57786128 ,0.13531019 ,0.82986917],
[0.64900318 ,0.94492431 ,0.63646809],
[0.84333034 ,0.17215229 ,0.43813501],
[0.222248   ,0.43198208 ,0.14564145],
[0.34599485 ,0.59990873 ,0.27203917]
]

start = locations[0]

# Test the search function
points = a_star_tsp(locations, start)
print("Result :", type(points), points)
print("Points 0 :", points[0][0], points[0][1], points[0][2])
print("Cost :", cost(points))

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
points = np.array(points)
ax.scatter(points[:,0], points[:,1], points[:,2], c='k', marker='o')

for i in range(len(points)-1):
    print("A",i)
    ax.scatter(points[:,0], points[:,1], points[:,2], c='k', marker='o')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    ax.plot([points[i][0], points[i+1][0]],
            [points[i][1], points[i+1][1]],
            [points[i][2], points[i+1][2]],
            c='r', linestyle='-', linewidth=2, marker='o')
    
    plt.savefig(os.path.join('results', f'astar_{i}.png'), dpi = 300, bbox_inches ="tight",)
    plt.pause(0.5)
    print("B",i)

ax.plot([points[0][0], points[-1][0]],
        [points[0][1], points[-1][1]],
        [points[0][2], points[-1][2]],
        c='r', linestyle='-', linewidth=2, marker='o')

plt.savefig(os.path.join('results', f'astar_{i+1}.png'), dpi = 300, bbox_inches ="tight",)

plt.show()