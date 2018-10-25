#!/usr/bin/env python
'''
Functions for reading in and extracting information from genealogies produced by ged2csv.py.
'''

import pandas as pd
import numpy as np
import warnings


class Individual(object):
    def __init__(self, fa, mo, sex, by, bp):
        self.fa = fa
        self.mo = mo
        self.sex = sex
        self.birth_place = by
        self.birth_year = bp


def csv2dict(csv):
    '''Read genealogy from CSV into a dictionary of individual objects.'''

    # Read CSV into dataframe.
    df = pd.read_csv(csv)

    dd = dict()
    for i in range(len(df)):
        # Obtain row of dataframe.
        row = df.loc[i]
        # Check that ID isn't already in dictionary.
        if row.ind in dd:
            warnings.warn('Individual RIN %d is associated with multiple records. Ignoring all but first seen record.' %row.ind, Warning)
        else:
            # Add record to dictionary.
            #dd[row.ind] = {'fa': row.father, 'mo': row.mother, 'sex': row.sex, 'birth_place': row.birth_place, 'birth_year': row.birth_year}
            dd[row.ind] = Individual(row.father, row.mother, row.sex, row.birth_place, row.birth_year)

    return dd


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


def lineage(ind, gen, lin, depth=None, d=0, by=None):
    '''
    Generate lineage of a single individual based on complete genealogy available.

    This method starts with a single individual and recursively obtains the parents of an individual,
    until either there are no more ancestors, or a stopping criteria is met.

    Example:
        lin = lineage(1, gen, dict())
        lin2 = lineage(1, gen, dict(), depth=5, by=1800)

    Input:
        ind:        Integer, ID of individual.
        gen:        Dictionary, genealogy object.
        lin:        Dictionary, set to empty dictionary (`dict()`).
        depth:      Integer, total generational depth allowed [`None`].
        d:          Integer, current generational depth, do not change [0].
        by:         Integer, minimum allowed birth year of ancestor [`None`].

    Returns:
    Dictionary, lineage of individual.
    '''

    # If the current individual is already in the genealogy, we do nothing.
    if ind in lin:
        return lin

    # If we have reached the maximum genereational depth, we do nothing.
    if depth is not None and d > depth:
        return lin

    # Get record corresponding to individual.
    rec = gen.get(ind)

    assert rec is not None, 'Individual %d does not exist in genealogy.' % ind

    # If we have reached the minimum birth year, we do nothing.
    if by is not None and rec.birth_year < by:
        return lin

    # Add record to lineage.
    lin[ind] = rec

    # Get IDs of the individual's parents.
    #fa = rec['fa']
    #mo = rec['mo']
    fa = rec.fa
    mo = rec.mo

    # If the parent exists (ID different from 0), make a recursive call, attempting
    # to add the parent.
    # Pass all parameters on in the recursive call, and increment the depth.
    # The recursive call will return the resulting lineage.
    if fa != 0:
        lin = lineage(ind=fa, gen=gen, depth=depth, d=d+1, lin=lin, by=by)
    if mo != 0:
        lin = lineage(ind=mo, gen=gen, depth=depth, d=d+1, lin=lin, by=by)

    return lin


def genealogy(inds, gen, lin, depth=None, d=0, by=None):
    '''
    Generate lineages of multiple individuals based on complete genealogy available.

    This method calls the `lineage` method, which generates the lineage of a single
    individual. See `lineage` for more details. The genealogy is generated iteratively
    one individual at a time, adding each lineage to the previous. The `lineage` method
    checks whether an individual is already added to the lineage, avoiding unnecessary
    CPU usage and memory overhead.

    The `depth` parameter specifies the depth of the individual lineages, and does not
    give any guarantees about the total generational depth of the complete genealogy.

    Example:
        gen2 = genealogy(1, gen, dict())
        gen3 = genealogy(1, gen, dict(), depth=5, by=1800)

    Input:
        inds:       List of integer, IDs of individuals.
        gen:        Dictionary, genealogy object.
        lin:        Dictionary, set to empty dictionary (`dict()`).
        depth:      Integer, total generational depth allowed [`None`].
        d:          Integer, current generational depth, do not change [0].
        by:         Integer, minimum allowed birth year of ancestor [`None`].

    Returns:
    Dictionary, genealogy of individuals.
    '''

    for ind in inds:
        lin = lineage(ind, gen, lin, depth, d, by)

    return lin


class Gen(object):
    def __init__(self, csv, inds, depth=None, by=None):
        '''
        Construct a genealogy object of specified individuals, taking ancestors from
        supplied CSV file.

        Examples:
            # Construct a genealogy of three specific individuals from CSV file.
            gen = Gen('path/to/genealogy.csv', [1,2,3])

            # Retrieve a single record.
            rec = gen.get(1)

            # Individual's parents.
            father = rec.fa
            mother = rec.mo

            # Number of individuals in genealogy.
            n = len(gen.individuals)

            # Write genealogy to CSV.
            gen.write_csv('small_genealogy.csv')

        Input:
            csv:        String, path to Gedcom ([filename].ged) file, produced by `ged2csv.py`.
            inds:       List of integer, IDs of individuals.
            depth:      Integer, total generational depth allowed [`None`].
            by:         Integer, minimum allowed birth year of ancestor [`None`].
        '''

        # Read genealogy into a dictionary of individual objects.
        # This dictionary includes all individuals in input genealogy.
        dd = csv2dict(csv)

        # Reconstruct genealogy of input individuals.
        self.gen = genealogy(inds, dd, dict(), depth=depth, by=by)

        # The genealogy which gen is created from is no longer needed.
        del dd

        self.individuals = list(self.gen.keys())


    def get(self, ind):
        return self.gen.get(ind)

    def write_csv(self, path):
        '''Write genealogy to a CSV file.'''
        with open(path, 'w') as fid:
            fid.write('ind,father,mother,sex,birth_place,birth_year\n')
            for ind in self.gen.keys():
                rec = self.get(ind)
                fid.write('%d,%d,%d,%s,%s,%s\n' %(ind, rec.fa, rec.mo, rec.sex, rec.birth_place, rec.birth_year))

