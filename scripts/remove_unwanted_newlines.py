#!/usr/bin/env python
'''
Remove unwanted newlines from Gedcom file.

Usage:
    python remove_unwanted_newlines.py myfile.ged > outputfile.ged
'''

import sys

# Input file.
path = sys.argv[1]

def is_int(string):
    '''Checks whether string represents an integer.'''
    try:
        int(string)
    except ValueError:
        return False
    return True

with open(path) as fid:
    for i, line in enumerate(fid):
        # Just print first line, which should be '0 HEAD'.
        if i == 0:
            print(line.strip(), end='')
            continue

        # Strip line of whitespace.
        line = line.strip()

        if len(line) == 0:
            # Empty line, ignore.
            continue
        elif not is_int(line[0]):
            # Continuation of previous line.
            print(' ' + line, end='')
        else:
            # End previous line with newline.
            # Write the next line.
            print('\n' + line, end='')


