from resources.const import GREEN, RED, ORANGE
from resources.helper_funcs import swap


def sift_down(draw_list, draw_info, lst, i, upper, ascending=True):
    # sift the new first element, i, to its appropriate index in the heap - mantains max/min heap property

    # i = parent/root element
    # upper = upper bound index of list = n

    while True:
        l, r = 2 * i + 1, 2 * i + 2  # indexes of left and right children

        if (
            max(l, r) < upper
        ):  # if there are 2 children then children's indices have to be smaller than upper bound to be valid
            if (lst[i] >= max(lst[l], lst[r]) and ascending) or (
                lst[i] <= min(lst[l], lst[r]) and not ascending
            ):  # if parent node is greater/less than child nodes don't need to swap
                break
            elif (lst[l] > lst[r] and ascending) or (
                lst[l] < lst[r] and not ascending
            ):  # if left child largest/smallest swap left child with parent
                swap(lst, i, l)
                draw_list(draw_info, {i: GREEN, l: RED}, True)
                i = l
            else:  # else right child largest/smallest swap right child with parent
                swap(lst, i, r)
                draw_list(draw_info, {i: GREEN, r: RED}, True)
                i = r
        elif (
            l < upper
        ):  # if there is one child that child is a left node then it's index has to be smaller than upperbound to be valid
            if (lst[l] > lst[i] and ascending) or (lst[l] < lst[i] and not ascending):
                swap(lst, i, l)
                draw_list(draw_info, {i: GREEN, l: RED}, True)
                i = l
            else:
                break
        elif (
            r < upper
        ):  # if there is one child that child is a right node then it's index has to be smaller than upperbound to be valid
            if (lst[r] > lst[i] and ascending) or (lst[r] < lst[i] and not ascending):
                swap(lst, i, r)
                draw_list(draw_info, {i: GREEN, r: RED}, True)
                i = r
            else:
                break
        else:  # no children
            break


def heap_sort(draw_list, draw_info, ascending=True):
    lst = draw_info.lst
    n = len(lst)

    # (n-2)//2 = index of very last parent
    for i in range((n - 2) // 2, -1, -1):  # heapify
        sift_down(draw_list, draw_info, lst, i, n, ascending)
        yield True

    for end in range(n - 1, 0, -1):  # sort list
        swap(lst, 0, end)
        draw_list(draw_info, {0: GREEN, end: ORANGE}, True)
        sift_down(draw_list, draw_info, lst, 0, end, ascending)
        yield True

    return lst
