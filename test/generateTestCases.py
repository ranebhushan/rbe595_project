import random
import numpy as np
import datetime
import os, sys
import copy

class CaseGenerator:
    def __init__(self, num_robots, num_skills, num_tasks, x_boundary=10, y_boundary=10, max_skills_per_task=2):
        self.num_robots = num_robots
        self.num_skills = num_skills
        self.num_tasks = num_tasks
        self.max_skills_per_task = max_skills_per_task
        self.x_boundary = x_boundary
        self.y_boundary = y_boundary
        self.robot_skill_matrix= self.generate_robot_skill_matrix()

        # if max_multiple_skills:
            # self.robot_skill_matrix= self.generate_multiskill_Q_matrix(max_multiple_skills)
        self.task_skill_matrix= self.generate_R_matrix()
        self.distance_matrix = np.zeros((self.num_robots, self.num_tasks, self.num_tasks), dtype=int)
        self.total_time_matrix= np.zeros((self.num_robots, self.num_tasks, self.num_tasks), dtype=int)
        self.task_completion_time = np.zeros((self.num_robots, self.num_tasks), dtype=int)
        self.task_locations = self.generate_task_locations()
        self.total_time_matrix= self.generate_T_matrix()
     
    def generate_Q_matrix(self):
        """
        Generates a unique mapping of skills possesed by each robot
        """
        Q = np.zeros((self.num_robots, self.num_skills), dtype=int)
        skills = list(range(self.num_skills))
        random.shuffle(skills)
        for i in range(self.num_robots):
            Q[i][skills[i]] = 1
        return Q
    
    def generate_multiskill_Q_matrix(self, n):
        Q = np.zeros((self.num_robots, self.num_skills), dtype=int)
        skills = list(range(self.num_skills))
        for i in range(self.num_robots):
            selected_skills = random.sample(skills, n)
            for j in selected_skills:
                Q[i][j] = 1
        return Q
    
    def generate_robot_skill_matrix(self):        
        mat = np.zeros((self.num_robots, self.num_skills), dtype=int)
        skillset = list(range(self.num_skills))
        available_skills = []
        for i in range(self.num_robots):
            if (len(available_skills) == 0):
                available_skills = copy.deepcopy(skillset)
                random.shuffle(available_skills)
            selected_skill = np.random.choice(available_skills)
            mat[i][selected_skill] = 1
            available_skills.remove(selected_skill)
        return mat

    def generate_R_matrix(self):

        R = np.zeros((self.num_tasks, self.num_skills), dtype=int)
        for i in range(self.num_tasks):
            required_skills = random.sample(range(self.num_skills), random.randint(1, self.max_skills_per_task))
            for j in required_skills:
                R[i][j] = 1
        return R
    
    def generate_task_locations(self):
        return np.random.randint(0, self.x_boundary, size=(self.num_tasks, 2))
    
    def generate_T_matrix(self):
        
        for i in range(self.num_robots):
            for j in range(self.num_tasks):
                for k in range(self.num_tasks):
                    # Calculate distance between task j and k
                    self.distance_matrix[i,j,k] = int(np.sqrt((self.task_locations[j][0]-self.task_locations[k][0])**2 
                                        + (self.task_locations[j][1]-self.task_locations[k][1])**2))
                    # task completeion time for robot i to complete task j
                    self.task_completion_time[i][j] = np.random.randint(1, 11) * self.task_skill_matrix[j][i]
                    # Set time taken to go from task j to k for robot i as distance plus time taken to complete task j
                    self.total_time_matrix[i][j][k] = self.distance_matrix[i,j,k] + self.task_completion_time[i][j]
        return self.total_time_matrix
    
if __name__ == "__main__":
    num_robots = 10
    num_skills = 7
    num_tasks = 5
    x_boundary = 10
    y_boundary = 10

    case = CaseGenerator(num_robots, num_skills, num_tasks, x_boundary, y_boundary)
    print(f'Robot Skills Matrix: \n{case.robot_skill_matrix}')
    print(f'Task Skills Matrix: \n{case.task_skill_matrix}')

    # np.savetxt(f"../input_data/robot_skill_mat.csv", case.robot_skill_mat, delimiter=",")
    # np.savetxt(f"../input_data/task_skill_mat.csv", case.task_skill_mat, delimiter=",")
    # np.savetxt(f"../input_data/distance_mat.csv", case.total_time_mat[0], delimiter=",")
    # np.savetxt(f"../input_data/task_completion_time.csv", case.total_time_mat[0], delimiter=",")
    # np.savetxt(f"../input_data/total_time_mat.csv", case.total_time_mat[0], delimiter=",")
    # np.savetxt(f"../input_data/task_locations.csv", case.task_locations, delimiter=",")

    # current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    # np.savetxt(f"../input_data/robot_skill_mat-{current_time}.csv", case.robot_skill_mat, delimiter=",")
    # np.savetxt(f"../input_data/task_skill_mat-{current_time}.csv", case.task_skill_mat, delimiter=",")
    # np.savetxt(f"../input_data/distance_mat-{current_time}.csv", case.total_time_mat[0], delimiter=",")
    # np.savetxt(f"../input_data/task_completion_time-{current_time}.csv", case.total_time_mat[0], delimiter=",")
    # np.savetxt(f"../input_data/total_time_mat-{current_time}.csv", case.total_time_mat[0], delimiter=",")
    # np.savetxt(f"../input_data/task_locations-{current_time}.csv", case.task_locations, delimiter=",")

