

# ged2csv

The folder "ged2csv" contains scripts used for converting from Gedcom format to a simple CSV format. The Gedcom data was exported from Legacy, to the Gedcom 5.5.1 format, using UTF-8 encoding. The exported data contains some unwanted newlines that make it not readable by Gedcom parsers. It also contains some Dos (Windows) characters that are unreadable in Unix environments such as Linux. So the data was cleaned up with the script "ged_cleanup.sh". Then the script "ged2csv.py" reads the Gedcom data and writes the relevant fields to a CSV file.

The [ged4py v0.1.9 Python package](https://github.com/andy-z/ged4py) was used to parse the Gedcom data.

The `export_list.gel` file is used when exporting data from Legacy, to include only the necessary fields. This includes some mandatory fields, and some others that are useful to us.

# Genealogy CSV format

The CSV files produced by `ged2csv.py` contains the following fields:

* ind: RIN ID of individual
* father: RIN ID of father of individual
* mother: RIN ID of mother of individual
* sex: "M" for male, "F" for female, and "U" for unknown
* birth_year: the year the individual was born
* birth_place: the name of the location the individual was born

# Lineages

`lineages.py` contains functions for reading in genealogies from a CSV produced by `ged2csv.py`, and working with these genealogies. The `Gen` class reads the records in a CSV into a dictionary, where each record is represented by the `Record` class. The `Gen` class reconstructs the genealogy of the input individuals, rather than just loading the entire genealogy in the CSV. The `lineages.py` script can also be executed from the commandline.

# Unit tests

Simple unit tests are implemented in `tests.py`, and test data is found in the `test_data` directory. To create a fictional family tree, the individuals were manually typed into Legacy, and exported to Gedcom 5.5.1 using UTF-8 encoding. The tests first convert the Gedcom data to CSV, then check that the records match the expected (which are manually typed into the `correct_results.csv` file), testing the functionality of the `csv2dict` function and the `Gen` class.



