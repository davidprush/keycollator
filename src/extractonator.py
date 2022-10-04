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

import threading

from halo import Halo
from collections import defaultdict

import nltk.data

from extractfile import ItemizeFileData as ifd
from analysis import KeyTextAnalysis as kta

from consts import \
    LINE, STOP_WORDS, LOGTXT, TEXT, \
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
    __txtifd = ifd(TEXT, STOP_WORDS)
    __keyifd = ifd(KEY, STOP_WORDS)
    __csv = CSV
    __log = LOG
    __limres = limit_result
    __abrvt = abreviate
    __uplb = ubound
    __lolb = lbound
    __fuzrat = fuzz_ratio
    __vrbs = verbose
    __cmprsns = 0
    __lgcnt = 0
    __rcnt = 0
    __nrslt = True
    __logging = logging
    __logger = CustomLogger(
        phony="yes") if verbose else CustomLogger(
            phony="no")
    __sntdtctr = nltk.data.load(
        'tokenizers/punkt/english.pickle')

    Methods
    -------
    echo_result()
    echo_stats()
    results2file()
    get_key2text_matches()
    __purge_limits()
    __limresult()
    __vrbs()
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

        Class: KeyKrawler

        Method:__init__(
                        text_file=TEXT, key_file=KEY,
                        csv_file=CSV, log_file=LOG,
                        logging=False, fuzz_ratio=99,
                        limit_result=None, abreviate=32,
                        verbose=False, ubound_limit=None,
                        lbound_limit=None
                    ) -> obj

            └──inherited class:ItemizeFileData
                       obj = Itemizefile(
                                filename: str,
                                [stopwords]: list
                            ) -> obj

            └──inherited class:KeyTextAnalysis:
                        obj = ItemizeFile.KeyTextAnalysis(
                                [fuzz_ratio]: int, optional
                            ) -> obj

        ...

        Attributes
        ----------
        __txtifd = ifd(TEXT, STOP_WORDS)
        __keyifd = ifd(KEY, STOP_WORDS)
        __csv = CSV
        __log = LOG
        __limres = limit_result
        __abrvt = abreviate
        __uplb = ubound
        __lolb = lbound
        __fuzrat = fuzz_ratio
        __vrbs = verbose
        __cmprsns = 0
        __lgcnt = 0
        __rcnt = 0
        __nrslt = True
        __logging = logging
        __logger = CustomLogger(
            phony="yes") if verbose else CustomLogger(
                phony="no")
        __sntdtctr = nltk.data.load(
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
        self.__txtifd = ifd(TEXT, STOP_WORDS)
        self.__keyifd = ifd(KEY, STOP_WORDS)
        self.__reskta = kta(self.__txtifd.dict, self.__keyifd.dict, fuzz_ratio)
        self.__csv = CSV
        self.__log = LOG
        self.__limres = limit_result
        self.__abrvt = abreviate
        self.__uplb = ubound
        self.__lolb = lbound
        self.__fuzrat = fuzz_ratio
        self.__vrbs = verbose
        self.__cmprsns = 0
        self.__lgcnt = 0
        self.__rcnt = 0
        self.__nrslt = True
        self.__drlst = defaultdict(str)
        self.__pwd = os.getcwd()
        self.__pwdlst = [i for i in os.listdir()]
        # self.__logger = CustomLogger(
        #     phony="yes") if verbose else CustomLogger(
        #         phony="no")

    def filename_update(self):
        """
        Class: KeyKrawler Method: filename_update() -> None
        User prompt to update a one of the following 4 files:

            No.         File            Property (Vars)
            --          ----            ---------------
            1.          text            __txtifd.filename
            2.          key             __keyifd.filename
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
                        self.__txtifd.filename,
                        self.__keyifd.filename,
                        self.__csv,
                        self.__log_count)))
        f = 0
        for n, fname in enumerate(os.listdir()):
            fext = fname[len(fname) - 4]
            if fext == PFILE[fid]:
                f += 1
                self.__drlst[n] = fname
                print("{0}. {1}".format(f, fname))
        fnum = 0
        while fnum not in PFILE.keys():
            fnum = int(input("Enter file # from list: "))
            if fnum in self.__drlst and \
                    os.path.exists(self.__drlst[fnum]):
                if fid == 1:
                    print("Updated text file from {0} to {1}".format(
                        self.__txtifd.filename, self.__drlst[fnum]))
                    self.__txtifd.filename = self.__drlst[fnum]
                if fid == 2:
                    print("Updated key file from {0} to {1}".format(
                        self.__keyifd.filename, self.__drlst[fnum]))
                    self.__keyifd.filename = self.__drlst[fnum]
                if fid == 3:
                    print("Updated csv file from {0} to {1}".format(
                        self.__csv, self.__drlst[fnum]))
                    self.__csv = self.__drlst[fnum]
                if fid == 4:
                    print("Updated log file from {0} to {1}".format(
                        self.__log_count, self.__drlst[fnum]))
                    self.__log_count = self.__drlst[fnum]

    def echo_result(self) -> None:
        """
        Class: KeyKrawler Method: echo_result() -> None
        Print the results formatted in a table to the console
        ...
        """
        table_data = []
        self.__purge_limits()
        for i, item in enumerate([x for x in self.__reskta.key_matches]):
            item = LOGTXT['echo_result'].format(
                item[0:self.__abrvt]
                if len(item) > self.__abrvt
                else item)
            table_data.append([
                i,
                item,
                self.__reskta.key_matches
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
            ["Keys", self.__keyifd.unique_item_count],
            ["Text", self.__txtifd.unique_item_count],
            ["Matches", self.__reskta.total_matches],
            ["Comparisons", self.__reskta.total_comparisons]
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

    def get_key2text_matches(self) -> dict:
        """
        Class: KeyKrawler Method: get_key2text_matches() -> None
        Completes all necessary procedures to evaluate the text
        by finding key matches in the text

        ...

        Returns
        -------
        -> dict,
            where key:=[unique text/str]
            and item:=[ total number of matches found in text]
        """
        # spinner = Halo("Itemizing Text", spinner='dots')
        # spinner.start()
        self.__txtifd.thread.start()
        # spinner.stop_and_persist(SYMB['success'], LOGTXT['extract'].format(
        #     self.__key_file, self.__timer.timestampstr()))
        # spinner = Halo("Itemizing Keys", spinner='dots')
        # spinner.start()
        self.__keyifd.thread.start()
        # spinner.stop_and_persist(SYMB['success'], LOGTXT['extract'].format(
        #     self.__text_file, self.__timer.timestampstr()))
        # spinner = Halo("Itemizing Keys", spinner='dots')
        # spinner.start()

        self.__keyifd.echo_stopwords()
        input()

        self.__reskta = kta(
            self.__txtifd.dict,
            self.__keyifd.dict,
            STOP_WORDS,
            self.__fuzrat
        )
        if self.__reskta.run_match_analysis():
            if self.results2file():
                if self.__reskta.echo_matches():
                    return self.__reskta.key_matches
        # spinner.stop_and_persist(SYMB['success'], LOGTXT['extract'].format(
        #     self.__key_file, self.__timer.timestampstr()))
        return None

    def results2file(self) -> bool:
        """
        Class: KeyKrawler Method: results2file() -> bool
        Get KeyTextAnalysis results from __reskta.key_matches
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
            for item in self.__reskta.key_matches:
                write_count += 1
                csv_formatted_item = LOGTXT['csv_formatted_item'].format(
                    str(item), str(self.__reskta.key_matches), LINE)
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
        Class: KeyKrawler Method: __limresult() -> bool
        Remove items above the __limres
        ...

        Return
        ------
        -> bool, True if limit is set for items to be removed from result
        """
        if self.__limres is not None:
            for i, item in enumerate([x for x in self.__reskta.key_matches]):
                if i >= self.__limres:
                    del self.__reskta.key_matches[item]
            return True
        return False

    def __purge_limits(self) -> bool:
        """
        Class: KeyKrawler Method: __purge_limits() -> bool
        Remove items with total number of matches
        below the lower boundry and above upper-boundry

        ...

        Return
        ------
        -> bool, True if items were removed outside the limits set
        """
        if self.__lolb is not None \
                and self.__uplb is not None:
            for item in enumerate([x for x in self.__reskta.key_matches]):
                if (self.__reskta.key_matches[item] < self.__lolb) \
                    and (self.__reskta.key_matches[item]
                         > self.__uplb):
                    del self.__reskta.key_matches[item]
                    self.__rcnt -= 1
            return True
        return True

    # def __vrbs(self, *args) -> None:

    #     Class: KeyKrawler Method: __vrbs() -> None
    #     If _set_verbose:=True then increase output to console
    #     ...

    #     if self.__vrbs and args:
    #         print(self.__logger.write_log(
    #             [str(x) for x in args], phony="yes"
    #         ))

    def __verify_files(self, *args) -> bool:
        """
        Class: KeyKrawler Method: __verify_files(*args) -> bool
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
