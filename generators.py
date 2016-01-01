def nested_for(*fors, skip=None):
    """Equivalent to nested for loops for each iterable in fors. The end result is
    similar to the working of a clock or an odometer.

    Yields a tuple the length of the number of iterables given.

    If skip is given, it must be a sequence where each item is an iterable
    containing items that must be skipped in the corresponding iterable in
    fors. Skip may be smaller than the length of fors if the rest of it would
    be empty. Suggested you use empty tuples or lists to get to the desired
    place, e.g. [(), (), 'aoeui']

    Fun fact:
        The number of tuples that will be yielded is equal to the product of
        the lengths of all the iterables in fors

    Warning:
        It will be unable to detect if an infinite generator was passed as an
        iterable and this will result in the infinite cycle before the first
        tuple is yielded.

    Example:
        >>> for x in nested_for(range(1, 4, 2), 'abc', range(2, 5, 2), skip=[(), 'a']):
        >>>     print(x)
        (1, 'b', 2)
        (1, 'b', 4)
        (1, 'c', 2)
        (1, 'c', 4)
        (3, 'b', 2)
        (3, 'b', 4)
        (3, 'c', 2)
        (3, 'c', 4)

    :param fors: some iterables
    :param skip: a sequence of iterables
    :returns: None
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
    if len(fors) == 0 or any(len(x) == 0 for x in fors):
        return  # as it would've properly skipped it entirely

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
help(nested_for)
