def nested_for(*fors, skip=None):
    """Equivalent to nested for loops for each iterable in fors.

    If skip is given, it must be a sequence where each item is an iterable
    containing items that must be skipped in the corresponding iterable in
    fors. The sequence may be shorter than the length of fors if the rest would
    be empty.

    :param fors:
    :param skip:
    :return:
    """

    if skip is None:
        skip = []

    fors = [list(x)[:] for x in fors]  # in case they're generators or something
    for i, bad in enumerate(skip):  # much quicker than checking at yield
        for x in bad:
            if x in fors[i]:
                try:
                    while True:
                        fors[i].remove(x)
                except ValueError:
                    continue
    if len(fors) == 0 or any(len(x) == 0 for x in fors):  # as it would've properly skipped it entirely
        return

    grab = [0 for _ in range(len(fors))]

    while True:
        grabbed = tuple(fors[i][grab[i]] for i in range(len(grab)))
        yield grabbed

        # increment grab
        to_inc = len(grab) - 1
        grab[to_inc] += 1
        while grab[to_inc] == len(fors[to_inc]):
            grab[to_inc] = 0
            to_inc -= 1
            if to_inc == -1:  # grab has reset to 0s, lists complete
                return
            grab[to_inc] += 1
