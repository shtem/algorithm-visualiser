from resources.const import GREEN, RED
from resources.helper_funcs import swap


def bubble_sort(draw_list, draw_info, ascending=True):  # generator
    lst = draw_info.lst

    for i in range(len(lst) - 1):  # execute n - 2 times, n = lenght of list
        for j in range(len(lst) - 1 - i):  # compare adjacent values with each other
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (
                num1 < num2 and not ascending
            ):  # if they are in the incorrect position swap them
                swap(lst, j, j + 1)
                draw_list(draw_info, {j: GREEN, j + 1: RED}, True)
                yield True
            # call this function for each swap, yield control back to function that called it instead of performing the whole algorithm, and wait to be called again
            # -> pause the execution of the function, then resume it -> saves state from when it yielded from last time
    return lst
