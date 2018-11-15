#!/usr/bin/env python

import subprocess
from lineages.lineages import csv2dict, Gen

def compare_records(rec1, rec2):
    '''Check that all fields in the two input records match.'''
    return rec1.fa == rec2.fa and rec1.mo == rec2.mo and rec1.sex == rec2.sex \
            and rec1.birth_place == rec2.birth_place and rec1.birth_year == rec2.birth_year


def check_ids(csv, csv_correct):
    '''Compare RIN IDs in produced CSV file to expected results.'''
    dd1 = csv2dict(csv)  # Output of ged2csv.py.
    dd2 = csv2dict(csv_correct)  # Expected results.

    # RIN IDs in actual and expected results respectively.
    ids1 = set(dd1.keys())
    ids2 = set(dd2.keys())

    # Check that the ID sets are identical.
    result = len(ids1.difference(ids2)) == 0

    return result


def check_records(csv, csv_correct):
    '''Compare records in produced CSV file to expected results.'''
    dd1 = csv2dict(csv)  # Output of ged2csv.py.
    dd2 = csv2dict(csv_correct)  # Expected results.

    # RIN IDs.
    ids = set(dd1.keys())

    # For each record, make sure the information in actual and expected results are identical.
    # If any record has a mismatch, we set result to False.
    result = True
    for i in ids:
        # Get records.
        rec1 = dd1[i]
        rec2 = dd2[i]
        # Compare records.
        if compare_records(rec1, rec2) is False:
            result = False

    return result

def check_gen_ids(csv, csv_correct):
    '''Compare RIN IDs in Gen object to expected results.'''
    gen1 = Gen(csv, [1])
    dd2 = csv2dict(csv_correct)  # Expected results.

    # RIN IDs in actual and expected results respectively.
    ids1 = set(gen1.individuals)
    ids2 = set(dd2.keys())

    # Check that the ID sets are identical.
    result = len(ids1.difference(ids2)) == 0

    return result


def check_gen_records(csv, csv_correct):
    '''Compare records in Gen object to expected results.'''
    gen = Gen(csv, [1])
    dd = csv2dict(csv_correct)  # Expected results.

    # RIN IDs in actual and expected results respectively.
    ids = set(gen.individuals)

    # For each record, make sure the information in actual and expected results are identical.
    # If any record has a mismatch, we set result to False.
    result = True
    for i in ids:
        # Get records.
        rec1 = gen.get(i)
        rec2 = dd[i]
        # Compare records.
        if compare_records(rec1, rec2) is False:
            result = False

    return result


if __name__ == '__main__':
    data_dir = 'test_data'

    # Input data.
    ged = data_dir + '/small_test_tree.ged'
    csv_correct = data_dir + '/correct_results.csv'
    inds = data_dir + '/test_individuals.txt'

    # Output data.
    csv = data_dir + '/small_test_tree.csv'
    ged_cleaned = data_dir + '/small_test_tree_cleaned.ged'
    exec_out = data_dir + '/small_test_tree_lineages_exec.csv'

    print('Cleaning up GED data.')
    subprocess.check_output('ged_cleanup.sh %s %s' %(ged, ged_cleaned), shell=True)

    print('Converting from GED to CSV.')
    subprocess.check_output('ged2csv.py %s %s' %(ged_cleaned, csv), shell=True)

    print('Checking data in CSV.')
    result = check_ids(csv, csv_correct)
    assert result, "RIN IDs in CSV file don't match the expected."
    result = check_records(csv, csv_correct)
    assert result, 'Information in at least one record in CSV file does not match the expected.'
    result = check_gen_ids(csv, csv_correct)
    assert result, "RIN IDs in Gen object don't match the expected."
    result = check_gen_records(csv, csv_correct)
    assert result, 'Information in at least one record in Gen object does not match the expected.'

    # Check records when executing lineages.py directly.
    subprocess.call('lineages.py --csv %s --ind %s --out %s' %(csv, inds, exec_out), shell=True)
    result = check_ids(exec_out, csv_correct)
    assert result, "RIN IDs in CSV file produced from executing lineage.py directly don't match the expected."
    result = check_records(exec_out, csv_correct)
    assert result, 'Information in at least one record in CSV from executing lineages.py directly does not match the expected.'

    print('All tests have succeeded.')

    print('Removing temporary files.')

    subprocess.check_call('rm %s %s %s' %(ged_cleaned, csv, exec_out), shell=True)


