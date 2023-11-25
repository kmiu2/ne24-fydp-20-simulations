# Kinetic Monte Carlo simulation of absorption and desorption of Sodium atoms on Al foil
import numpy as np
import matplotlib.pyplot as plt

## Input parameters
alpha = 1  # Strength of near neighbor interaction
ra = 4  # Absorption rate
rd = 2  # Desorption rate
num_runs = 5000  # Number of MC runs
length = 32  # Length of the foil (number of sites)

## Rates Setup
rates = np.zeros(6)  # Rates of absorption and desorption
rates[0] = ra

# Rates of desorption with respect to number of neighbours
# rdi = rd * alpha**i where i is the number of neighbours (0 to 4)

for i in range(1, 6):
    num_neighbours = i - 1
    rates[i] = rd * alpha**num_neighbours

## Simulation Setup
lattice = np.zeros(
    (length + 2, length + 2)
)  # Lattice of atoms (with extra sites for periodic boundary conditions)
prob = np.zeros(6)  # Probability of each rate event
results = np.zeros(num_runs)  # Results of the simulation

## Main Loop
for run in range(num_runs):
    # Matrix to store locations
    sites = [[] for _ in range(6)]
    num_times = np.zeros(6)  # Number of times each rate event occurs

    for i in range(1, length + 1):
        for j in range(1, length + 1):
            if lattice[i, j] == 0:
                num_times[0] += 1
                sites[0].append((i, j))
            elif lattice[i, j] == 1:
                num_neighbours = int(
                    lattice[i - 1, j]
                    + lattice[i + 1, j]
                    + lattice[i, j - 1]
                    + lattice[i, j + 1]
                )
                num_times[num_neighbours] += 1
                sites[num_neighbours].append((i, j))

    # Calculate total rate
    total_rate = 0
    for i in range(6):
        total_rate += num_times[i] * rates[i]

    # Calculate probabilities
    prob[0] = num_times[0] * rates[0] / total_rate
    for i in range(5):
        prob[i + 1] = prob[i] + num_times[i + 1] * rates[i + 1] / total_rate

    # Choose event
    rand = np.random.random()

    # Absorption event
    if rand <= prob[0]:
        temp = np.floor(np.random.random() * num_times[0] + 1)
        if temp > num_times[0]:
            temp = num_times[0]
        temp = int(temp) - 1

        x = sites[0][temp][0]
        y = sites[0][temp][1]
        lattice[x, y] = 1

        # Periodic boundary conditions
        if x == 1:
            lattice[length + 1, y] = 1
        elif x == length:
            lattice[0, y] = 1

        if y == 1:
            lattice[x, length + 1] = 1
        elif y == length:
            lattice[x, 0] = 1

    # Desorption event
    elif rand > prob[0]:
        for i in range(5):
            if prob[i] < rand <= prob[i + 1]:
                temp = np.floor(np.random.random() * num_times[i + 1] + 1)
                if temp > num_times[i + 1]:
                    temp = num_times[i + 1]
                temp = int(temp) - 1

                x = sites[i + 1][temp][0]
                y = sites[i + 1][temp][1]
                lattice[x, y] = 0

                # Periodic boundary conditions
                if x == 1:
                    lattice[length + 1, y] = 0
                elif x == length:
                    lattice[0, y] = 0

                if y == 1:
                    lattice[x, length + 1] = 0
                elif y == length:
                    lattice[x, 0] = 0

    ## Record results
    # Calculate fractional coverage
    coverage = np.sum(lattice[1 : length + 1, 1 : length + 1]) / length**2
    results[run] = coverage

## Plotting
steps = np.arange(1, num_runs + 1)
plt.figure()
plt.plot(steps, results)
plt.xlabel("Steps")
plt.ylabel("Coverage")
plt.title("Coverage vs Steps")
plt.show()
