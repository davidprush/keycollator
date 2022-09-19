#!venv/bin/ python3
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
import sys
import os.path
import string
import logging
import time
from collections import defaultdict
from nltk.stem import PorterStemmer
from fuzzywuzzy import fuzz
from constants import ProCons
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

    def stop_timerz(self, end_caller):
        if end_caller != self.__caller:
            self.__end_caller = end_caller
        self.__duration = self.__toc - self.__tic

    def echo_timerz(self):
        self.__formatted_duration = self.__toc - self.__tic
        print(f"Caller: {self.__caller} \
            Duration: {self.__formatted_duration:0.4f} seconds")

    def get_timerz_start(self):
        return self.__tic

    def get_timerz_stop(self):
        return self.__toc

    def get_timerz(self, console_output=False):
        self.__formatted_duration = self.__toc - self.__tic
        return f"Current Duration: \
                {self.__formatted_duration:0.4f} seconds"


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
        fuzzyness=99,
        set_logging=False
    ):
        self.timer = ProTimerz(sys._getframe().f_code.co_name)
        self.text_file = text_file
        self.key_file = key_file
        self.result_file = result_file
        self.log_file = log_file
        self.set_logging = set_logging
        self.valid_files = False
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
        self.__reset_logz()
        self.__itemize_text()
        self.__itemize_keys()
        self.__txt2key_matcher()
        self.__results2file()
        self.__spam_console()
        self.cool_stats()
        self.timer.stop_timerz(sys._getframe().f_code.co_name)

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
        text_data = open(self.text_file, 'r')
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
                    self.timer.get_timerz(),
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
                        self.timer.get_timerz(),
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
                        self.timer.get_timerz(),
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
        self.__result_items = temp_dict.copy()

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
                        self.timer.get_timerz(),
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
                        self.timer.get_timerz(),
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
                self.timer.get_timerz(),
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
            self.timer.get_timerz()
        ))

    def __verify_all_filez(self, *args):
        for arg in args:
            if not os.path.exists(arg):
                self.valid_files = False
            else:
                self.valid_files = True

    def __log_this(self, *args):
        if self.set_logging:
            self.__log_items += 1
            log_string = ""
            logging.basicConfig(
                filename=ProCons.LOGZ,
                filemode='a',
                format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                datefmt='%H:%M:%S',
                level=logging.DEBUG
            )
            if args:
                for arg in args:
                    log_string += str("[{}]".format(arg))
            logging.info(log_string)

    def __reset_logz(self):
        results_file = open(self.log_file, 'w')
        results_file.close()
