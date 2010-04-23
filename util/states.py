def find_matching(iterable_states1, iterable_states2):
    s1 = set(iterable_states1)
    s2 = set(iterable_states2)
    inter = s1.intersection(s2))
    if inter:
        return list(inter)[0]
    else:
        raise RuntimeError('No matching states found.')
