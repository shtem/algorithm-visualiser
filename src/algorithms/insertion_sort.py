from resources.const import GREEN, RED


def insertion_sort(draw_list, draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):  # first element is in sorted subset
        curr = lst[
            i
        ]  # select a number from list so we can insert it in the correct position by swapping

        while True:
            ascending_sort = (
                i > 0 and lst[i - 1] > curr and ascending
            )  # if ascending we want to check if current number is less than previous number so we can swap
            descending_sort = (
                i > 0 and lst[i - 1] < curr and not ascending
            )  # if descending we want to check if current number is greater than previous number so we can swap

            if not ascending_sort and not descending_sort:
                break  # if both these conditions are not true we break, don't swap

            # swap current number with previous number
            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = curr
            draw_list(draw_info, {i - 1: GREEN, i: RED}, True)
            yield True

    return lst
