import time
import random
import math
import numpy as np
import matplotlib.pyplot as plt

#-----------------------------------


def objective_function(X):
    return X[len(X)-1]

def check_golomb_ruler(solution):
    size_variables = len(solution)

    # check if first element is not 0
    if solution[0] != 0: return False

    # check if contains negative values
    for item in solution:
        if item < 0: return False

    # check differences table
    tab_diff = []

    for i in range(size_variables-1):
        d = solution[i+1]-solution[i]
        if tab_diff.__contains__(d): return False
        tab_diff.append(d)
    
    index = size_variables - 2
    diff_len = 2
    for i in range(index,0,-1):
        for j in range(i):
            d = 0
            for k in range(diff_len):
                d += tab_diff[k+j] 
                
            if tab_diff.__contains__(d): return False
            tab_diff.append(d)

        diff_len +=1
    
    # case of two identical marks
    if tab_diff.__contains__(0): return False

    return True

def random_solution(size_variables,max_bound):
    new_solution = np.zeros(size_variables).astype(int)

    while(check_golomb_ruler(new_solution) == False):
        for v in range(size_variables-1):
            # generate a random value that not exist in new solution
            random_value = random.randint(1,max_bound)
            while new_solution.__contains__(random_value):
                random_value = random.randint(1,max_bound)

            new_solution[v+1] = random_value
             
        new_solution.sort()

    return new_solution

def neighborhood_function(current_solution,size_variables,max_bound,trials_number=20):
    neighboring_solution = current_solution[:]

    # try to find best neighbor while trials > 0
    record_temp_solutions = []
    while trials_number > 0:
        random_number = random.randint(1,4)
        if random_number>max_bound: random_number = max_bound - random_number
        random_position = random.randint(1,size_variables-1)

        # create a temp solution and record it if not exist before
        temp_solution = []
        for item in current_solution:
            temp_solution.append(item)
        
        temp_solution[random_position] -= random_number
        
        temp_solution.sort()
        
        if record_temp_solutions.__contains__(temp_solution) == False:
            record_temp_solutions.append(temp_solution)

        # check if golomb ruler (correct solution)
        if check_golomb_ruler(temp_solution):
            neighboring_solution = temp_solution
            break
            
        trials_number -=1

    # if fail to find best neighbor, generate a random one
    if trials_number == 0:
        neighboring_solution = random_solution(size_variables,max_bound)
            

    return neighboring_solution


# Simulted Annealing Algorithm :
def golomb_simulated_annealing(size_variables,max_bound,
        initial_temperature,cooling_coeff,computing_time,
        trials_number,attempts_in_each_level_of_temperature):

    initial_solution = random_solution(size_variables,max_bound)

    current_solution = initial_solution
    best_solution = initial_solution

    n = 1 # number of accepted solutions
    i = 1 # iteration number

    best_fitness = objective_function(best_solution)
    current_temperature = initial_temperature # current temperature
    record_best_fitness = []

    start = time.time()

    # stop by computing time
    while time.time()-start < computing_time:
        for j in range(attempts_in_each_level_of_temperature):

            current_solution = neighborhood_function(current_solution,size_variables,
                max_bound,trials_number)
            current_fitness = objective_function(current_solution)
            
            if current_fitness > best_fitness:
                p = math.exp((best_fitness-current_fitness)/current_temperature)
                r = random.random()

                # make a decision to accept the worse solution or not
                if r<p:
                    accept = True # this worse solution is accepted
                else:
                    accept = False # this worse solution is not accepted
            else:
                accept = True # accept better solution

            if accept:
                best_solution = current_solution # update the best solution
                best_fitness = objective_function(best_solution)
                n = n + 1 # count the solutions accepted
            
            # end For Loop
        # end For Loop

        i += 1 # increment iterations number
        #record_best_fitness.append(best_fitness)

        # cooling the temperature
        current_temperature = current_temperature * cooling_coeff

    # end While Loop

   
    return {"initial_solution" : initial_solution, "best_solution" : best_solution, "best_fitness" : best_fitness}  


