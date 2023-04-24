import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import sys
# need to convert aco_tsp.py code to work for Task Allocation

class AntColonyOptimization:
    def __init__(self, Q, R, no_of_robots, no_of_tasks, no_of_skills, n_ants, n_iterations, alpha, beta, evaporation_rate):
        self.Q = Q
        self.R = R
        self.no_of_robots = no_of_robots
        self.no_of_tasks = no_of_tasks
        self.no_of_skills = no_of_skills
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.pheromone = np.ones((self.no_of_tasks, self.no_of_tasks))
        self.best_path = {i: 0 for i in range(self.no_of_robots)}
        self.best_path_length = {i: np.inf for i in range(self.no_of_robots)}
        
    
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
            
            for robot in range(self.no_of_robots):
                # print('Ant {}'.format(ant))
                visited = [False]*self.no_of_tasks
                # if the robot does not have the skill to complete the a particular task mark it as visied
                # if(self.Q[ant][self.R[ant][0]] == 0):
                #     visited[ant] = True
                # Start from task 0
                current_task = 0
                visited[current_task] = True
                path = [current_task]
                path_length = 0
                
                # Run until all tasks have been visited
                while False in visited:
                    unvisited = np.where(np.logical_not(visited))[0]#[i for i, x in enumerate(visited) if x == False]
                    # print(len(unvisited))
                    probabilities = np.zeros(len(unvisited))
                    
                    # Choose next task probabilistically based on pheromone deposited
                    for i, unvisited_task in enumerate(unvisited):
                        # print("Ant", ant, 'Task :', unvisited_task)
                        # print("PMat")
                        # print(self.pheromone)
                        # print(f'T[{ant}]')
                        # print(T[ant])
                        # print('Phermone {}, Time {}'.format(self.pheromone[current_task][unvisited_task], T[ant][current_task][unvisited_task]))
                        if T[robot][current_task][unvisited_task] == np.inf:
                            probabilities[i] = 0
                            visited[unvisited_task] = True
                        else:   
                            probabilities[i] = self.pheromone[current_task][unvisited_task]**self.alpha / T[robot][current_task][unvisited_task]**self.beta
                        
                        # print("probabilites", i, "=",probabilities[i])
                        # print("-"*50)

                    if sum(probabilities):
                        probabilities = probabilities/sum(probabilities)

                    # print("norm probabilites", i, "=",probabilities)
                    # if all the probabilities are zero then it means that the robot does not have the skill to complete any of the remaining tasks
                    # so the robot will do no task, if we have a task m+1 later we can assign it to the robot
                    # if not np.sum(probabilities) and all nodes are visited then break:
                    # print(visited)
                    if sum(probabilities) == 0 and False not in visited:
                        print("No task can be assigned to robot", robot)
                        if paths.get(robot) is None:
                            paths[robot] = []
                            path_lengths[robot] = []
                        
                        paths[robot].append(path)
                        path_lengths[robot].append(path_length)                       
                        continue
                    next_task = np.random.choice(unvisited, p=probabilities)
                    # print("next task", next_task)
                    path.append(next_task)
                    # print("path", path)

                    # Update path length
                    path_length += T[robot][current_task][next_task]
                    
                    current_task = next_task
                    visited[current_task] = True
                    # print("ant", ant, "current task", current_task)

                    # print("*"*50)

                # Update path and path length
                if paths.get(robot) is None:
                    paths[robot] = []
                    path_lengths[robot] = []
                paths[robot].append(path)
                path_lengths[robot].append(path_length)
                # print('paths', paths)
                # print('path lengths', path_lengths)
                # print('path_lengths[ant]', path_lengths[ant])
                # print('self.best_path_length[ant]', self.best_path_length[ant])

                # Update best path and best path length for each ant

                if path_length < self.best_path_length[robot]:
                    self.best_path[robot] = paths[robot]
                    self.best_path_length[robot] = path_length
                #     print("best path", self.best_path, "best path length", self.best_path_length)
                # print("="*50)

            # Phermone evaporation
            self.pheromone *= self.evaporation_rate

            # Update pheromone
            for robot in range(no_of_robots):
                path_temp = self.best_path[robot][0]
                path_length_temp = self.best_path_length[robot]
                if path_length_temp == np.inf or path_length_temp == 0:
                    continue
                # print('path_temp', path_temp, 'path_length_temp', path_length_temp)
                for i in range(len(path_temp)-1):
                    self.pheromone[path_temp[i]][path_temp[i+1]] += 1/path_length_temp
                self.pheromone[path_temp[-1]][path_temp[0]] += 1/path_length_temp
                # print("pheromone", self.pheromone)

        return self.best_path, self.best_path_length
    
    


no_of_tasks = 3 # number of tasks
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
T = [[[0, np.inf, 4], 
      [np.inf, 0, 2], 
      [np.inf, np.inf, 0]],
      [[0, 5, np.inf], 
       [np.inf, 0, np.inf], 
       [np.inf, 3, 0]], 
      [[0, np.inf, np.inf], 
       [1, 0, np.inf], 
       [2, np.inf, 0]]]
# We define matrix Q(i,j) to map the robot i with the skills j
# Q(i,j) = 1 if robot i has skill j
Q = [[0, 1, 0], 
     [0, 0, 1], 
     [0, 1, 0]]
# We define matrix R(i, j) to map the task i with the required skills j
# R(i, j) = 1 if task i requires skill j
R = [[0, 0, 0], 
     [0, 0, 1], 
     [1, 0, 0]] 
# The above matrices are given as input to the ACO algorithm along with the other required parameters
# The task to skill map and robot to skill map will be given in place of points to ACO
# The time to task matrix will be given in place of distance function to ACO
aco = AntColonyOptimization(Q, R, no_of_robots, no_of_tasks, no_of_skills, n_ants=3, n_iterations=2, alpha=1, beta=1, evaporation_rate=0.5)
best_path, best_path_length = aco.ant_colony_optimizatoin(T)
print('best_paths for each robot',best_path)
print('best path lengths respectively', best_path_length)
