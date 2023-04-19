import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform


# Define the objective function to minimize (total distance traveled)
def objective_function(solution, distances):
    return np.sum(distances[solution[i], solution[i+1]] for i in range(len(solution)-1))


# Define the acceptance probability function
def acceptance_probability(cost, new_cost, temperature):
    if new_cost < cost:
        return 1.0
    else:
        return np.exp(-(new_cost - cost) / temperature)


# Define the simulated annealing function
def simulated_annealing(distances, initial_solution, initial_temperature, cooling_rate, stopping_temperature):
    current_solution = initial_solution
    current_cost = objective_function(current_solution, distances)
    best_solution = current_solution
    best_cost = current_cost
    temperature = initial_temperature
    
    while temperature > stopping_temperature:
        # Generate a new candidate solution by randomly swapping two cities
        new_solution = np.copy(current_solution)
        i, j = np.random.randint(len(new_solution), size=2)
        new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
        
        # Calculate the cost of the new solution and accept or reject it based on the acceptance probability
        new_cost = objective_function(new_solution, distances)
        if acceptance_probability(current_cost, new_cost, temperature) > np.random.random():
            current_solution = new_solution
            current_cost = new_cost
        
        # Update the best solution found so far
        if current_cost < best_cost:
            best_solution = current_solution
            best_cost = current_cost
        
        # Cool down the temperature
        temperature *= cooling_rate
        
    return best_solution, best_cost


# Generate a random TSP instance with 10 cities
np.random.seed(1)
n_cities = 10
cities = np.random.rand(n_cities, 2)
distances = squareform(pdist(cities))

# Define the initial solution (visit the cities in order)
initial_solution = np.arange(n_cities)

# Set the initial temperature, cooling rate, and stopping temperature
initial_temperature = 100.0
cooling_rate = 0.99
stopping_temperature = 1e-8

# Solve the TSP using simulated annealing
best_solution, best_cost = simulated_annealing(distances, initial_solution, initial_temperature, cooling_rate, stopping_temperature)

# Plot the results
plt.figure(figsize=(6, 6))
plt.scatter(cities[:, 0], cities[:, 1], color='b')
plt.plot(cities[best_solution, 0], cities[best_solution, 1], color='r', lw=2, zorder=2)
plt.title(f'Total distance traveled: {best_cost:.3f}')
plt.show()
