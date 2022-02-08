from random import randrange
from resources.const import GREEN, RED, ORANGE
from resources.helper_funcs import swap


def partition(draw_list, draw_info, lst, start, end, ascending=True):
    rand_pivot = randrange(start, end)  # random pivot point chosen
    swap(lst, rand_pivot, end)  # place pivot element at end of the list

    pivot = lst[end]
    p_index = start

    for i in range(start, end):  # for each element that is not the pivot
        curr = lst[i]

        if (curr <= pivot and ascending) or (
            curr >= pivot and not ascending
        ):  # if current element is in the incorrect position then move element to the correct side of pivot
            swap(lst, i, p_index)
            draw_list(draw_info, {i: GREEN, p_index: RED}, True)
            p_index += 1

    swap(lst, p_index, end)
    draw_list(draw_info, {end: ORANGE, p_index: RED}, True)

    return p_index


def quick_sort_aux(draw_list, draw_info, lst, start, end, ascending=True):
    if start < end:

        # p_index is partitioning index, lst[p] is at correct position
        p_index = partition(draw_list, draw_info, lst, start, end, ascending)

        # Separately sort elements before partition and after partition
        yield from quick_sort_aux(
            draw_list, draw_info, lst, start, p_index - 1, ascending
        )
        yield from quick_sort_aux(
            draw_list, draw_info, lst, p_index + 1, end, ascending
        )

    yield True


def quick_sort(draw_list, draw_info, ascending=True):
    # randomised quicksort

    lst = draw_info.lst
    start = 0
    end = len(lst) - 1

    yield from quick_sort_aux(draw_list, draw_info, lst, start, end, ascending)

    return lst
