import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import os

def distance(point1, point2):
    return np.sqrt(np.sum((point1 - point2)**2))

def ant_colony_optimization(points, n_ants, n_iterations, alpha, beta, evaporation_rate, Q):
    n_points = len(points)
    pheromone = np.ones((n_points, n_points))
    best_path = None
    best_path_length = np.inf
    
    for iteration in range(n_iterations):
        paths = []
        path_lengths = []
        
        for ant in range(n_ants):
            visited = [False]*n_points
            current_point = np.random.randint(n_points)
            visited[current_point] = True
            path = [current_point]
            path_length = 0
            
            # Run until all points have been visited
            while False in visited:
                unvisited = np.where(np.logical_not(visited))[0]
                probabilities = np.zeros(len(unvisited))
                
                # Heuristic probability calculation
                for i, unvisited_point in enumerate(unvisited):
                    probabilities[i] = pheromone[current_point, unvisited_point]**alpha / distance(points[current_point], points[unvisited_point])**beta
                
                probabilities /= np.sum(probabilities)
                
                next_point = np.random.choice(unvisited, p=probabilities)
                path.append(next_point)
                path_length += distance(points[current_point], points[next_point])
                visited[next_point] = True
                current_point = next_point
            
            paths.append(path)
            path_lengths.append(path_length)
            
            if path_length < best_path_length:
                best_path = path
                best_path_length = path_length
        
        # Phermone evaporation
        pheromone *= evaporation_rate
        
        # Phermone update while back propagation
        for path, path_length in zip(paths, path_lengths):
            for i in range(n_points-1):
                pheromone[path[i], path[i+1]] += Q/path_length
            pheromone[path[-1], path[0]] += Q/path_length

    return best_path, best_path_length
    
def plot_best(points, best_path):
    n_points = len(points)
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(points[:,0], points[:,1], points[:,2], c='r', marker='o')
    
    for i in range(n_points-1):
        ax.plot([points[best_path[i],0], points[best_path[i+1],0]],
                [points[best_path[i],1], points[best_path[i+1],1]],
                [points[best_path[i],2], points[best_path[i+1],2]],
                c='g', linestyle='-', linewidth=2, marker='o')
    # Plot 1st and last point to close the path    
    ax.plot([points[best_path[0],0], points[best_path[-1],0]],
            [points[best_path[0],1], points[best_path[-1],1]],
            [points[best_path[0],2], points[best_path[-1],2]],
            c='g', linestyle='-', linewidth=2, marker='o')
    
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()

# Example usage:
points1 = np.random.rand(10, 3) # Generate 10 random 3D points
points1 = np.array([
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
])
# print("Points 1", points1)
best_path1, best_path_length1 = ant_colony_optimization(points1, n_ants=10, n_iterations=100, alpha=1, beta=1, evaporation_rate=0.5, Q=1)
print("Best path 1", best_path1)
print("Best path length 1", best_path_length1)

# same_points = points1[np.random.choice(points1.shape[0], size = 4, replace=False)]
# # print("same points", same_points)
# points2 = np.random.rand(6, 3) # Generate 10 random 3D points
# points2 = np.concatenate((points2, same_points), axis=0)
# # print("Points 2", points2)
# best_path2 = ant_colony_optimization(points2, n_ants=10, n_iterations=100, alpha=1, beta=1, evaporation_rate=0.5, Q=1)
# print("Best path 2", best_path2)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

print("Points1 length", len(points1))
for i in range(len(points1)-1):
    print("A",i)
    ax.scatter(points1[:,0], points1[:,1], points1[:,2], c='k', marker='o')
    # ax.scatter(points2[:,0], points2[:,1], points2[:,2], c='k', marker='*')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    ax.plot([points1[best_path1[i],0], points1[best_path1[i+1],0]],
            [points1[best_path1[i],1], points1[best_path1[i+1],1]],
            [points1[best_path1[i],2], points1[best_path1[i+1],2]],
            c='r', linestyle='-', linewidth=2, marker='o')
    
    # ax.plot([points2[best_path2[i],0], points2[best_path2[i+1],0]],
    #         [points2[best_path2[i],1], points2[best_path2[i+1],1]],
    #         [points2[best_path2[i],2], points2[best_path2[i+1],2]],
            # c='b', linestyle='-.', linewidth=2, marker='*')  
    plt.savefig(os.path.join('results', f'aco_{i}.png'), dpi = 300, bbox_inches ="tight",)
    plt.pause(0.25)
    print("B",i)
print("C")

# Plot 1st and last point to close the path    
ax.plot([points1[best_path1[0],0], points1[best_path1[-1],0]],
        [points1[best_path1[0],1], points1[best_path1[-1],1]],
        [points1[best_path1[0],2], points1[best_path1[-1],2]],
        c='r', linestyle='-', linewidth=2, marker='o')
print("D")

# ax.plot([points2[best_path2[0],0], points2[best_path2[-1],0]],
#         [points2[best_path2[0],1], points2[best_path2[-1],1]],
#         [points2[best_path2[0],2], points2[best_path2[-1],2]],
#         c='b', linestyle='-.', linewidth=2, marker='*')
# print("E")

plt.savefig(os.path.join('results', f'aco_{i+1}.png'), dpi = 300, bbox_inches ="tight",)
plt.show()
print("F")