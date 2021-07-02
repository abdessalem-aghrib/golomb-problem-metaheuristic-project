import random
import time
import itertools


def is_golomb_ruler(ruler: list[int]) -> bool:
    marks_count = len(ruler)

    # check if first element is not 0
    if len(ruler) == 0 or ruler[0] != 0:
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


# get differences table of golomb ruler
def get_differences_table(diff_count: int, stop: list[bool], numbers_interval: list[int],
                          n: int, k: int, diff_tab_output: list[int], partial=[]):
    if stop[0]:
        return

    s = sum(partial)

    # check if the partial sum is equals to target
    if s == n:
        if len(partial) == k:
            # for each combination try to find a best_combination to build golomb ruler . stop when find one
            for combination in list(itertools.permutations(partial)):

                # consider that this combination is true
                correct_combination = True

                # reset differences table to null
                diff_tab = [0 for _ in range(diff_count)]

                # fill the first (k=marks_count-1) cases of differences table
                for d in range(len(combination)):
                    diff_tab[d] = combination[d]

                # fill other cases
                current_index = k
                index = k - 1
                diff_len = 2
                for i in range(index, 0, -1):
                    if correct_combination:
                        for j in range(i):

                            d = 0
                            for g in range(diff_len):
                                d += diff_tab[g + j]

                            if diff_tab.__contains__(d):
                                # wrong combination, change them with new one
                                correct_combination = False
                                break

                            diff_tab[current_index] = d
                            current_index += 1

                        diff_len += 1

                    else:
                        break

                if correct_combination:
                    stop[0] = True
                    for diff in diff_tab:
                        diff_tab_output.append(diff)
                    return

    if s >= n:
        return  # if we reach the number why bother to continue

    for z in range(len(numbers_interval)):
        v = numbers_interval[z]
        remaining = numbers_interval[z + 1:]
        get_differences_table(diff_count=diff_count, stop=stop, numbers_interval=remaining,
                              n=n, k=k, diff_tab_output=diff_tab_output, partial=partial + [v])


def generate_golomb_ruler(marks_count: int, max_bound: int, max_generate_time: float) -> list[int]:
    if max_bound < marks_count:
        return []

    new_ruler = [0 for _ in range(marks_count)]

    # >>> First way : used when the max bound is big so we used the random method
    start = time.time()
    while (time.time() - start) < max_generate_time:
        for v in range(marks_count - 1):
            # generate a random value that not exist in new ruler
            random_value = random.randint(1, max_bound)
            while new_ruler.__contains__(random_value):
                random_value = random.randint(1, max_bound)

            new_ruler[v + 1] = random_value

        new_ruler.sort()

        if is_golomb_ruler(new_ruler):
            return new_ruler

    # >>> Second way : used when the max bound is minimal
    new_ruler = [0 for _ in range(marks_count)]

    # differences count
    diff_count = int(marks_count * (marks_count - 1) / 2)

    for last_diff in range(max_bound, 6, -1):

        max_interval = int(last_diff - (marks_count - 1) * (marks_count - 2) / 2)
        numbers_interval = [k for k in range(1, max_interval + 1)]  # TODO : check max bound here

        # get differences table of golomb ruler
        diff_tab = []

        get_differences_table(diff_count=diff_count, stop=[False], numbers_interval=numbers_interval,
                              n=last_diff, k=marks_count - 1, diff_tab_output=diff_tab)

        # build golomb ruler with best_combination founded
        if len(diff_tab) != 0:
            for i in range(marks_count - 1):
                new_ruler[i + 1] = new_ruler[i] + diff_tab[i]

            # stop algorithm
            return new_ruler

    # no rule found
    return []


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
        temp_ruler = golomb_ruler.copy()  # TODO : decide place of this line
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
