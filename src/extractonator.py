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
from threadanalysis import KeyTextAnalysis as kta

from consts import \
    LINE, STOP_WORDS, LOGTXT, TEXT, \
    KEY, CSV, LOG, RTBLHDR, STBLHDR, PFILE

__author__ = "David Rush"
__copyright__ = "Copyright 2022, Rush Solutions, LLC"
__credits__ = ["David Rush", "...", "...", "..."]
__license__ = "MIT"
__version__ = "0.0.5"
__maintainer__ = "David Rush"
__email__ = "davidprush@gmail.com"
__status__ = "Development"


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
    _txtifd = ifd(TEXT, STOP_WORDS)
    _keyifd = ifd(KEY, STOP_WORDS)
    _csv = CSV
    _log = LOG
    _limres = limit_result
    _abrvt = abreviate
    _uplb = ubound
    _lolb = lbound
    _fuzrat = fuzz_ratio
    _vrbs = verbose
    _cmprsns = 0
    _lgcnt = 0
    _rcnt = 0
    _nrslt = True
    _logging = logging
    _logger = CustomLogger(
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
    _purge_limits()
    _limresult()
    _vrbs()
    _verify_files()

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
        _txtifd = ifd(TEXT, STOP_WORDS)
        _keyifd = ifd(KEY, STOP_WORDS)
        _csv = CSV
        _log = LOG
        _limres = limit_result
        _abrvt = abreviate
        _uplb = ubound
        _lolb = lbound
        _fuzrat = fuzz_ratio
        _vrbs = verbose
        _cmprsns = 0
        _lgcnt = 0
        _rcnt = 0
        _nrslt = True
        _logging = logging
        _logger = CustomLogger(
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
        self._txtifd = ifd(TEXT, STOP_WORDS)
        self._keyifd = ifd(KEY, STOP_WORDS)
        self._reskta = kta(self._txtifd.dict, self._keyifd.dict, fuzz_ratio)
        self._csv = CSV
        self._log = LOG
        self._limres = limit_result
        self._abrvt = abreviate
        self._uplb = ubound
        self._lolb = lbound
        self._fuzrat = fuzz_ratio
        self._vrbs = verbose
        self._cmprsns = 0
        self._lgcnt = 0
        self._rcnt = 0
        self._nrslt = True
        self._drlst = defaultdict(str)
        self._pwd = os.getcwd()
        self._pwdlst = [i for i in os.listdir()]
        # self._logger = CustomLogger(
        #     phony="yes") if verbose else CustomLogger(
        #         phony="no")

    def filename_update(self):
        """
        (Class:KeyKrawler) => Method: filename_update() -> None
        User prompt to update a one of the following 4 files:

            No.         File            Property (Vars)
            --          ----            ---------------
            1.          text            _txtifd.filename
            2.          key             _keyifd.filename
            3.          csv             _csv
            4.          log             _log

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
                        self._txtifd.filename,
                        self._keyifd.filename,
                        self._csv,
                        self._log_count)))
        f = 0
        for n, fname in enumerate(os.listdir()):
            fext = fname[len(fname) - 4]
            if fext == PFILE[fid]:
                f += 1
                self._drlst[n] = fname
                print("{0}. {1}".format(f, fname))
        fnum = 0
        while fnum not in PFILE.keys():
            fnum = int(input("Enter file # from list: "))
            if fnum in self._drlst and \
                    os.path.exists(self._drlst[fnum]):
                if fid == 1:
                    print("Updated text file from {0} to {1}".format(
                        self._txtifd.filename, self._drlst[fnum]))
                    self._txtifd.filename = self._drlst[fnum]
                if fid == 2:
                    print("Updated key file from {0} to {1}".format(
                        self._keyifd.filename, self._drlst[fnum]))
                    self._keyifd.filename = self._drlst[fnum]
                if fid == 3:
                    print("Updated csv file from {0} to {1}".format(
                        self._csv, self._drlst[fnum]))
                    self._csv = self._drlst[fnum]
                if fid == 4:
                    print("Updated log file from {0} to {1}".format(
                        self._log_count, self._drlst[fnum]))
                    self._log_count = self._drlst[fnum]

    def echo_result(self) -> None:
        """
        (Class:KeyKrawler) => Method: echo_result() -> None
        Print the results formatted in a table to the console
        ...
        """
        table_data = []
        self._purge_limits()
        for i, item in enumerate([x for x in self._reskta.keys_found]):
            item = LOGTXT['echo_result'].format(
                item[0:self._abrvt]
                if len(item) > self._abrvt
                else item)
            table_data.append([
                i,
                item,
                self._reskta.keys_found
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
        (Class:KeyKrawler) => echo_stats() -> None
        Prints analysis totals in a table to the console
        ...
        """
        table_data = [
            ["Keys", self._keyifd.unique_item_count],
            ["Text", self._txtifd.unique_item_count],
            ["Matches", self._reskta.total_matches],
            ["Comparisons", self._reskta.total_comparisons]
            # ["Logs", self._logger.log_count]
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
        (Class:KeyKrawler) => Method: get_key2text_matches() -> None
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
        self._txtifd.thread.start()
        # spinner.stop_and_persist(SYMB['success'], LOGTXT['extract'].format(
        #     self.__key_file, self.__timer.timestampstr()))
        # spinner = Halo("Itemizing Keys", spinner='dots')
        # spinner.start()
        self._keyifd.thread.start()
        # spinner.stop_and_persist(SYMB['success'], LOGTXT['extract'].format(
        #     self.__text_file, self.__timer.timestampstr()))
        # spinner = Halo("Itemizing Keys", spinner='dots')
        # spinner.start()
        self._txtifd.thread.join()
        self._keyifd.thread.join()
        self._keyifd.echo_stopwords()
        input()

        self._reskta = kta(
            self._txtifd.dict,
            self._keyifd.dict,
            STOP_WORDS,
            self._fuzrat
        )
        if self._reskta.run_keys2text_all():
            if self.results2file():
                if self._reskta.echo_keys_found():
                    return self._reskta.keys_found
        # spinner.stop_and_persist(SYMB['success'], LOGTXT['extract'].format(
        #     self.__key_file, self.__timer.timestampstr()))
        return None

    def results2file(self) -> bool:
        """
        (Class:KeyKrawler) => Method: results2file() -> bool
        Get KeyTextAnalysis results from _reskta.keys_found
        and formats to write it to CSV file (_csv)
        ...
        """
        with open(self._csv, 'w') as fh:
            write_count = 0
            # spinner = Halo(
            #     text=LOGTXT['write_results2file'].format(
            #         self._csv),
            #     spinner='dots'
            # )
            # spinner.start()
            self._purge_limits()
            for item in self._reskta.keys_found:
                write_count += 1
                csv_formatted_item = LOGTXT['csv_formatted_item'].format(
                    str(item), str(self._reskta.keys_found), LINE)
                fh.write(csv_formatted_item)
            fh.close()
            # spinner.stop_and_persist(
            #     SYMB['success'],
            #     "{0} Complete.[{1}]".format(
            #         self._csv,
            #         self.__timer.timestampstr()
            #     )
            # )
            return True
        return False

    def _limresult(self) -> bool:
        """
        (Class:KeyKrawler) => Method: _limresult() -> bool
        Remove items above the _limres
        ...

        Return
        ------
        -> bool, True if limit is set for items to be removed from result
        """
        if self._limres is not None:
            for i, item in enumerate([x for x in self._reskta.keys_found]):
                if i >= self._limres:
                    del self._reskta.keys_found[item]
            return True
        return False

    def _purge_limits(self) -> bool:
        """
        (Class:KeyKrawler) => Method: _purge_limits() -> bool
        Remove items with total number of matches
        below the lower boundry and above upper-boundry

        ...

        Return
        ------
        -> bool, True if items were removed outside the limits set
        """
        if self._lolb is not None \
                and self._uplb is not None:
            for item in enumerate([x for x in self._reskta.keys_found]):
                if (self._reskta.keys_found[item] < self._lolb) \
                    and (self._reskta.keys_found[item]
                         > self._uplb):
                    del self._reskta.keys_found[item]
                    self._rcnt -= 1
            return True
        return True

    # def _vrbs(self, *args) -> None:

    #     (Class:KeyKrawler) => Method: _vrbs() -> None
    #     If _set_verbose:=True then increase output to console
    #     ...

    #     if self._vrbs and args:
    #         print(self._logger.write_log(
    #             [str(x) for x in args], phony="yes"
    #         ))

    def _verify_files(self, *args) -> bool:
        """
        (Class:KeyKrawler) => Method: _verify_files(*args) -> bool
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
