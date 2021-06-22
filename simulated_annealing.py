import time
import random
import math
import golomb as golomb


# -----------------------------------


def objective_function(ruler: list[int]) -> int:
    return ruler[len(ruler) - 1] - ruler[0]


def neighborhood_function(current_ruler: list[int], marks_count: int, max_bound: int, trials_number: int) -> list[int]:
    neighboring_ruler = current_ruler[:]

    # try to find best neighbor while trials > 0
    record_temp_rulers = []
    while trials_number > 0:
        random_number = random.randint(1, 4)
        if random_number > max_bound: random_number = max_bound - random_number
        random_position = random.randint(1, marks_count - 1)

        # create a temp ruler and record it if not exist before
        temp_ruler = []
        for item in current_ruler:
            temp_ruler.append(item)

        temp_ruler[random_position] -= random_number

        temp_ruler.sort()

        if not record_temp_rulers.__contains__(temp_ruler):
            record_temp_rulers.append(temp_ruler)

        # check if golomb ruler (correct ruler)
        if golomb.is_golomb_ruler(temp_ruler):
            neighboring_ruler = temp_ruler
            break

        trials_number -= 1

    # if fail to find best neighbor, generate a random one
    if trials_number == 0:
        neighboring_ruler = golomb.generate_golomb_ruler(marks_count, max_bound, max_generate_time=3600)

    return neighboring_ruler


def simulated_annealing(marks_count: int, max_bound: int,
                        initial_temperature: float, cooling_coeff: float, computing_time: float,
                        trials_number: int, attempts_in_each_level_of_temperature: int) -> dict:
    # begin time
    start = time.time()

    initial_ruler = golomb.generate_golomb_ruler(marks_count, max_bound, max_generate_time=3600)

    current_ruler = initial_ruler
    best_ruler = initial_ruler

    n = 1  # number of accepted rulers
    i = 1  # iteration number

    best_fitness = objective_function(best_ruler)
    current_temperature = initial_temperature  # current temperature
    # record_best_fitness = []

    # stop by computing time
    while time.time() - start < computing_time:
        for j in range(attempts_in_each_level_of_temperature):

            current_ruler = neighborhood_function(current_ruler, marks_count,
                                                  max_bound, trials_number)

            if len(current_ruler) == 0:
                raise ValueError("Fail to find the neighbor ruler")

            current_fitness = objective_function(current_ruler)

            if current_fitness > best_fitness:
                try:
                    p = math.exp((best_fitness - current_fitness) / current_temperature)
                except:
                    pass
                r = random.random()

                # make a decision to accept the worse ruler or not
                if r < p:
                    accept = True  # this worse ruler is accepted
                else:
                    accept = False  # this worse ruler is not accepted
            else:
                accept = True  # accept better ruler

            if accept:
                best_ruler = current_ruler  # update the best ruler
                best_fitness = objective_function(best_ruler)
                n = n + 1  # count the rulers accepted

            # end For Loop
        # end For Loop

        i += 1  # increment iterations number
        # record_best_fitness.append(best_fitness)

        # cooling the temperature
        current_temperature = current_temperature * cooling_coeff

        # end time
        end = time.time() - start

    # end While Loop

    return {"initial_ruler": initial_ruler,
            "best_ruler": best_ruler,
            "best_fitness": best_fitness,
            "runtime": end}
