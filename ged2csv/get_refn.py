#!/usr/bin/env python
'''
Reads records from a Gedcom file ([filename].ged) and writes two fields to CSV: RIN and REFN.

Usage:
    ged2csv.py [GED filename] [CSV filename]

Arguments:
    GED filename:       Path to a Gedcom file.
    CSV filename:       Path to output CSV file.
'''

from ged4py import GedcomReader
import pandas as pd
import sys, re, warnings

assert len(sys.argv) > 2, 'To few arguments to "ged2csv.py", see documentation for details.'

ged_path = sys.argv[1]  # Path to input GED file.
csv_path = sys.argv[2]  # Path to output CSV file.

# List to store relevant fields of all records in.
gen = list()

count_none_rin = 0

def format_rin(rin):
    '''Extract RIN, as Gedcom represents RIN as e.g. @I1@.'''
    return rin[2:-1]

# Initialize GED parser.
with GedcomReader(ged_path, encoding='utf-8') as parser:
    # iterate over all INDI records
    for i, record in enumerate(parser.records0('INDI')):
        # Get individual RIN ID.
        ind_ref = int(format_rin(record.xref_id))

        # Get the records of the individual.
        ind_records = {r.tag: r for r in record.sub_records}

        # Get the record with tag "REFN".
        refn = ind_records.get('REFN')
        if refn is not None:
            refn = refn.value

        # Add record to list.
        gen.append((ind_ref, refn))

# Convert list of records to dataframe and write to CSV.
gen = pd.DataFrame(data=gen, columns=('RIN', 'REFN'))
gen.to_csv(csv_path, index=None)


