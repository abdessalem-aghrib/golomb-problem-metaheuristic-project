import golomb_simulated_annealing as gsa

# initial varibles

size_variables = int(input('Enter number of marks : ')) # marks number of golomb ruler
max_bound = int(input('Enter max bound of marks : ')) # max len of golomb ruler


# customization section

initial_temperature = 1000
cooling_coeff = 0.7 # cooling coefficient
computing_time = 3 # seconds
trials_number = 20 # number or trials to get neighborhood before use random one
attempts_in_each_level_of_temperature = 100 # number of attempts in each level of temperature


# main
result = gsa.golomb_simulated_annealing(size_variables,max_bound,initial_temperature,cooling_coeff,
    computing_time,trials_number,attempts_in_each_level_of_temperature)


print('\n\tinitial solution : {}\n\tbest_solution: {}\n\tbest_fitness: {}\n'.format(result["initial_solution"],result["best_solution"],result["best_fitness"]))



#plt.plot(record_best_fitness)
#plt.show()