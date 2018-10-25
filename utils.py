#!/usr/bin/env python
'''
Functions for working with genealogies (dictionaries or Gen objects).
'''


def calc_depth(ind, gen, d=0, depth=0):
    '''
    Calculate the total generational depth of the lineage of a single individual.

    Example:
        depth = calc_depth(1, gen)

    Input:
        ind:        Integer, ID of individual.
        gen:        Dictionary, genealogy object.
        d:          Integer, current generational depth, do not change [0].
        depth:      Integer, total generational depth, do not change [0].

    Returns:
    '''

    # Get the record corresponding to the individual.
    rec = gen.get(ind)

    assert rec is not None, 'Individual %d does not exist in genealogy.' % ind

    # If current depth is larger than the total, update depth.
    if d > depth:
        depth = d

    # Get IDs of parents.
    fa = rec.fa
    mo = rec.mo

    # If the parent exists (ID different from 0), make a recursive call.
    # Pass all parameters on in the recursive call, and increment the depth.
    # The recursive call will return the resulting generational depth.
    if fa != 0 and gen.get(fa) is not None:
        depth = calc_depth(fa, gen, d+1, depth)
    if mo != 0 and gen.get(mo) is not None:
        depth = calc_depth(mo, gen, d+1, depth)

    return depth

