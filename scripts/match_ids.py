#!/usr/bin/env python
#
# Takes two CSV files and matches the IDs in the second column, and writes a CSV with the first columns.
# Use this script to match P-numbers in Progeny with "REFN" numbers in AEBS.
#
# Usage:
# python match_ids.py [csv 1] [csv 2] [csv out] [txt out]
#
# Input:
# csv 1         CSV with two columns: sample ID and P-number from Progeny.
# csv 2         CSV with two columns: RIN and REFN from AEBS.
#
# Output:
# csv out       CSV with sample ID (csv 1) and RIN (csv 2) where P-number (csv 1) and REFN (csv 2) match.
# txt out       Text file with only the RIN in the CSV file.

import sys, warnings

assert len(sys.argv) > 2, 'To few arguments to "match_ids.py", see documentation for details.'

csv1_path = sys.argv[1]  # CSV with sample IDs and P-numbers.
csv2_path = sys.argv[2]  # CSV with RIN and REFN.
csv_out = sys.argv[3]  # CSV to write RIN and sample IDs.
txt_out = sys.argv[4]  # Text file with only RIN of samples.

def csv2dict(csv):
    '''
    Read CSV file to a dictionary. Discards first line as header.

    Input:
    csv:    CSV path.

    Output:
    Dictionary.
    '''
    dd = dict()
    with open(csv) as fid:
        # Discard header.
        tt = fid.readline()
        # Read all lines.
        for line in fid:
            # Extract fields.
            name, idd = line.strip().split(',')

            # Remove any trailing whitespace from name and idd.
            name = name.strip()
            idd = idd.strip()

            assert dd.get(name) is None, 'Error: row "%s" is a duplicate.' % name

            # Add row to dictionary.
            dd[name] = idd

    return dd

# Read both CSV files into dictionaries.
progeny_ids = csv2dict(csv1_path)
aebs_ids = csv2dict(csv2_path)

# Discard hyphen in P-number.
for sample, pnum in progeny_ids.items():
    idx = pnum.find('-')
    if idx > -1:
        # Hyphen found. Remove it from string.
        pnum = pnum[:idx] + pnum[idx+1:]

    # Check formatting of ID.
    #idd_len = len(idd)
    #assert idd_len == 9: 'Error: ID %s is incorrectly formatted.' % idd
    if len(pnum) != 9:
        warnings.warn('P-number should be of length 9 (excluding hyphen). Ignoring record with P-number: %s' %pnum, Warning)

    progeny_ids[sample] = pnum


# Discard all records with no REFN.
n_before = len(aebs_ids)
for rin, refn in list(aebs_ids.items()):
    if len(refn) == 0:
        del aebs_ids[rin]

n_after = len(aebs_ids)

print('Records with no REFN discarded: %d' % (n_before - n_after))

# Discard all records with REFN ending in 000.
n_before = len(aebs_ids)
for rin, refn in list(aebs_ids.items()):
    if refn[-3:] == '000':
        del aebs_ids[rin]

n_after = len(aebs_ids)

print('Records with REFN ending in "000" discarded: %d' % (n_before - n_after))

# Reformat REFN so that it matches that of P-number. The correct format is:
# ddmmYYXXX
# REFN that cannot be parsed are discarded.
refn_fail = 0
aebs_rev = dict() ##FIXME
for rin, refn in aebs_ids.items():
    if len(refn) != 11:
        warnings.warn('REFN should be of length 11. Ignoring record with REFN: %s' %refn, Warning)
        refn_fail += 1

    # Get birth date and three cipher ID from REFN.
    yyyy = refn[:4]
    mm = refn[4:6]
    dd = refn[6:8]
    XXX = refn[8:11]

    # Use two last digits of date.
    YY = yyyy[-2:]

    # Format new ID, and replace the old one.
    new_id = dd + mm + YY + XXX
    aebs_rev[new_id] = rin

warnings.warn('Number of records with problematic REFN discarded: %d' %refn_fail)

# Write a file with RIN and sample IDs.
csv_fid = open(csv_out, 'w')
txt_fid = open(txt_out, 'w')
# CSV file header.
csv_fid.write('rin,sample\n')
no_match = 0  # Number of samples with no matching AEBS record.
for sample, pnum in progeny_ids.items():
    if aebs_rev.get(pnum) is None:
        warnings.warn('P-number %s could not be matched with AEBS.' %pnum, Warning)
        no_match += 1
        continue

    # Get RIN corresponding to sample.
    rin = aebs_rev[pnum]

    csv_fid.write('%s,%s\n' %(rin, sample))
    txt_fid.write(rin + '\n')

warnings.warn('%d individuals were not found in AEBS.' %no_match, Warning)

