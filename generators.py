def recursive_for(*enum, skip=None):
    if skip is None:
        skip = []

    enum = [list(x)[:] for x in enum]  # in case they're generators or something
    for i, bad in enumerate(skip):  # much quicker than checking at yield
        for x in bad:
            if x in enum[i]:
                try:
                    while True:
                        enum[i].remove(x)
                except ValueError:
                    continue
    if len(enum) == 0 or any(len(x) == 0 for x in enum):  # as it would've properly skipped it entirely
        return

    grab = [0 for _ in range(len(enum))]

    while True:
        grabbed = tuple(enum[i][grab[i]] for i in range(len(grab)))
        yield grabbed

        # increment grab
        to_inc = len(grab) - 1
        grab[to_inc] += 1
        while grab[to_inc] == len(enum[to_inc]):
            grab[to_inc] = 0
            to_inc -= 1
            if to_inc == -1:  # grab has reset to 0s, lists complete
                return
            grab[to_inc] += 1
