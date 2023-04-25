import numpy as np
import matplotlib.pyplot as plt
import os, sys
import datetime
import time
import random
import math
import copy

# Custom Imports
import generateTestCases as gtc

# GLOBAL DEFINES

class Ant:
    def __init__(self, 
                 ant_id : int,
                 robot_skill_matrix : np.ndarray,
                 task_skill_matrix : np.ndarray):
        self.ant_id = ant_id
        self.reset(robot_skill_matrix, task_skill_matrix)

    def reset(self, 
              robot_skill_matrix : np.ndarray,
              task_skill_matrix : np.ndarray):
        self.current_task = 0
        self.visited_tasks = []
        self.path_length = 0.0
        self.path = []
        self.best_path = []
        self.best_path_length = np.inf

        # Mark task as visited if robot does not have that required skill
        # self.visited_tasks = not np.dot(robot_skill_matrix[self.ant_id],task_skill_matrix).tolist()

        self.skills = np.where(robot_skill_matrix[self.ant_id] == 1)[0]
        print(f'Robot {self.ant_id} has skills {self.skills}')

        self.visited_tasks = np.where(task_skill_matrix[:, self.skills] == 1)[0]
        print(f'Robot {self.ant_id} can do tasks {self.visited_tasks}')

        # self.visited_tasks = np.where(task_skill_matrix[:, skill for skill in self.skills] == 1)[0]

    def update_best_path(self):
        if self.path_length < self.best_path_length:
            self.best_path_length = self.path_length
            self.best_path = self.path

class TaskSharing:
    def __init__(self, 
                 num_robots : int,
                 num_skills : int,
                 num_tasks : int,
                 robot_skill_matrix : np.ndarray,
                 task_skill_matrix : np.ndarray,
                 distance_matrix : np.ndarray,
                 task_completion_time : np.ndarray,
                 total_time_matrix : np.ndarray,
                 alpha : float = 0.5,
                 beta : float = 0.5,
                 gamma : float = 0.5,
                 evaporation_rate : float = 0.1) -> None:
        
        self.num_robots = num_robots
        self.num_skills = num_skills
        self.num_tasks = num_tasks
        self.robot_skill_matrix = robot_skill_matrix
        self.task_skill_matrix = task_skill_matrix
        self.distance_matrix = distance_matrix
        self.task_completion_time = task_completion_time
        self.total_time_matrix = total_time_matrix
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.evaporation_rate = evaporation_rate
        
        # Empty Variables
        self.best_path = []

        # Initialize Ants equal to number of robots
        self.ants = [Ant(i, self.robot_skill_matrix, self.task_skill_matrix) for i in range(self.num_robots)]

        # Pheromone Matrix
        self.pheromone_matrix = np.ones((self.num_robots, self.num_tasks, self.num_tasks), dtype=float)
        
    def update_pheromone(self):
        self.pheromone_matrix = (1 - self.evaporation_rate) * self.pheromone_matrix

        for ant in self.ants:
            if (ant.best_path_length == 0 or ant.best_path_length == np.inf):
                continue
            for i in range(len(ant.best_path) - 1):
                self.pheromone_matrix[ant.ant_id][ant.best_path[i]][ant.best_path[i+1]] += 1.0 / ant.best_path_length
            self.pheromone_matrix[ant.ant_id][ant.best_path[-1]][ant.best_path[0]] += 1.0 / ant.best_path_length
       
    def launch_ant(self, ant):
        ant.reset()
        
        ant.current_task = 0
        ant.visited_tasks[ant.current_task] = 1
        ant.path.append(ant.current_task)
        ant.path_length = 0.0

        while False in ant.visited_tasks:
            unvisited_tasks = np.where(not ant.visited_tasks)[0]
            likelihood = np.zeros(len(unvisited_tasks))

            for i in range(len(unvisited_tasks)):

                if(self.time_matrix[ant.ant_id][ant.current_task][unvisited_tasks[i]] == np.inf):
                    likelihood[i] = 0
                    ant.visited_tasks[unvisited_tasks[i]] = 1

                else:

                    likelihood[i] = self.pheromone_matrix[ant.ant_id][ant.current_task][unvisited_tasks[i]]**self.alpha / self.time_matrix[ant.ant_id][ant.current_task][unvisited_tasks[i]]**self.beta

            if np.sum(likelihood) > 0:
                probability = likelihood / np.sum(likelihood)

            if np.sum(probability) == 0 and False in ant.visited_tasks:
                # TODO : If any miscellaneous path is found, check previous code 
                continue

            # Select next task
            next_task = np.random.choice(a = unvisited_tasks, 
                                            size = 1, 
                                            p = probability)
            
            ant.path_length += self.time_matrix[ant.ant_id][ant.current_task][next_task]
            ant.path.append(next_task)
            ant.current_task = next_task
            ant.visited_tasks[next_task] = 1
        ant.update_best_path()            

    def gobabygo(self, num_iterations : int):
        self.num_iterations = num_iterations
        for i in range(self.num_iterations):
            for ant in self.ants:
                self.launch_ant(ant)
            self.update_pheromone()
            self.best_paths = self.update_best_path()
        return self.best_paths
    
if __name__ == "__main__":
    gen = gtc.CaseGenerator(num_robots=3,
                            num_skills=3,
                            num_tasks=5)
    
    print(f'Robot Skill Matrix:\n{gen.robot_skill_matrix}')
    print(f'Task Skill Matrix:\n{gen.task_skill_matrix}')

    aunty = Ant(ant_id=0, 
                robot_skill_matrix = gen.robot_skill_matrix, 
                task_skill_matrix = gen.task_skill_matrix)
    
    # system = TaskSharing(num_robots=gen.num_robots,
    #                     num_skills=gen.num_skills,
    #                     num_tasks=gen.num_tasks,
    #                     robot_skill_matrix=gen.robot_skill_matrix,
    #                     task_skill_matrix=gen.task_skill_matrix,
    #                     distance_matrix=gen.distance_matrix,
    #                     task_completion_time=gen.task_completion_time,
    #                     total_time_matrix=gen.total_time_matrix)
    
    # system.gobabygo(num_iterations=10)
    # print("Best Paths ", system.best_paths)
