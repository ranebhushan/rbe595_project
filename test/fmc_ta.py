import copy

robot_radius = 15
robot_ids = [1, 2, 3]
robots_skills = [(1,2), (3,4), (4, 3, 1)]
robot_locations = [100, 50, 69]
# List of robot location and skills
agent_robots = {
    robot_ids[0]: [robots_skills[0], robot_locations[0]]
} 
task_id = ['a', 'b', 'c']
skills = [(1,2), (3,4), (4, 3, 1)]
# Task location
task_locations = [11, 43, 98]

tasks = {task_id[0]:[skills[0], task_locations[0]]}
# Pending Tasks
pending_task = copy.deepcopy(task_id)

# All tasks consume same time and are equally important
"""Perform Task Allocation"""
# For each robot 

    # Pick a task to perform based on tasks on robots radius # Algo
    
    # Pick a matching task based on matching skills and distance to the task (objective function) ---- MAIN TASK *FMC_TA 
    # If tie pick randomly
    # Update pending task


# Allocate Task to the agent




# Finally compute the total cost required and minimize

# back to top

