# CLI

`keycollator` uses the **cli** to change default parameters and functions

```bash
usage: keycollator.py [-h] [-c CSV_FILE] [-d DICTIONARY_FILE] [-f COUNT] 
                      [-i IN_FILE] [-l] [-o OUT_FILE] [-v] [--version]

  App takes two files, a dictionary file and a and a text file, and counts 
  how many times each line in the dictionary file appears in the text file.
  The app can output the results to the console and/or csv/text file. 
  Matching will use fuzzy matching to get desired results.

optional arguments:
  -h, --help            show this help message and exit
  -c CSV_FILE, --csv-file CSV_FILE
                        Change the csv output file name (defautl is results.csv)
  -d DICTIONARY_FILE, --dictionary-file DICTIONARY_FILE
                        Change the dictionary file name (default is dictionary.txt)
  -f COUNT, --fuzzy COUNT
                        Select a value for fuzzyness 1-99, 1 for decresed accuracy, 99 for increased
                        accuracy, default is set to 95
  -i IN_FILE, --in-file IN_FILE
                        Change the input file name (default is text.txt)
  -l, --logging         Set flag to True for logging.
  -o OUT_FILE, --out-file OUT_FILE
                        Change the output file name (default is results.txt)
  -v, --verbose         Verbosity (-v, -vv, etc)
  --version             show version number and exit
```

## Applying fuzzy matching

For **fuzzy matching** use

```bash
keycollator --fuzzy-matching=[1-99]
```

## Setting the dictionary file (simple text file with items separated by line)

Set the **dictionary file**

```bash
keycollator -- /path/to/dictionary/directory/
```

## Create a log file

To create a **log file**, execute

```bash
keycollator -l /path/to/log_file/directory/
```

## Specify the CSV results file

Specify the results **csv file** name, execute

```bash
keycollator -c /path/to/results/file.csv
```

## Add verbosity (5 levels)

Specify verbosity using the following format:

```bash
keycollator -v [1-5]
```
