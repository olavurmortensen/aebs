#!/usr/bin/env python

import pandas as pd
import warnings

def csv2dict(csv):

    df = pd.read_csv(csv)

    dd = dict()
    for i in range(len(df)):
        row = df.loc[i]
        if row.ind in dd:
            warnings.warn('Individual RIN %d is associated with multiple records. Ignoring all but first seen record.' %row.ind, Warning)
        else:
            dd[row.ind] = {'fa': row.father, 'mo': row.mother, 'sex': row.sex, 'birth_place': row.birth_place, 'birth_year': row.birth_year}


    return dd

def calc_depth(ind, gen, d=0, depth=0):
    rec = gen.get(ind)

    assert rec is not None, 'Individual %d does not exist in genealogy.' % ind

    if d > depth:
        depth = d

    fa = rec['fa']
    mo = rec['mo']

    if fa != 0 and gen.get(fa) is not None:
        depth = calc_depth(fa, gen, d+1, depth)
    if mo != 0 and gen.get(mo) is not None:
        depth = calc_depth(mo, gen, d+1, depth)

    return depth


def lineage(ind, gen, lin, dmax=None, d=0, by=None):

    if ind in lin:
        return lin

    if dmax is not None and d > dmax:
        return lin

    rec = gen.get(ind)

    assert rec is not None, 'Individual %d does not exist in genealogy.' % ind

    if by is not None and rec['birth_year'] < by:
        return lin

    lin[ind] = rec

    fa = rec['fa']
    mo = rec['mo']

    if fa != 0:
        lin = lineage(ind=fa, gen=gen, dmax=dmax, d=d+1, lin=lin, by=by)
    if mo != 0:
        lin = lineage(ind=mo, gen=gen, dmax=dmax, d=d+1, lin=lin, by=by)

    return lin

def genealogy(inds, gen, lin, dmax=None, d=0, by=None):

    for ind in inds:
        lin = lineage(ind, gen, lin, dmax, d, by)

    return lin

