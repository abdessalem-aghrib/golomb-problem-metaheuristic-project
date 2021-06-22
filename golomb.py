import random
from time import time
import numpy as np

np.seterr(divide='ignore', invalid='ignore', all='ignore')


def is_golomb_ruler(ruler: list[int]) -> bool:
    marks_count = len(ruler)

    # check if first element is not 0
    if ruler[0] != 0:
        return False

    # check if contains negative values
    for item in ruler:
        if item < 0:
            return False

    # check differences table
    tab_diff = []

    for i in range(marks_count - 1):
        d = ruler[i + 1] - ruler[i]
        if tab_diff.__contains__(d):
            return False

        tab_diff.append(d)

    index = marks_count - 2
    diff_len = 2
    for i in range(index, 0, -1):
        for j in range(i):
            d = 0
            for k in range(diff_len):
                d += tab_diff[k + j]

            if tab_diff.__contains__(d):
                return False

            tab_diff.append(d)

        diff_len += 1

    # case of two identical marks
    if tab_diff.__contains__(0):
        return False

    return True


def generate_golomb_ruler(marks_count: int, max_bound: int, max_generate_time: float) -> list[int]:
    if max_bound < marks_count:
        return []

    new_ruler = [0 for _ in range(marks_count)]

    start = time()
    while not is_golomb_ruler(new_ruler) and ((time() - start) < max_generate_time):
        for v in range(marks_count - 1):
            # generate a random value that not exist in new ruler
            random_value = random.randint(1, max_bound)
            while new_ruler.__contains__(random_value):
                random_value = random.randint(1, max_bound)

            new_ruler[v + 1] = random_value

        new_ruler.sort()

    if not is_golomb_ruler(new_ruler):
        return []

    return new_ruler


def correct_golomb_ruler(ruler: list[int], original_ruler: list[int], max_trying_time: float) -> list[int]:
    golomb_ruler = ruler.copy()
    golomb_ruler.sort()

    if is_golomb_ruler(golomb_ruler):
        return golomb_ruler

    marks_count = len(golomb_ruler)
    current_max_bound = golomb_ruler[marks_count - 1]

    # print(f'\truler to correct : {golomb_ruler}')

    interval = [k for k in range(1, current_max_bound, 1) if k not in golomb_ruler]

    # try to correct the current ruler
    for i in range(marks_count - 1, 0, -1):
        temp_ruler = golomb_ruler.copy()  # second way
        for item in interval:
            # temp_ruler = golomb_ruler.copy()
            temp_ruler[i] = item
            temp_ruler.sort()

            # check if golomb ruler
            if is_golomb_ruler(temp_ruler) and temp_ruler != original_ruler:
                return temp_ruler

    # fail to correct current ruler, so generate the new one

    # try to generate it with max bound of the current ruler
    golomb_ruler = generate_golomb_ruler(marks_count, current_max_bound, max_generate_time=max_trying_time)
    if len(golomb_ruler) != 0:
        return golomb_ruler

    '''
    # generate new ruler with original max bound
    golomb_ruler = generate_golomb_ruler(marks_count, original_ruler[marks_count - 1],
                                         max_generate_time=max_trying_time)
    if len(golomb_ruler) != 0:
        return golomb_ruler
    '''

    return original_ruler
