#!/usr/bin/env python
'''
TODO: documentation
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

# Initialize GED parser.
with GedcomReader(ged_path, encoding='utf-8') as parser:
    # iterate over all INDI records
    for i, record in enumerate(parser.records0('INDI')):
        # Get individual RIN ID.
        ind_ref = int(record.xref_id[2:-1])

        # Get the RIN ID of the individuals parents.
        # If the parent does not exist, set to 0.

        fa = record.father
        fa_ref = 0
        if not fa is None:
            if fa.xref_id is not None:
                fa_ref = int(fa.xref_id[2:-1])

        mo = record.mother
        mo_ref = 0
        if not mo is None:
            if mo.xref_id is not None:
                mo_ref = int(mo.xref_id[2:-1])

        # Get information about individual in a dictionary.
        ind_records = {r.tag: r for r in record.sub_records}

        sex = ind_records['SEX'].value

        birth = ind_records.get('BIRT')
        # If birth year or place is not found in record, it is set to NA.
        birth_year = 'NA'
        birth_place = 'NA'
        if birth is not None:
            birth_records = {r.tag: r for r in birth.sub_records}

            # Get birth year of individual.
            birth_date = birth_records.get('DATE')  # Date record, or None.
            if birth_date is not None:
                birth_date = birth_date.value  # DateValue object.
                birth_date = birth_date.fmt()  # Birth date as a string.
                # Match birth year in string using regex, as format is inconsistent.
                match = re.search('\d{4}', birth_date)  # Find four letter digit.
                if match:
                    birth_year = birth_date[match.start():match.end()]  # Birth year as a string.

                    # If the birth year is not an integer, something probably went wrong.
                    # Just make a warning.
                    try:
                        _ = int(birth_year)
                    except ValueError:
                        warnings.warn('Non integer birth year in record %d: %s' %(ind_ref, birth_year), Warning)

            # Get birth place of individual.
            birth_place = birth_records.get('PLAC')  # Get the record with tag "PLAC".
            if birth_place is not None:
                birth_place = birth_place.value

        # Add record to list.
        gen.append((ind_ref, fa_ref, mo_ref, sex, birth_year, birth_place))

# Convert list of records to dataframe and write to CSV.
gen = pd.DataFrame(data=gen, columns=('ind', 'father', 'mother', 'sex', 'birth_year', 'birth_place'))
gen.to_csv(csv_path, index=None)


