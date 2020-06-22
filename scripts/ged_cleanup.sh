#!/bin/bash
#
# Cleans up Gedcom data ([filename].ged) by replacing Dos characters by Unix characters
# and removing unwanted newlines. The newlines occurr in the middle of Gedcom lines,
# or as extra newlines causing empty lines.
#
# Usage:
# ./ged_cleanup.sh myfile.ged outputfile.ged

in=$1
out=$2

temp=$out\_temp.ged
dos2unix -n $in $temp

echo 'Removing unwanted newlines from GEDCOM file.'
remove_unwanted_newlines.py $temp > $out

rm $temp


