test = [1412990, 1416625, 2143485, 2151616, 2572447]


delta = 10000


def split_list(list):

    result = []
    bin = []

    for this_element in list:
        if len(bin) == 0:
            bin.append(this_element)

        elif this_element - bin[-1] > delta:
            result.append(bin.copy())
            bin.clear()
            bin.append(this_element)
        else:
            bin.append(this_element)

    if len(bin) > 0:
        result.append(bin)

    return result


print(split_list(test))






