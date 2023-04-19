import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform


# Define the objective function to minimize (total distance traveled)
def objective_function(solution, distances):
    return distances[solution[-1], solution[0]] + np.sum(distances[solution[i], solution[i+1]] for i in range(len(solution)-1))


# Define the ant colony optimization function
def ant_colony_optimization(distances, n_ants, n_iterations, evaporation_rate, alpha, beta):
    # Initialize the pheromone matrix
    pheromone = np.ones(distances.shape) / len(distances)
    
    # Initialize the best solution found so far
    best_solution = None
    best_cost = np.inf
    
    # Iterate over a fixed number of iterations
    for i in range(n_iterations):
        # Initialize the ant solutions and their corresponding costs
        ant_solutions = []
        ant_costs = np.zeros(n_ants)
        
        # Iterate over each ant
        for k in range(n_ants):
            # Initialize the ant's solution as visiting the cities in a random order
            solution = np.arange(distances.shape[0])
            np.random.shuffle(solution)
            
            # Iterate over the remaining cities and choose the next city to visit based on the pheromone trail and heuristic information
            for j in range(1, distances.shape[0]):
                unvisited_cities = np.setdiff1d(np.arange(distances.shape[0]), solution[:j])
                pheromone_values = pheromone[solution[j-1], unvisited_cities]
                heuristic_values = 1.0 / distances[solution[j-1], unvisited_cities]
                probabilities = (pheromone_values ** alpha) * (heuristic_values ** beta)
                probabilities = probabilities / np.sum(probabilities)
                next_city = np.random.choice(unvisited_cities, p=probabilities)
                solution[j] = next_city
            
            # Calculate the cost of the ant's solution
            cost = objective_function(solution, distances)
            
            # Update the best solution found so far
            if cost < best_cost:
                best_solution = solution
                best_cost = cost
            
            # Add the ant's solution and cost to the list of ant solutions and costs
            ant_solutions.append(solution)
            ant_costs[k] = cost
        
        # Update the pheromone trail based on the ant solutions
        pheromone *= evaporation_rate
        for k in range(n_ants):
            for j in range(1, distances.shape[0]):
                pheromone[ant_solutions[k][j-1], ant_solutions[k][j]] += 1.0 / ant_costs[k]
        
    return best_solution, best_cost


# Generate a random TSP instance with 10 cities
np.random.seed(1)
n_cities = 10
cities = np.random.rand(n_cities, 2)
distances = squareform(pdist(cities))

# Set the parameters for ant colony optimization
n_ants = 10
n_iterations = 100
evaporation_rate = 0.5
alpha = 1.0
beta = 3.0

# Solve the TSP using ant colony optimization
best_solution, best_cost = ant_colony_optimization(distances, n_ants, n_iterations, evaporation_rate, alpha, beta)

# Plot the results
plt.figure(figsize=(6, 6))
plt.scatter(cities[:, 0], cities[:, 1], color='b')
plt.plot(cities[best_solution, 0], cities[best_solution, 1], color='r', lw=2, zorder=2)
plt.title(f'Total distance traveled: {best_cost:.3f}')
plt.show()
