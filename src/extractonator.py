# -*- coding: utf-8 -*-
"""
┌─┐─┐ ┬┌┬┐┬─┐┌─┐┌─┐┌┬┐┌─┐┌┐┌┌─┐┌┬┐┌─┐┬─┐
├┤ ┌┴┬┘ │ ├┬┘├─┤│   │ │ ││││├─┤ │ │ │├┬┘
└─┘┴ └─ ┴ ┴└─┴ ┴└─┘ ┴ └─┘┘└┘┴ ┴ ┴ └─┘┴└─

Copyright (C) 2022 Rush Solutions, LLC
Author: David Rush <davidprush@gmail.com>
License: MIT
Contains:

    obj = KeyKrawler(text_file=TEXT, key_file=KEY, csv_file=CSV,
                    limit_result=None, abrev_items=32, log_file=LOG,
                    verbose=False, ubound_limit=None, lbound_limit=None,
                    fuzzy_match=99, logging=False, run_now=False) -> obj
        imports
            └──class:ItemizeFileData:
                   obj = Itemizefile(filename: str, [stopwords]: list,
                                    [logfile]: str, [verbose]: bool,
                                    [fuzzy_matching]: int) -> obj
        imports
            └──class:KeyTextAnalysis:
                    obj = ItemizeFile.TextAnalysis(
                            [fuzzy_matching]: int,
                            optional) -> obj

Todo:
    ✖ Refactor code and remove redunancies
    ✖ Fix pylint errors
    ✖ Add proper error handling
"""
import os.path
import termtables as tt

from halo import Halo
from collections import defaultdict

import nltk.data

from extractfile import ItemizedFileData as ifd
from analysis import KeyTextAnalysis as kta

from consts import \
    LINE, STOP_WORDS, SYMB, LOGTXT, TEXT, \
    KEY, CSV, LOG, RTBLHDR, STBLHDR, PFILE


class KeyKrawler:
    """
    Class: KeyKrawler

    obj = KeyKrawler(text_file=TEXT, key_file=KEY, csv_file=CSV,
                    limit_result=None, abreviate=32, log_file=LOG,
                    verbose=False, ubound_limit=None, lbound_limit=None,
                    fuzzy_match=99, logging=False, run_now=False) -> obj

    └──subclass:ItemizeFile:
           obj = Itemizefile(filename: str, [stopwords]: list,
                            [logfile]: str, [verbose]: bool,
                            [fuzz_ratio]: int) -> obj

    └──subclass:ItemizeFile.KeyTextAnalysis:
            obj = ItemizeFile.KeyTextAnalysis([fuzz_ratio]: int, optional) -> obj

    ...

    Attributes
    ----------
    __textobj = ifd(TEXT, STOP_WORDS)
    __keyobj = ifd(KEY, STOP_WORDS)
    __csv = CSV
    __log = LOG
    __limit_result = limit_result
    __abreviate = abreviate
    __ulbound = ubound
    __llbound = lbound
    __fuzz_ratio = fuzz_ratio
    __verbose = verbose
    __comparisons = 0
    __logct = 0
    __rct = 0
    __noresult = True
    __logging = logging
    __logger = CustomLogger(
        phony="yes") if verbose else CustomLogger(
            phony="no")
    __sent_detector = nltk.data.load(
        'tokenizers/punkt/english.pickle')

    Methods
    -------
    echo_result()
    echo_stats()
    set_result2file()
    match_keys()
    __purge_limits()
    __limresult()
    __verbose()
    __verify_files()

    Parameters
    ----------
    text_file=TEXT,
    key_file=KEY,
    csv_file=CSV,
    log_file=LOG,
    logging=False,
    fuzz_ratio=99,
    limit_result=None,
    abreviate=32,
    verbose=False,
    lbound=None,
    ubound=None
    """

    def __init__(
        self,
        text_file=TEXT,
        key_file=KEY,
        csv_file=CSV,
        log_file=LOG,
        logging=False,
        fuzz_ratio=99,
        limit_result=None,
        abreviate=32,
        verbose=False,
        lbound=None,
        ubound=None
    ) -> None:
        """
        Class: KeyKrawler Method:
            __init__(text_file=TEXT, key_file=KEY,
                csv_file=CSV, log_file=LOG, logging=False,
                fuzz_ratio=99, limit_result=None, abreviate=32,
                verbose=False, ubound_limit=None, lbound_limit=None) -> obj

        └──subclass:ItemizedFileData
               obj = Itemizefile(filename: str, [stopwords]: list) -> obj

        └──subclass:ItemizeFile.KeyTextAnalysis:
                obj = ItemizeFile.KeyTextAnalysis([fuzz_ratio]: int, optional) -> obj

        ...

        Attributes
        ----------
        __textobj = ifd(TEXT, STOP_WORDS)
        __keyobj = ifd(KEY, STOP_WORDS)
        __csv = CSV
        __log = LOG
        __limit_result = limit_result
        __abreviate = abreviate
        __ulbound = ubound
        __llbound = lbound
        __fuzz_ratio = fuzz_ratio
        __verbose = verbose
        __comparisons = 0
        __logct = 0
        __rct = 0
        __noresult = True
        __logging = logging
        __logger = CustomLogger(
            phony="yes") if verbose else CustomLogger(
                phony="no")
        __sent_detector = nltk.data.load(
            'tokenizers/punkt/english.pickle')

        Parameters
        ----------
        text_file=TEXT,
        key_file=KEY,
        csv_file=CSV,
        log_file=LOG,
        logging=False,
        fuzz_ratio=99,
        limit_result=None,
        abreviate=32,
        verbose=False,
        lbound=None,
        ubound=None
        """
        self.__textobj = ifd(TEXT, STOP_WORDS)
        self.__keyobj = ifd(KEY, STOP_WORDS)
        self.__csv = CSV
        self.__log = LOG
        self.__resobj = None
        self.__limit_result = limit_result
        self.__abreviate = abreviate
        self.__ulbound = ubound
        self.__llbound = lbound
        self.__fuzz_ratio = fuzz_ratio
        self.__verbose = verbose
        self.__comparisons = 0
        self.__logct = 0
        self.__rct = 0
        self.__noresult = True
        self.__dirlist = defaultdict(str)
        self.__pwd_list = [i for i in os.listdir()]
        self.__pwd = os.getcwd()
        # self.__logger = CustomLogger(
        #     phony="yes") if verbose else CustomLogger(
        #         phony="no")
        self.__sent_detector = nltk.data.load(
            'tokenizers/punkt/english.pickle')

    def filename_update(self):
        """
        Class: KeyKrawler Method: filename_update() -> None
        User prompt to update a one of the following 4 files:

            No.         File            Property (Vars)
            --          ----            ---------------
            1.          text            __textobj.filename
            2.          key             __keyobj.filename
            3.          csv             __csv
            4.          log             __log

        *starts in current working directory

        ...
        """
        fid = 0
        print("Current directory: {0}".format(os.getcwd()))
        while fid not in PFILE.keys():
            fcat = int(
                input(
                    "Enter the # of the file name to update... \n \
                    1. Text: {0} \n \
                    2. Key: {1} \n \
                    3. CSV: {2} \n \
                    4. log: {3} \n".format(
                        self.__textobj.filename,
                        self.__keyobj.filename,
                        self.__csv,
                        self.__log_count)))
        f = 0
        for n, fname in enumerate(os.listdir()):
            fext = fname[len(fname) - 4]
            if fext == PFILE[fid]:
                f += 1
                self.__dirlist[n] = fname
                print("{0}. {1}".format(f, fname))
        fnum = 0
        while fnum not in PFILE.keys():
            fnum = int(input("Enter file # from list: "))
            if fnum in self.__dirlist and \
                    os.path.exists(self.__dirlist[fnum]):
                if fid == 1:
                    print("Updated text file from {0} to {1}".format(
                        self.__textobj.filename, self.__dirlist[fnum]))
                    self.__textobj.filename = self.__dirlist[fnum]
                if fid == 2:
                    print("Updated key file from {0} to {1}".format(
                        self.__keyobj.filename, self.__dirlist[fnum]))
                    self.__keyobj.filename = self.__dirlist[fnum]
                if fid == 3:
                    print("Updated csv file from {0} to {1}".format(
                        self.__csv, self.__dirlist[fnum]))
                    self.__csv = self.__dirlist[fnum]
                if fid == 4:
                    print("Updated log file from {0} to {1}".format(
                        self.__log_count, self.__dirlist[fnum]))
                    self.__log_count = self.__dirlist[fnum]

    def echo_result(self) -> None:
        """
        Class: KeyKrawler Method: echo_result() -> None
        Print the results formatted in a table to the console
        ...
        """
        table_data = []
        self.__purge_limits()
        for i, item in enumerate([x for x in self.__resobj.key_matches]):
            item = LOGTXT['echo_result'].format(
                item[0:self.__abreviate]
                if len(item) > self.__abreviate
                else item)
            table_data.append([
                i,
                item,
                self.__resobj.key_matches
            ])
        tt.print(
            table_data,
            header=RTBLHDR,
            style=tt.styles.rounded,
            padding=(0, 0),
            alignment="clc"
        )

    def echo_stats(self) -> None:
        """
        Class: KeyKrawler echo_stats() -> None
        Prints analysis totals in a table to the console
        ...
        """
        table_data = [
            ["Keys", self.__keyobj.unique_item_count],
            ["Text", self.__textobj.unique_item_count],
            ["Matches", self.__resobj.total_matches],
            ["Comparisons", self.__resobj.total_comparisons]
            # ["Logs", self.__logger.log_count]
            # ["Runtime", self.__timer.timestamp(True)]
        ]
        tt.print(
            table_data,
            header=STBLHDR,
            style=tt.styles.rounded,
            padding=(0, 0),
            alignment="lc"
        )

    def match_keys(self) -> None:
        """
        Class: KeyKrawler method: match_keys() -> None
        Completes all necessary procedures to evaluate the text
        ...
        """
        # spinner = Halo("Itemizing Text", spinner='dots')
        # spinner.start()

        self.__textobj.itemize_file()

        # spinner.stop_and_persist(SYMB['success'], LOGTXT['extract'].format(
        #     self.__key_file, self.__timer.timestampstr()))

        # spinner = Halo("Itemizing Keys", spinner='dots')
        # spinner.start()

        self.__keyobj.itemize_file()

        # spinner.stop_and_persist(SYMB['success'], LOGTXT['extract'].format(
        #     self.__text_file, self.__timer.timestampstr()))

        # spinner = Halo("Itemizing Keys", spinner='dots')
        # spinner.start()

        self.__resobj = kta(
            self.__textobj.dict,
            self.__keyobj.dict,
            self.__fuzz_ratio
        )

        self.__resobj.eval_keys2text()
        self.__resobj.echo_key_matches()

        # spinner.stop_and_persist(SYMB['success'], LOGTXT['extract'].format(
        #     self.__key_file, self.__timer.timestampstr()))

        self.echo_result()
        self.echo_stats()
        self.set_result2file()

    def set_result2file(self) -> bool:
        """
        Class: KeyKrawler method set_result2file() -> bool
        Get KeyTextAnalysis results from __resobj.key_matches
        and formats to write it to CSV file (__csv)
        ...
        """
        with open(self.__csv, 'w') as fh:
            write_count = 0
            # spinner = Halo(
            #     text=LOGTXT['write_results2file'].format(
            #         self.__csv),
            #     spinner='dots'
            # )
            # spinner.start()
            self.__purge_limits()
            for item in self.__resobj.key_matches:
                write_count += 1
                csv_formatted_item = LOGTXT['csv_formatted_item'].format(
                    str(item), str(self.__resobj.key_matches), LINE)
                fh.write(csv_formatted_item)
            fh.close()
            # spinner.stop_and_persist(
            #     SYMB['success'],
            #     "{0} Complete.[{1}]".format(
            #         self.__csv,
            #         self.__timer.timestampstr()
            #     )
            # )
            return True
        return False

    def __limresult(self) -> bool:
        """
        Class: KeyKrawler method __limresult() -> bool
        Remove items above the __limit_result
        ...

        Return
        ------
        -> bool, True if limit is set for items to be removed from result
        """
        if self.__limit_result is not None:
            for i, item in enumerate([x for x in self.__resobj.key_matches]):
                if i >= self.__limit_result:
                    del self.__resobj.key_matches[item]
            return True
        return False

    def __purge_limits(self) -> bool:
        """
        Class: KeyKrawler method __purge_limits() -> bool
        Remove items with total number of matches
        below the lower boundry and above upper-boundry
        ...

        Return
        ------
        -> bool, True if items were removed outside the limits set
        """
        if self.__llbound is not None \
                and self.__ulbound is not None:
            for item in enumerate([x for x in self.__resobj.key_matches]):
                if (self.__resobj.key_matches[item] < self.__llbound) \
                    and (self.__resobj.key_matches[item]
                         > self.__ulbound):
                    del self.__resobj.key_matches[item]
                    self.__rct -= 1
            return True
        return True

    # def __verbose(self, *args) -> None:
        
    #     Class: KeyKrawler method __verbose() -> None
    #     If _set_verbose:=True then increase output to console
    #     ...
        
    #     if self.__verbose and args:
    #         print(self.__logger.write_log(
    #             [str(x) for x in args], phony="yes"
    #         ))

    def __verify_files(self, *args) -> bool:
        """
        Class: KeyKrawler method: __verify_files(*args) -> bool
        Verifies all file names (str) passed as args are valid
        ...

        Returns
        -------
        -> bool, True if ALL str *args are valid files
        """
        self.__valid_files = True
        for arg in args:
            if isinstance(arg, str):
                if not os.path.exists(arg):
                    print("{0} is not a valid file!".format(arg))
                    self.__valid_files = False
        return self.__valid_files
