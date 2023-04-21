import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# need to convert aco_tsp.py code to work for Task Allocation

class AntColonyOptimization:
    def __init__(self, Q, R, no_of_robots, no_of_tasks, no_of_skills, n_ants, n_iterations, alpha, beta, evaporation_rate):
        self.Q = Q
        self.R = R
        self.no_of_robots = no_of_robots
        self.no_of_tasks = no_of_tasks
        self.no_of_skills = no_of_skills
        self.n_ants = n_ants # This can be replaced with number of robots
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.pheromone = np.ones((self.no_of_tasks, self.no_of_tasks))
        self.best_path = None
        self.best_path_length = np.inf
        
    
    def ant_colony_optimizatoin(self, T):
        # The above matrices are given as input to the ACO algorithm along with the other required parameters
        # The task to skill map and robot to skill map will be given in place of points to ACO
        # The time to task matrix will be given in place of distance function to ACO
        # Use the above to modify the ACO implementation accordingly
        # Assume all the robots start from task 0
        # Assume all the robots have the skill to complete task 0
         
        for iteration in range(self.n_iterations):
            paths = {}
            path_lengths = {}
            
            for ant in range(self.n_ants):
                visited = [False]*self.no_of_tasks
                # if the robot does not have the skill to complete the a particular task mark it as visied
                if(self.Q[ant][self.R[ant][0]] == 0):
                    visited[ant] = True
                # Start from task 0
                current_task = 0
                visited[current_task] = True
                path = [current_task]
                path_length = 0

                # Run until all tasks have been visited
                while False in visited:
                    unvisited = [i for i, x in enumerate(visited) if x == False]
                    # print(unvisited)
                    probabilities = np.zeros(len(unvisited))

                    # Choose next task probabilistically based on pheromone deposited
                    for i, unvisited_task in enumerate(unvisited):
                        probabilities[i] = self.pheromone[current_task][unvisited_task]**self.alpha * T[ant][current_task][unvisited_task]**self.beta
                    
                    probabilities = probabilities/sum(probabilities)

                    next_task = np.random.choice(unvisited, p=probabilities)
                    path.append(next_task)

                    # Update path length
                    path_length += T[ant][current_task][next_task]
                    visited[next_task] = True
                    current_task = next_task

                # Update path and path length
                paths[ant].append(path)
                path_lengths[ant].append(path_length)
                
                # Update best path and best path length for each ant
                if path_length[ant] < self.best_path_length[ant]:
                    self.best_path[ant] = path[ant]
                    self.best_path_length[ant] = path_length[ant]
            
            # Phermone evaporation
            self.pheromone *= self.evaporation_rate

            # Update pheromone
            for i in range(self.no_of_tasks):
                for j in range(self.no_of_tasks):
                    for ant in range(self.n_ants):
                        if j in paths[ant]:
                            self.pheromone[i][j] += 1/path_lengths[ant]

no_of_tasks = 5 # number of tasks
no_of_skills = 3 # number of skills
no_of_robots = 3 # number of robots

# In ACO we need to have the distance function replaced by the time required to complete task from j to k for a robot i from matrix T(i,j,k)
# T(i,j,k) = time to complete task k for robot i from task j
# T(i,j,k) = 0 if robot i does not have skill k
# T(i,j,k) = 0 if task j does not require skill k
# T(i,j,k) = 0 if task j is already completed
# T(i,j,k) = 0 if task k is already assigned to robot i and task does not require multiple skills to complete
# T(i,j,k) = 0 if task k is already assigned to another robot and task does not require multiple skills to complete
# If task k is already assigned to robot i and task requires multiple skills to complete, then T(i,j,k) = time to complete task k for robot i from task j

# We define matrix Q(i,j) to map the robot i with the skills j
# Q(i,j) = 1 if robot i has skill j

# We define matrix R(i, j) to map the task i with the required skills j
# R(i, j) = 1 if task i requires skill j

# The above matrices are given as input to the ACO algorithm along with the other required parameters
# The task to skill map and robot to skill map will be given in place of points to ACO
# The time to task matrix will be given in place of distance function to ACO
