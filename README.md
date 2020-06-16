
This repository contains code to convert data from the Gedcom 5.5.1 format to a simple CSV format, specifically in usage with Legacy Family Tree software, and to reconstruct the genealogies of specific individuals in said genealogy. More specifically, this code is developed to deal with the Genealogy Registry in the Genetic Biobank of the Faroe Islands (http://biobank.gov.fo/?lang=en).

# Installation / setup

To run this code there are some software requirements:

* Python 3.6
* Pandas 1.0.0
* ged4py 0.1.11

The recommended way of installing these is to first setup a conda environment using the `environment.yml` file in this repo:

```
conda env create -f environment.yml
```

# Usage

The following are the steps to use this code:

* Export data from Legacy to the Gedcom 5.5.1 format using UTF-8 encoding and the list of fields in the `export_list.gel` file
* Go to the directory where this code is stored
* Run the following commands:
    * `source setup.py`
    * `ged_cleanup.py [your GED file] [output GED file]`
    * `ged2csv.py [your (cleaned) GED file] [output CSV file]`
* The output of the last command is your genealogy in CSV format
* Find the RIN IDs of the individuals who's genealogy you want to reconstruct
* Run `python lineages.py [your CSV] [your individuals list] [output CSV file]`

To better understand the input to the various functions, see their documentation in the files themselves.


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

**TODO:** how to use this.

# Unit tests

Simple unit tests are implemented in `tests.py`, and test data is found in the `test_data` directory. To create a fictional family tree, the individuals were manually typed into Legacy, and exported to Gedcom 5.5.1 using UTF-8 encoding. The tests first convert the Gedcom data to CSV, then check that the records match the expected (which are manually typed into the `correct_results.csv` file), testing the functionality of the `csv2dict` function and the `Gen` class.



