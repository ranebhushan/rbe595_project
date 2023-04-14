import copy

robot_radius = 15
robot_ids = [1, 2, 3]
robots_skills = [(1,2), (3,4), (4, 3, 1)]
robot_locations = [100, 50, 69]
# List of robot location and skills
agent_robots = {
    robot_ids[0]: [robots_skills[0], robot_locations[0]],
    robot_ids[1]: [robots_skills[1], robot_locations[1]],
    robot_ids[2]: [robots_skills[2], robot_locations[2]]
} 
task_id = ['a', 'b', 'c']
skills = [(1,2), (3,4), (4, 3, 1)]
# Task location
task_locations = [11, 43, 98]

tasks = {
    task_id[0]:[skills[0], task_locations[0]],
        task_id[1]:[skills[1], task_locations[1]],
        task_id[2]:[skills[2], task_locations[2]]
}
# Pending Tasks
pending_task = copy.deepcopy(task_id)

# All tasks consume same time and are equally important
"""Perform Task Allocation"""
# For each robot 
for r in robot_ids:
    # Pick a task to perform based on tasks on robots radius # Algorithm to pick a task based on radius
    # Check if task lies in robot radius
    # If yes, pick the task
    # If no, pick the task with minimum distance to the robot
    # If tie, pick randomly
    # Update pending task           
    for t in tasks:
        if tasks[t][1] <= robot_locations[r] + robot_radius:
            print("Task {} is in robot {} radius".format(t, r))
            # Check if robot has the skills to perform the task
            # If yes, pick the task
            # If no
            if tasks[t][0] in robots_skills[r]:
                print("Robot {} has the skills to perform task {}".format(r, t))
            # Update pending task
            pending_task.remove(t)
        else:
            print("Task {} is not in robot {} radius".format(t, r))
            # Update pending task
            pending_task.remove(t)
    


    # Pick a matching task based on matching skills and distance to the task (objective function) ---- MAIN TASK *FMC_TA 
    # If tie pick randomly
    # Update pending task


# Allocate Task to the agent




# Finally compute the total cost required and minimize

# back to top

