#!/venv/bin/ python3
# -*- coding: utf-8 -*-
"""
┌─┐─┐ ┬┌┬┐┬─┐┌─┐┌─┐┌┬┐┌─┐┌┐┌┌─┐┌┬┐┌─┐┬─┐
├┤ ┌┴┬┘ │ ├┬┘├─┤│   │ │ ││││├─┤ │ │ │├┬┘
└─┘┴ └─ ┴ ┴└─┴ ┴└─┘ ┴ └─┘┘└┘┴ ┴ ┴ └─┘┴└─
Module filework.py documentation

 #     # ### #######    #       ###  #####  ####### #     #  #####  #######
 ##   ##  #     #       #        #  #     # #       ##    # #     # #
 # # # #  #     #       #        #  #       #       # #   # #       #
 #  #  #  #     #       #        #  #       #####   #  #  #  #####  #####
 #     #  #     #       #        #  #       #       #   # #       # #
 #     #  #     #       #        #  #     # #       #    ## #     # #
 #     # ###    #       ####### ###  #####  ####### #     #  #####  #######

[[Copyright (c) 2022 David P. Rush]]Permission is hereby granted, free of charge, to
any person obtaining a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished to
do so, subject to the following conditions: The above copyright notice and this
permission notice shall be included in all copies or substantial portions of the
Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR
A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Example:

    -

Contains two classes:

    1. ProTimerz
        -
    2. KeyKrawler
        -

Notes:

    -

Todo:

    *

"""
import os.path
import string
import logging
import time
from collections import defaultdict
from nltk.stem import PorterStemmer
from fuzzywuzzy import fuzz
from constants import ProCons
# import sys
# import progressbar
# import verboselogs
# import pandas as pd
# from nltk.tokenize import word_tokenize


class ProTimerz:
    def __init__(
        self,
        caller=""
    ):
        self.__tic = time.perf_counter()
        self.__caller = caller
        self.__end_caller = caller
        self.__toc = self.__tic
        self.__duration = time.perf_counter()
        self.__formatted_duration = str(self.__duration)

    def stop_timer(self, end_caller):
        if end_caller != self.caller:
            self.__end_caller = end_caller
        self.__duration = self.__toc - self.tic

    def get_duration(self, console_output=False, verbose=False):
        if console_output or verbose:
            print(f"Caller: {self.caller} \
                Duration: {self.__formatted_duration:0.4f} seconds")
        return self.__duration

    def get_start(self):
        return self.__tic

    def get_stop(self):
        return self.__toc

    def get_current_time(self, console_output=False):
        if console_output:
            print(f"Current Duration: \
                {self.__formatted_duration:0.4f} seconds")
        return (self.__toc - self.__tic)


class KeyKrawler:
    def __init__(
        self,
        text_file=ProCons.TXTS,
        key_file=ProCons.KEYZ,
        result_file=ProCons.REZF,
        log_file=ProCons.LOGZ,
        verbosity=0,
        ubound=99999,
        lbound=0,
        fuzzyness=99
    ):
        self.timer = ProTimerz("filework.py::__init__")
        self.text_file = text_file
        self.key_file = key_file
        self.result_file = result_file
        self.log_file = log_file
        self.text_file_exists = False
        self.key_file_exists = False
        self.result_file_exists = False
        self.log_file_exists = False
        self.__key_freq = defaultdict(int)
        self.__text_freq = defaultdict(int)
        self.__result_items = defaultdict(int)
        self.__ubound = ubound
        self.__lbound = lbound
        self.__fuzzyness = fuzzyness
        self.__verbosity = verbosity
        self.__text_items = 0
        self.__key_items = 0
        self.__key_matches = 0
        self.__no_matches = False
        self.__total_comparisons = 0
        self.__log_items = 0
        self.__match_items = 0
        self.__ps = PorterStemmer()
        self.__freq = 0
        self.__itemize_text()
        self.__itemize_keys()
        self.__txt2key_matcher()
        self.__results2file()
        self.__spam_console()
        self.cool_stats()
        self.timer.stop_timer("filework.py::write_results()")

    def __iter__(self):
        self.__freq = 0
        return self

    def __next__(self):
        if self.__freq <= self.max:
            result = 2 ** self.n
            self.n += 1
            return result
        else:
            raise StopIteration

    def __itemize_text(self):
        text_data = open(ProCons.TXTS, 'r')
        self.__text_items = 0
        for text in text_data:
            text = text. \
                translate(text.maketrans("", "", string.punctuation))
            text = text.lower()
            self.__text_freq[text] = 0
            self.__text_items += 1
            self.__log_this(
                "Added ",
                self.__text_items,
                "::",
                text,
                ">>> to text list"
            )
        text_data.close()

    def __itemize_keys(self):
        key_data = open(self.key_file, 'r')
        self.__key_items = 0
        for key in key_data:
            # Sanitize the keys
            key = key.translate(key.maketrans("", "", string.punctuation))
            key = key.lower()
            key = key.rstrip(ProCons.END_LINE)
            # Verify key is not in dictionary before adding it
            if self.__ps.stem(key) not in self.__key_freq:
                # Initialize the key in dictionary
                self.__key_freq[key] = 0
                self.__key_items += 1
                self.__log_this(
                    "Added ",
                    self.__key_items,
                    "::",
                    key,
                    ">>> to key list"
                )
        key_data.close()

    def __txt2key_matcher(self):
        self.__total_comparisons = 0
        self.__key_items = 0
        temp_dict = defaultdict(int)
        for key in self.__key_freq:
            self.__key_items += 1
            for item in self.__text_freq:
                self.__total_comparisons += 1
                self.__log_this(
                    self.timer.get_current_time(),
                    self.__key_items,
                    "::",
                    key,
                    self.__total_comparisons,
                    ":text=",
                    item
                )
                # Check for near-perfect match
                if self.__ps.stem(key) in self.__ps.stem(item):
                    temp_dict[key] += 1
                    self.__key_items += 1
                    self.__log_this(
                        self.timer.get_current_time(),
                        key,
                        "#{self.__key_items}#",
                        "<<<Found in>>>",
                        item,
                        "{item}comparison#[",
                        self.__total_comparisons,
                        "]::",
                        self.__text_freq[item]
                    )
                # Only perform fuzzy matching if imperfect match
                elif fuzz.partial_ratio(key, item) >= self.__fuzzyness:
                    temp_dict[key] += 1
                    self.__key_items += 1
                    self.__log_this(
                        self.timer.get_current_time(),
                        key,
                        "#{self.__key_items}#",
                        "<<<FUZZY-MATCHED \
                        ({self.__fuzzyness})>>>",
                        item,
                        "{item}comparison#[",
                        self.__total_comparisons,
                        "]::",
                        self.__text_freq[item]
                    )
        if temp_dict:
            self.__result_items.clear()
            self.__result_items = temp_dict.copy()
        else:
            self.__no_matches = True

    def __results2file(self):
        if not self.__no_matches:
            results_file = open(self.result_file, 'w')
            write_count = 0
            for key in self.__key_freq:
                if self.__key_freq[key] > self.__lbound \
                        and self.key_freq[key] < self.__ubound:
                    write_count += 1
                    results_file.write(
                        write_count,
                        ". ",
                        key,
                        ",",
                        self.__result_items[key]
                    )
                    self.__log_this(
                        self.timer.get_current_time(),
                        write_count,
                        "::",
                        key,
                        ":",
                        self.__key_freq[key]
                    )
            results_file.close()
            self.__match_items = write_count
        else:
            return False

    def __spam_console(self):
        if not self.__no_matches:
            print_item = 0
            print(ProCons.RESULTS_HDR)
            print(ProCons.RESULTS_HDR_TXT)
            for key in self.__key_freq:
                if self.__key_freq[key] > self.__lbound \
                        and self.key_freq[key] < self.__ubound:
                    print_item += 1
                    print(
                        "\t\t[",
                        print_item,
                        "]. ",
                        key,
                        "\t\t",
                        self.__key_freq[key])
                    self.__log_this(
                        self.timer.get_current_time(),
                        "\t\t[",
                        print_item,
                        "]. ",
                        key,
                        "\t\t",
                        self.__key_freq[key]
                    )
            print(ProCons.RESULTS_FTR)
        else:
            print(ProCons.NO_MATCHES)
            self.__log_this(
                self.timer.get_current_time(),
                ProCons.NO_MATCHES
            )

    def cool_stats(self):
        print(ProCons.DIV_LINE)
        print(ProCons.RESULTS_FTR)
        print(ProCons.STATISTICS.format(
            self.__key_items,
            self.__text_items,
            self.__match_items,
            self.__total_comparisons,
            self.__duration
        ))

    def __verboze(self):
        pass

    def __verify_all_filez(self):
        self.text_file_exists = os.path.exists(self.text_file)
        self.key_file_exists = os.path.exists(self.key_file)
        self.result_file_exists = os.path.exists(self.result_file)
        self.log_file_exists = os.path.exists(self.log_file)
        if self.text_file_exists and self.key_file_exists and \
                self.result_file_exists and os.path.exists(self.log_file) \
                and self.__verbosity > 0:
            print("All files are valid")
        elif not self.text_file_exists:
            print("WARNING!::The file ", self.text_file, " is not valid.")
            self.__log_this(
                "WARNING!::The file ",
                self.text_file,
                " is not valid."
            )
        elif not self.key_file_exists:
            print("The file ", self.key_file, " is not valid.")
            self.__log_this(
                "WARNING!::The file ",
                self.text_file,
                " is not valid."
            )
        elif not self.result_file_exists:
            print("The file ", self.result_file, " is not valid.")
            self.__log_this(
                "WARNING!::The file ",
                self.result_file,
                " is not valid."
            )
        elif not self.log_file_exists:
            print("The file ", self.log_file, " is not valid.")
            self.__log_this(
                "WARNING!::The file ",
                self.log_file,
                " is not valid."
            )
        return True

    def __log_this(self, *args):
        # log_file = open(ProCons.LOGZ, 'w')
        self.__log_items += 1
        log_string = ""
        logging.basicConfig(
            filename=ProCons.LOGZ,
            filemode='a',
            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
            datefmt='%H:%M:%S',
            level=logging.DEBUG
        )
        logging.info("Running Urban Planning")
        logger = logging.getLogger('urbanGUI')
        logger.setLevel(logging.INFO)
        if self.__verbosity >= 4:
            logger.setLevel(logging.SPAM)
            # logger.SPAM("This message will show most frequently")
        elif self.__verbosity >= 3:
            logger.setLevel(logging.DEBUG)
            # logger.DEBUG("This will be a level 3 for verbosity")
        elif self.__verbosity >= 2:
            logger.setLevel(logging.VERBOSE)
            # logger.VERBOSE("This will be a level 2, \
            # a somewhat verbose situation")
        elif self.__verbosity >= 1:
            logger.setLevel(logging.NOTICE)
            # logger.NOTICE("Sparingly used to notify the user of something")
        elif self.__verbosity < 0:
            logger.setLevel(logging.WARNING)
            # logger.WARNING("The rarest of messages, reserved for errors")
        if args:
            for arg in args:
                log_string += str(arg)
