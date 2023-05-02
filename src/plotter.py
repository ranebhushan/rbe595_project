import matplotlib.pyplot as plt
import numpy as np
import matplotlib.markers as mmarkers

# Assuming that we have the following variables:
# best_paths: list of best paths for each robot
# Q: robot-skill matrix

# Q = robo vs skill
# R = task vs skill

def plot_task_allocation(best_paths, task_locations, robot_skill_matrix, task_skill_matrix):
    unique_markers = list(mmarkers.MarkerStyle.markers.keys())
    colors = plt.cm.rainbow(np.linspace(0, 1, len(best_paths)))

    for i, task_location in enumerate(task_locations):
        task_skills = np.where(task_skill_matrix[i] == 1)[0]
        for task_skill in task_skills:
            plt.scatter(task_location[0], task_location[1], c='black', s=100, marker=unique_markers[task_skill])

    for i, path in enumerate(best_paths):
        color = colors[i]
        x, y = zip(*path)
        plt.plot(x, y, c=color, linewidth=2, label=f"Robot {i}")
    
    legend_handles = [plt.Line2D([0], [0], linestyle='none', marker=m, color='black') for m in unique_markers]
    legend_handles.append(plt.Line2D([0], [0], linestyle='-', color='black'))
    plt.legend(handles=legend_handles, labels=[f"Skill {i}" for i in range(len(unique_markers))] + ["Robot Path"], loc='upper left')
    # Set axis limits and title
    plt.xlim([min(x for x, y in task_locations)-1, max(x for x, y in task_locations)+1])
    plt.ylim([min(y for x, y in task_locations)-1, max(y for x, y in task_locations)+1])
    plt.title("Task Allocation with Robot Paths")
    plt.show()



# # Define a list of unique markers for each skill
# # unique_markers = ['o', 's', 'v', '^', '>', '<']
# unique_markers = list(mmarkers.MarkerStyle.markers.keys())
# # Define a color map for each robot
# colors = plt.cm.rainbow(np.linspace(0, 1, len(best_paths)))

# # Plot the task locations with markers based on skills
# for i, (x, y) in enumerate(task_locations):
#     skill = task_skills[i]
#     marker = unique_markers[skill]
#     plt.scatter(x, y, c='black', s=100, marker=marker)

# # Plot the paths for each robot
# for i, path in enumerate(best_paths):
#     color = colors[i]
#     x, y = zip(*path)
#     plt.plot(x, y, c=color, linewidth=2, label=f"Robot {i}")

# # Add legend for the markers
# legend_handles = [plt.Line2D([0], [0], linestyle='none', marker=m, color='black') for m in unique_markers]
# legend_labels = [f"Skill {i+1}" for i in range(len(unique_markers))]
# plt.legend(handles=legend_handles, labels=legend_labels)

# # Set axis limits and title
# plt.xlim([min(x for x, y in task_locations)-1, max(x for x, y in task_locations)+1])
# plt.ylim([min(y for x, y in task_locations)-1, max(y for x, y in task_locations)+1])
# plt.title("Task Allocation with Robot Paths")

# # Show the plot
# plt.show()
