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
                 task_skill_matrix : np.ndarray,
                 total_time_matrix : np.ndarray):
        self.ant_id = ant_id
        self.others_paths = {}
        self.best_path = []
        self.best_path_length = np.inf
        self.others_task = []
        self.total_time_matrix = total_time_matrix
        self.robot_skill_matrix = robot_skill_matrix
        self.task_skill_matrix = task_skill_matrix
        
        self.reset(robot_skill_matrix, task_skill_matrix)

    def reschedule(self):
        """ This function uses the robots best path and others best path and reschedules the tasks"""
        
        if self.others_paths:
            
            # For every task that other robots visit which are same as your previous task, 
            # for the next loop you do not visit the tasks which you visit very late in the previous iteration 
            # and let the other robot with same skill visit it
            for robot, path in self.others_paths.items():
                overlapping_tasks = list(set(path) & set(self.best_path)) 
                if overlapping_tasks:
                    # Check if the overlapping task in our path has a higher index than the other robot, if yes then remove it from our path
                    # if no keep that task
                    # if same then go to conflict resolution
                    resolve = False
                    for task in overlapping_tasks:
                        skills_required_by_task = np.where(self.task_skill_matrix[task] == 1)[0]
                        print('skills_required_by_task = ', skills_required_by_task)
                        for skill in skills_required_by_task:
                            print('skill = ', skill)
                            if(self.robot_skill_matrix[self.ant_id][skill] == self.robot_skill_matrix[robot][skill]):
                                resolve = True
                                break

                        if task == 0 or resolve == False:
                            continue
                        
                        if self.best_path.index(task) > path.index(task):
                            self.others_task.append(task)
                        elif self.best_path.index(task) < path.index(task):
                            pass
                        else:
                            if self.conflict_resolution(robot, task):
                                pass
                            else:
                                self.others_task.append(task)
            print(f'{self.ant_id}self.others_task = {self.others_task}')

    def conflict_resolution(self, robot, task):
        """This code resolves the conflict between two robots who have the same task at the same time
            Returns True if this robot keeps the task
        """
        # from task and robots path get the previous task and 
        # get the time from total time matrix for previous task to task, 
        # for both robots and compare the time, the robot having shorter time will get the task
        other_path = self.others_paths[robot]
        other_time = self.total_time_matrix[robot][other_path[other_path.index(task) - 1]][task]
        
        my_time = self.total_time_matrix[self.ant_id][self.best_path[self.best_path.index(task) - 1]][task]
        
        if my_time < other_time:
            return True 
        else:
            return False


    def reset(self, 
              robot_skill_matrix : np.ndarray,
              task_skill_matrix : np.ndarray):
        self.current_task = 0
        self.visited_tasks = []
        self.path_length = 0.0
        self.path = []
        
        
        # Mark task as visited if robot does not have that required skill
        # self.visited_tasks = not np.dot(robot_skill_matrix[self.ant_id],task_skill_matrix).tolist()

        self.skills = np.where(robot_skill_matrix[self.ant_id] == 1)[0]
        print(f'Robot {self.ant_id} has skills {self.skills}')
        
        self.to_do_tasks = list(set(np.where(task_skill_matrix[:, self.skills] == 1)[0]))
        print(f'Robot {self.ant_id} can do tasks {self.to_do_tasks}')

        self.visited_tasks = [False] * task_skill_matrix.shape[0]
        
        # For every task that is not in the list of tasks that the robot can do, mark it as visited
        for task in range(task_skill_matrix.shape[0]):
            if task not in self.to_do_tasks or task in self.others_task:
                # print(f'Robot {self.ant_id} cannot do task {self.others_task}')
                self.visited_tasks[task] = True
        # self.others_task = []
        print(f'Ant {self.ant_id} Visited tasks = {self.visited_tasks}')
        # self.visited_tasks = np.where(task_skill_matrix[:, skill for skill in self.skills] == 1)[0]

    def update_best_path(self):
        if self.path_length < self.best_path_length:
            self.best_path_length = self.path_length
            self.best_path = self.path
        print(f'{self.ant_id} best path = {self.best_path}')

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
        self.ants = [Ant(i, self.robot_skill_matrix, self.task_skill_matrix, self.total_time_matrix) for i in range(self.num_robots)]

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
        
        ant.reset(self.robot_skill_matrix, self.task_skill_matrix)
        
        ant.current_task = 0
        ant.visited_tasks[ant.current_task] = True
        ant.path.append(ant.current_task)
        ant.path_length = 0.0
       
        
        while False in ant.visited_tasks:
            unvisited_tasks = np.where(np.logical_not(ant.visited_tasks))[0]
            likelihood = np.zeros(len(unvisited_tasks))

            for i in range(len(unvisited_tasks)):

                if(self.total_time_matrix[ant.ant_id][ant.current_task][unvisited_tasks[i]] == np.inf):
                    likelihood[i] = 0
                    ant.visited_tasks[unvisited_tasks[i]] = True

                else:

                    likelihood[i] = self.pheromone_matrix[ant.ant_id][ant.current_task][unvisited_tasks[i]]**self.alpha / self.total_time_matrix[ant.ant_id][ant.current_task][unvisited_tasks[i]]**self.beta

            if np.sum(likelihood) > 0:
                probability = likelihood / np.sum(likelihood)

            if np.sum(likelihood) == 0 and False in ant.visited_tasks:
                probability = 0
                # TODO : If any miscellaneous path is found, check previous code 
                continue

            # Select next task
            next_task = np.random.choice(a = unvisited_tasks, p = probability)
            
            ant.path_length += self.total_time_matrix[ant.ant_id][ant.current_task][next_task]
            ant.path.append(next_task)
            ant.current_task = next_task
            ant.visited_tasks[next_task] = True
        ant.update_best_path()            


    
    def sharing_is_caring(self):
        """ This function takes care of robots sharing their best paths with each other"""
        for ant in self.ants:
            ant.others_task = []
            for other_ant in self.ants:
                if ant.ant_id == other_ant.ant_id:
                    continue
                else:
                    ant.others_paths[other_ant.ant_id] = other_ant.best_path   

    def gobabygo(self, num_iterations : int):
        self.num_iterations = num_iterations
        for i in range(self.num_iterations):
            for ant in self.ants:
                ant.reschedule()
                self.launch_ant(ant)
            self.sharing_is_caring()
            self.update_pheromone()
        
        self.best_paths = [ant.best_path for ant in self.ants]
            # self.best_paths = self.update_best_path()
        return self.best_paths
    
if __name__ == "__main__":
    gen = gtc.CaseGenerator(num_robots=3,
                            num_skills=3,
                            num_tasks=10)
    
    print(f'Robot Skill Matrix:\n{gen.robot_skill_matrix}')
    print(f'Task Skill Matrix:\n{gen.task_skill_matrix}')

    # aunty = Ant(ant_id=0, 
    #             robot_skill_matrix = gen.robot_skill_matrix, 
    #             task_skill_matrix = gen.task_skill_matrix)
    
    system = TaskSharing(num_robots=gen.num_robots,
                        num_skills=gen.num_skills,
                        num_tasks=gen.num_tasks,
                        robot_skill_matrix=gen.robot_skill_matrix,
                        task_skill_matrix=gen.task_skill_matrix,
                        distance_matrix=gen.distance_matrix,
                        task_completion_time=gen.task_completion_time,
                        total_time_matrix=gen.total_time_matrix)
    
    system.gobabygo(num_iterations=10)
    print("Best Paths ", system.best_paths)
