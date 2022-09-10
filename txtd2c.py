#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module txtd2c.py Documentation.

This app takes a dictionary file containing words or phrases and
and compares it to a text file, then outputs a file listing the total
number of appearances for each word/phrase from the dictionary.

Example:

        $ python txtd2c.py

        *Notes

Attributes:


Todo:
    * Fix command line args
    * Add progress/status bars when populating text data
    * Add progress/status bars when populating dictionary data
    * Add progress/status bars when comparing dictionary to text
    * Migrate text file dictionary extraction to function
    * Migrate dictionary file extraction to function
    * Migrate comparison process to function
    * Consider adding classes

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""
from collections import defaultdict
from nltk.stem import PorterStemmer
from time import sleep
# from nltk.tokenize import word_tokenize
from fuzzywuzzy import fuzz
# import pandas as pd
import string
import argparse
import progressbar
import verboselogs
import logging
import sys
import os.path

__author__ = "David Rush"
__copyright__ = "Copyright 2022, Rush Solutions, LLC"
__credits__ = ["David Rush", "", "", ""]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "David Rush"
__email__ = "david@rushsoutions.net"
__status__ = "Prototype"
"""__status__ Common Usage:
    "Prototype", "Development", or "Production"
"""

APP_NAME = "txtd2c.py"
END_LINE = "\n"
RESULTS_HDR = \
    "**************************** Results ******************************"
RESULTS_HDR_TXT = \
    "The following is a list of dcitionary items found in the text file:"
RESULTS_FTR = \
    "**************************** End Results **************************"


# Start building class for handling file information
# Add atributes for file data (dict), Number of unique items,
#   source file name, sorted flag
# Add methods for populating and sorting
class MySourceFile:

    def __init__(self, name, file='None'):
        self.name = name
        # move to conditional below self.file = file
        self.data = defaultdict(int)
        self.unique_items = 0
        self.total_source_items = 0
        self.sort_status = False
        self.file_verifed = False
        '''
         Add test for file exist <Move to private method>
        if file == None:
            # INSERT error/warning
            return
        self.file = file
        if os.path.isfile(file):
            try:
                self.data = open(file,'r')
            except IOError:
                sys.stderr.write('Problem opening file %s\n' % file)
                return
            self.file = file
            f.close()
        else:
            self.data []
            '''

    def __sort_data(self):
        self.data = dict(sorted(
            self.data.items(), key=lambda item: item[1], reverse=True))
        self.sort_status = True

    def __populate_data(self):
        if self.file_verified:
            ps = PorterStemmer()
            self.data = open(self.source_file, 'r')
            item_freq = defaultdict(int)
            self.total_source_items = 0
            self.unique_items = 0
            for item in self.data:
                item = item.translate(
                    item.maketrans("", "", string.punctuation))
                item = item.lower()
                item = item.rstrip(END_LINE)
                self.total_source_items += 1
                if ps.stem(item) not in item_freq:
                    item_freq[item] = 0
                    self.unique_items += 1

    def __verify_file_exists(self):
        self.file_verified = os.path.exists(self.source_file)

    def search(self, pattern):
        srch = re.compile(pattern,re.I)
        found = []
        for item in self.db:
            if srch.search(item.name):
                found.append(item)
        return found

    def print_stats(self): # Placeholder for thoughts
        print(self.unique_items)
        print(self.total_source_items)
        print(self.file_verified)
        # etc...


'''
Create a class for results and file output
'''


def close_items(*args):
    for arg in args:
        arg.close()


def output_console_file(*args):
    output_text = ''.join(map(str, args))
    print(output_text)
    output_text += END_LINE
    results_file.write(output_text)


def parse_args():
    parser = argparse.ArgumentParser(
        prog=APP_NAME,
        description='''
            App takes two files, a dictionary file and a
              and a text file, and counts how many times
              each line in the dictionary file appears in
              the text file. The app can output the results
              to the console and/or csv/text file. Matching
              will use fuzzy matching to get desired results.''',
        epilog='''
            End of help.''')

    parser.add_argument(
        "-c",
        "--csv-file",
        action="store",
        dest="csv_file",
        default="results.csv",
        help='''
        Change the csv output file name (defautl is results.csv)''')

    parser.add_argument(
        "-d",
        "--dictionary-file",
        action="store",
        dest="dictionary_file",
        default="dictionary.txt",
        help='''
        Change the dictionary file name (default is dictionary.txt)''')

    parser.add_argument(
        "-f",
        "--fuzzy",
        action="store",
        dest="count",
        default=95,
        help='''
        Select a value for fuzzyness 1-99, 1 for decresed accuracy,
          99 for increased accuracy, default is set to 95''')

    parser.add_argument(
        "-i",
        "--in-file",
        action="store",
        dest="in_file",
        default="text.txt",
        help='''
        Change the input file name (default is text.txt)''')

    parser.add_argument(
        "-l",
        "--logging",
        action="store_true",
        help='''
        Set flag to True for logging.''')

    parser.add_argument(
        "-o",
        "--out-file",
        action="store",
        dest="out_file",
        default="results.txt",
        help='''
        Change the output file name (default is results.txt)''')

    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbosity",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    return args


def main():
    cargs = parse_args()

    logger = verboselogs.VerboseLogger('demo')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)

    if cargs.verbosity >= 4:
        logger.setLevel(logging.SPAM)
    elif cargs.verbosity >= 3:
        logger.setLevel(logging.DEBUG)
    elif cargs.verbosity >= 2:
        logger.setLevel(logging.VERBOSE)
    elif cargs.verbosity >= 1:
        logger.setLevel(logging.NOTICE)
    elif cargs.verbosity < 0:
        logger.setLevel(logging.WARNING)

    # Example logger usage
    logger.SPAM("This message will show most frequently")
    logger.DEBUG("This will be a level 3 for verbosity")
    logger.VERBOSE("This will be a level 2, a somewhat verbose situation")
    logger.NOTICE("Sparingly used to notify the user of something")
    logger.WARNING("The rarest of messages, reserved for errors")

    text_file_items = open(cargs.in_file, 'r')
    dict_file_items = open(cargs.dictionary_file, 'r')
    log_file = open("log_file.txt", 'w')
    results_file = open(cargs.out_file, 'w')

    word_freq = defaultdict(int)
    text_dict = defaultdict(int)

    ps = PorterStemmer()

    dict_item_count = 0
    for item in dict_file_items:
        item = item.translate(item.maketrans("", "", string.punctuation))
        item = item.lower()
        item = item.rstrip(END_LINE)
        if ps.stem(item) not in word_freq:
            word_freq[item] = 0
            dict_item_count += 1
            log_string = "Added " \
                + str(dict_item_count) + "." + item + " to dictionary list"
            logger.info(log_string)
            log_string = log_string + END_LINE
            log_file.write(str(str(log_string) + END_LINE))

    text_item_count = 0
    for text_item in text_file_items:
        text_item = text_item. \
            translate(text_item.maketrans("", "", string.punctuation))
        text_item = text_item.lower()
        log_file.write(str(str(log_string) + END_LINE))
        text_dict[text_item] = 0
        text_item_count += 1
        log_string = "Added " \
            + str(text_item_count) + "." + text_item + " to text list"
        logger.info(log_string)
        log_file.write(str(str(log_string) + END_LINE))

    item_compare_count = 0
    word_freq_key_count = 0
    for key in word_freq:
        word_freq_key_count += 1
        for text in text_dict:
            item_compare_count += 1
            log_string = str(word_freq_key_count), \
                "Comparison:", key, str(item_compare_count), ":", text
            logger.info(log_string)
            log_file.write(str(str(log_string) + END_LINE))
            if ps.stem(key) in ps.stem(text):
                word_freq[key] += 1
                log_string = key + " found in " + text
                log_file.write(str(str(log_string) + END_LINE))
            elif fuzz.partial_ratio(key, text) >= 95:
                word_freq[key] += 1
                log_string = key + " fuzzy matched with " + text
                logger.info(log_string)
                log_file.write(str(str(log_string) + END_LINE))

 #   word_freq = sort_dictionary(word_freq)

    output_console_file(RESULTS_HDR)
    output_console_file(RESULTS_HDR_TXT)

    item_num = 0
    for key in word_freq:
        if word_freq[key] > 10:
            item_num += 1
            output_console_file(item_num, ". ", key, ",", word_freq[key])

    output_console_file(RESULTS_FTR)

    output_console_file(
        "Stats for this run...", END_LINE,
        "Total Dictionary Items: ", dict_item_count, END_LINE,
        "Total Text File Items: ", text_item_count, END_LINE,
        "Total Keys Added to List: ", word_freq_key_count, END_LINE,
        "Total Comparisons: ", item_compare_count, END_LINE,
        END_LINE)

    close_items(
        text_file_items,
        dict_file_items,
        log_file,
        results_file)


if __name__ == '__main__':
    main()
