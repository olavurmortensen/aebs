#!/usr/bin/env python
'''
Functions for reading in and extracting information from genealogies produced by ged2csv.py. This script can also be executed direclty, to read in a genealogy and reconstruct the genealogy of specified individuals. See `Gen` class to learn how to use this class.

Usage:
    python lineages.py --csv [CSV] --ind [individuals] --out [output]

Input:
    CSV:              Input CSV file with genealogy.
    Individuals:      Text file with RIN of individuals to reconstruct.
    Output:           Filename to write resulting CSV to.
'''

import pandas as pd
import numpy as np
import warnings, argparse


class Record(object):
    def __init__(self, fa, mo, sex, by, bp):
        self.fa = fa
        self.mo = mo
        self.sex = sex
        self.birth_place = bp
        self.birth_year = by


def csv2dict(csv):
    '''Read genealogy from CSV into a dictionary of individual objects.'''

    # Read CSV into dataframe.
    df = pd.read_csv(csv)

    dd = dict()
    for i, row in df.iterrows():
        # Obtain row of dataframe.
        # Check that ID isn't already in dictionary.
        if row.ind in dd:
            warnings.warn('Individual RIN %d is associated with multiple records. Ignoring all but first seen record.' %row.ind, Warning)
        else:
            # Add record to dictionary.
            if np.isnan(row.birth_year):
                birth_year = np.nan
            else:
                birth_year = int(row.birth_year)

            dd[row.ind] = Record(row.father, row.mother, row.sex, birth_year, row.birth_place)

    return dd


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

    # Get record corresponding to individual.
    rec = gen.get(ind)

    assert rec is not None, 'Individual %d does not exist in genealogy.' % ind

    # If we have reached the minimum birth year or the maximum genereational depth, we do
    # nothing.
    if by is not None and rec.birth_year < by or depth is not None and d > depth:
        return lin

    # Add record to lineage.
    lin[ind] = rec

    # Get IDs of the individual's parents.
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


def sim_gen(ind, gen, d, dmax, sex):

    if d > dmax:
        return gen

    fa = np.random.randint(1, 1000000)
    mo = np.random.randint(1, 1000000)

    while fa in gen:
        fa = np.random.randint(1, 1000000)
    while fa in gen:
        mo = np.random.randint(1, 1000000)

    gen[ind] = Record(fa, mo, sex, None, None)

    gen = sim_gen(fa, gen, d+1, dmax, 1)
    gen = sim_gen(mo, gen, d+1, dmax, 2)

    return gen


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
                fid.write('%d,%d,%d,%s,"%s",%s\n' %(ind, rec.fa, rec.mo, rec.sex, rec.birth_place, rec.birth_year))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Arguments for parser.
    parser.add_argument('--csv', type=str, required=True)
    parser.add_argument('--ind', type=str, required=True)
    parser.add_argument('--out', type=str, required=True)
    parser.add_argument('--by_thres', type=int)
    parser.add_argument('--d_thres', type=int)

    # Parse input arguments.
    args = parser.parse_args()

    csv_path = args.csv
    ind_path = args.ind
    out_path = args.out
    birth_year = args.by_thres
    depth = args.d_thres

    # Read lines in individual list.
    ind = open(ind_path).readlines()
    # Remove whitespace.
    ind = [int(i.strip()) for i in ind]

    # Construct a genealogy of three specific individuals from CSV file.
    gen = Gen(csv_path, ind, depth=depth, by=birth_year)

    # Write genealogy to CSV.
    gen.write_csv(out_path)



