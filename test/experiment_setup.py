import numpy as np
import time 
import generateTestCases as gtc
import task_sharing as ts
import pandas as pd

NO_OF_EXPERIMENTS = 50


for i in range(2,8):
    NUM_TASKS = 2**i
    NUM_ROBOTS = NUM_TASKS//2
    NUM_SKILLS = int(NUM_TASKS * .6)
    MAX_SKILLS_PER_TASK = 1

    solving_time_sharing = {}
    solving_time_no_sharing = {}

    best_path_length_sharing = {}
    best_path_length_no_sharing = {}    
    # print(f'Robot Skill Matrix:\n{gen.robot_skill_matrix}')
    # print(f'Task Skill Matrix:\n{gen.task_skill_matrix}')
    for exp in range(NO_OF_EXPERIMENTS):
        gen = gtc.CaseGenerator(num_robots=NUM_ROBOTS,
                                num_skills=NUM_SKILLS,
                                num_tasks=NUM_TASKS,
                                max_skills_per_task=MAX_SKILLS_PER_TASK)
        
        
        for i in range(2):
            task_sharing_flag = False
            if i == 1:
                task_sharing_flag = True

        
            system = ts.TaskSharing(num_robots=gen.num_robots,
                                num_skills=gen.num_skills,
                                num_tasks=gen.num_tasks,
                                robot_skill_matrix=gen.robot_skill_matrix,
                                task_skill_matrix=gen.task_skill_matrix,
                                distance_matrix=gen.distance_matrix,
                                task_completion_time=gen.task_completion_time,
                                total_time_matrix=gen.total_time_matrix,
                                task_locations=gen.task_locations,
                                task_sharing_flag = task_sharing_flag)
            start_time = time.time()
            system.gobabygo(num_iterations=2*gen.num_tasks)
            end_time = time.time()
            time_taken = end_time - start_time
            
            if task_sharing_flag:
                solving_time_sharing[exp] = time_taken 
                best_path_length_sharing[exp] = sum(system.best_path_lengths) 
            else:
                solving_time_no_sharing[exp] = time_taken
                best_path_length_no_sharing[exp] = sum(system.best_path_lengths)


    df_sharing = pd.DataFrame.from_dict([solving_time_sharing, best_path_length_sharing], orient='index', columns=['Time'])
    df_sharing.to_csv(f'../Experiment_data/{NUM_ROBOTS}_{NUM_SKILLS}_{NUM_TASKS}_sharing.csv')

    df_sharing = pd.DataFrame.from_dict(solving_time_no_sharing, best_path_length_no_sharing, orient='index', columns=['Time'])
    df_sharing.to_csv(f'../Experiment_data/{NUM_ROBOTS}_{NUM_SKILLS}_{NUM_TASKS}_NO_sharing.csv')

    print(f'Experiment {exp} done')

