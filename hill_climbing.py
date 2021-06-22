import random


# Hill Climbing algorithm         
def hill_climbing(problem_function, algo_type, marks_count, max_bound, attempts_count=10):
    current = {}

    if algo_type == "simulated_annealing":
        # initial solution
        initial_temperature = random.uniform(1000, 50000)  # initial temperature
        cooling_coeff = random.random()  # cooling coefficient
        if cooling_coeff == 0.0: cooling_coeff = 0.1
        computing_time = random.uniform(0.3, 20.0)  # in seconds
        trials_number = random.randint(5, 50)  # number or trials to get neighborhood before use random one
        attempts_in_each_level_of_temperature = random.randint(5,
                                                               500)  # number of attempts in each level of temperature

        current["initial_temperature"] = initial_temperature
        current["cooling_coeff"] = cooling_coeff
        current["computing_time"] = computing_time
        current["trials_number"] = trials_number
        current["attempts_in_each_level_of_temperature"] = attempts_in_each_level_of_temperature

        neighbor = current.copy()

        current_result = problem_function(marks_count, max_bound, initial_temperature, cooling_coeff,
                                          computing_time, trials_number, attempts_in_each_level_of_temperature)

        while attempts_count > 0:
            # generate neighbor solution
            initial_temperature = random.uniform(500, 5000)  # initial temperature
            cooling_coeff = random.random()  # cooling coefficient
            if cooling_coeff == 0: cooling_coeff = 0.1
            computing_time = random.uniform(0.3, 20.0)  # in seconds
            trials_number = random.randint(5, 50)  # number or trials to get neighborhood before use random one
            attempts_in_each_level_of_temperature = random.randint(5, 500)  # number of attempts in each level of temperature

            neighbor["initial_temperature"] = initial_temperature
            neighbor["cooling_coeff"] = cooling_coeff
            neighbor["computing_time"] = computing_time
            neighbor["trials_number"] = trials_number
            neighbor["attempts_in_each_level_of_temperature"] = attempts_in_each_level_of_temperature

            neighbor_result = problem_function(marks_count, max_bound, initial_temperature, cooling_coeff,
                                               computing_time, trials_number, attempts_in_each_level_of_temperature)

            # check if neighbor solution is better than the current one
            if neighbor_result["best_fitness"] < current_result["best_fitness"] or (neighbor_result["best_fitness"]
                                                                                    == current_result[
                                                                                        "best_fitness"] and
                                                                                    neighbor_result["runtime"] <
                                                                                    current_result["runtime"]):
                current = neighbor.copy()

            # decrement attempts count
            attempts_count -= 1

    return current
