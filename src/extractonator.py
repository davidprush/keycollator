# -*- coding: utf-8 -*-
"""
┌─┐─┐ ┬┌┬┐┬─┐┌─┐┌─┐┌┬┐┌─┐┌┐┌┌─┐┌┬┐┌─┐┬─┐
├┤ ┌┴┬┘ │ ├┬┘├─┤│   │ │ ││││├─┤ │ │ │├┬┘
└─┘┴ └─ ┴ ┴└─┴ ┴└─┘ ┴ └─┘┘└┘┴ ┴ ┴ └─┘┴└─

Copyright (C) 2022 Rush Solutions, LLC
Author: David Rush <davidprush@gmail.com>
License: MIT
Contains class:

    obj = KeyKrawler(text_file=TEXT, key_file=KEY, csv_file=CSV,
                    limit_result=None, abrev_items=32, log_file=LOG,
                    verbose=False, ubound_limit=None, lbound_limit=None,
                    fuzzy_match=99, logging=False, run_now=False) -> obj

    └──subclass:ItemizeFile:
           obj = Itemizefile(filename: str, [stopwords]: list,
                            [logfile]: str, [verbose]: bool,
                            [fuzzy_matching]: int) -> obj

    └──subclass:ItemizeFile.TextAnalysis:
            obj = ItemizeFile.TextAnalysis([fuzzy_matching]: int, optional) -> obj

Todo:
    ✖ Refactor code and remove redunancies
    ✖ Fix pylint errors
    ✖ Add proper error handling
    ✖ Add CHANGELOG.md
    ✖ Create method to KeyKrawler to select and _create missing files_
    ✖ Update CODE_OF_CONDUCT.md
    ✖ Update CONTRIBUTING.md
    ✖ Github: issue and pr templates
    ✖ Workflow Automation
    ✖ Makefile Usage
    ✖ Dockerfile
    ✖ @dependabot configuration
    ✖ Release Drafter (release-drafter.yml)
"""
import sys
import os.path
import string
import joblib
import termtables as tt

from halo import Halo
from fuzzywuzzy import fuzz
from collections import defaultdict

import nltk.data
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

from consts import \
    LINE, STOP_WORDS, SYMB, LOGTXT, TEXT, \
    KEY, CSV, LOG, RTBLHDR, STBLHDR, TAB, SQT

from proceduretimer import ProcedureTimer
from customlogger import CustomLogger

import nltk.downloader
"""
Module Requires:

    "punkt" for nltk

    CLI command:

        python3 -m nltk.downloader punkt
"""
try:
    dler = nltk.downloader.Downloader()
    if dler._status_cache['punkt'] != 'installed':
        dler._update_index()
        dler.download('punkt')
except Exception as ex:
    print(ex)  # replace with CustomLogger


class ItemizeFile:
    """
    Class: ItemizeFile

    obj = Itemizefile(filename: str, [stopwords]: list,
                        [logfile]: str, [verbose]: bool,
                        [fuzzy_matching]: int)

    subclass => TextAnalysis:

    obj = ItemizeFile.TextAnalysis([fuzzy_matching]: int, optional)
    ...
    Features
    --------

    Attributes
    ----------
    __timer:=obj, instance of ProcedureTimer("ItemizeFile")
    __filename:=str, set to optional fname parameter
    __file_exists:=bool, True if __filename exists, false otherwise
    __stopwords:=list, words to be removed from the text
    __origin_map:=dict, init to defaultdict(list), for __dict meta data
    __dict:=dict, init to defaultdict(int),
    __indexed:= init to defaultdict(int),
    __log:=list, used for recording event data
    __log_count:=int, iterative for items added to __log
    __unique_items:=int, total num. of unique items added to __dict
    __file_items:=int, total num. of items (lines) of text from __filename
    __logger:=obj, instance of CustomLogger(filename=logfile, phony='yes')
    __other:=obj, another instance of this class to be used for analysis
    __ta:=obj, instance of TextAnalysis(fuzzy_matching)

    Methods
    -------
    self.file_exists(fname) -> bool
        method of Itemizefile, verifies __filename exists
    CustomLogger(filename=logfile, phony='yes') -> obj
        instance for timing events
    TextAnalysis(fuzzy_matching) -> obj
        used to analyze text of other instance of this class

    Parameters
    ----------
    fname:=str, required filename of text to be used by this instance
    stopwords=list, stop words to be removed from text, default=consts.STOP_WORDS
    logfile=str, optional name of file for log, default=consts.LOG
    verbose=bool, optional flag for verbosity, default=False
    fuzzy_matching=int, ratio representation for fuzzy-matching, default=9
    """

    # subclass of ItemizeFile
    class TextAnalysis:
        """
        Class: TextAnalysis Parent Class: ItemizeFile

        obj = ItemizeFile.TextAnalysis([fuzzy_matching]: int, optional)

        ...
        Features
        --------

        Attributes
        ----------
        __timer:=obj, class instance of ProcedureTimer("TextAnalysis")
        __result_dict:=dict, init to defaultdict(int)
        __result_map:=dict, init to defaultdict(list)
        __result_count:=int, init to 0
        __search_text:=dict, init to defaultdict(int)
        __search_map:=dict, init to defaultdict(list)
        __key_text:=dict, init to defaultdict(int)
        __key_map:=dict, init to defaultdict(list)
        __log:=list, init to []
        __eval_count:=int, init to 0
        __fuzzy_matching:=int,
            inti to fm_level=99, used for fuzz-matching see not below
        __has_match:=bool, init to False

        Methods
        -------
        ProcedureTimer("TextAnalysis"):obj(class)

        Parameters
        ----------
        fm_level:=int, ratio for fuzzy-matching
            Uses the fuzzywuzzy library that implements:
                *Levenshtein distance =>
                    is a string metric for measuring the difference between
                    two sequences. Informally, the Levenshtein distance between
                    two words is the minimum number of single-character edits
        """

        def __init__(
            self,
            fm_level=99
        ) -> None:
            """
            Class: TextAnalysis method:__init__ to instantiate class attributes

                obj = TextAnalysis([fuzzy_matching]: int, optional)
            ...

            Attributes
            ----------
            __timer:=obj, class instance of ProcedureTimer("TextAnalysis")
            __result_dict:=dict, init to defaultdict(int)
            __result_map:=dict, init to defaultdict(list)
            __result_count:=int, init to 0
            __search_text:=dict, init to defaultdict(int)
            __search_map:=dict, init to defaultdict(list)
            __key_text:=dict, init to defaultdict(int)
            __key_map:=dict, init to defaultdict(list)
            __log:=list, init to []
            __eval_count:=int, init to 0
            __fuzzy_matching:=int,
                inti to fm_level=99, used for fuzz-matching see not below
            __has_match:=bool, init to False

            Methods
            -------
            ProcedureTimer("TextAnalysis"):=obj(class)

            Parameters
            ----------
            fm_level:=int, ratio for fuzzy-matching
                Uses the fuzzywuzzy library that implements:
                    *Levenshtein distance =>
                        is a string metric for measuring the difference between
                        two sequences. Informally, the Levenshtein distance between
                        two words is the minimum number of single-character edits
            """
            self.__timer = ProcedureTimer("TextAnalysis")
            self.__result_dict = defaultdict(int)
            self.__result_map = defaultdict(list)
            self.__result_count = 0
            self.__search_text = defaultdict(int)
            self.__search_map = defaultdict(list)
            self.__key_text = defaultdict(int)
            self.__key_map = defaultdict(list)
            self.__log = []
            self.__eval_count = 0
            self.__fuzzy_matching = fm_level
            self.__has_match = False

        @property
        def search_map(self) -> dict:
            return self.__search_map

        @search_map.setter
        def search_map(self, value) -> None:
            self.__search_map = value

        @property
        def key_text(self) -> dict:
            return self.__key_text

        @key_text.setter
        def key_text(self, value) -> None:
            self.__key_text = value

        @property
        def key_map(self) -> dict:
            return self.__key_map

        @key_map.setter
        def key_map(self, value) -> None:
            self.__key_map = value

        @property
        def fuzzy_matching(self) -> None:
            self.__search_text

        @fuzzy_matching.setter
        def fuzzy_matching(self, value) -> None:
            self.__fuzzy_matching = value

        @property
        def result_dict(self) -> dict:
            return self.__result_dict

        @result_dict.setter
        def result_dict(self, value) -> None:
            if len(self.__result_dict) == 0:
                self.__result_dict = value

        @property
        def result_map(self) -> dict:
            return self.__result_map

        @result_map.setter
        def result_map(self, key, item, indx) -> None:
            self.__result_map.append[
                item,
                self.__result_dict[item],
                indx]

        def eval_text(self) -> bool:
            """
            Class: TextAnalysis method: eval_text() -> bool
            Validates the following objects then calls method eval_text() -> bool
            ...

            Attributes
            ----------
            __key_text
            __search_text
            __eval_count
            __result_map(key, item, indx)
            __has_match = True
            __result_map(key, item, indx)

            Methods
            -------
            eval_text() -> bool, True if matches found, otherwise False
                └──:__eval_direct_match(key, item) -> bool
                └──:__eval_tokenized_match(key, item) -> bool
                └──:__eval_fuzzy_match(key, item) -> bool
                └──:__result_map(key, item, indx) -> bool
                └──:__sort_dict() -> bool

            Returns
            -------
            -> bool, True if matches found, False otherwise
            """
            for key in self.__key_text:
                for item in self.__search_text:
                    indx = [[key, self.__key_text], [item, self.__search_text]]
                    self.__eval_count += 1
                    self.log.append(
                        LOGTXT['timer'].format(self.__timer.timestampstr()),
                        LOGTXT['EVALUATED'].format(
                            self.__eval_count, key,
                            self.__key_text[key],
                            item, self.__search_text))
                    if self.eval_direct_match(key, item):
                        self.__result_map(key, item, indx)
                        self.__has_match = True
                    elif self.eval_tokenized_match(key, item):
                        self.__result_map(key, item, indx)
                        self.__has_match = True
                    elif self.eval_fuzzy_match(key, item):
                        self.__result_map(key, item, indx)
                        self.__has_match = True
            if self.__has_match:
                self.sort_dict()
                return self.__has_match
            self.__has_match = False
            return self.__has_match

        def eval_direct_match(self, key, item) -> bool:
            """
            TextAnalysis
            Parameters
            ----------
                []]: [type], [required/optional]
            """
            if key in item:
                self.__result_dict[key] += 1
                self.__result_count += 1
                self.log.append(
                    LOGTXT['timer'].format(self.__timer.timestampstr()),
                    self.__eval_count, self.__result_count,
                    key, self.__search_text[item], item)
                return True
            return False

        def eval_tokenized_match(self, key, item) -> bool:
            """
            TextAnalysis
            Parameters
            ----------
                []]: [type], [required/optional]
            """
            tokenized_key = word_tokenize(key)
            key_string = str(tokenized_key)
            item_tokenized = word_tokenize(item)
            item_string = str(item_tokenized)
            if key_string in item_string:
                self.__result_dict[key] += 1
                self.__result_count += 1
                return True
            return False

        def eval_fuzzy_match(self, key, item) -> bool:
            """
            Class: TextAnalysis method: eval_fuzzy_match(key: str, item: str) -> bool
            Uses the fuzzywuzzy library that implements:
                *Levenshtein distance =>
                    is a string metric for measuring the difference between
                    two sequences. Informally, the Levenshtein distance between
                    two words is the minimum number of single-character edits
            ...

            Attributes
            ----------
            __fuzzy_matching:=int, ratio [1-99] where
                                1 is insensitive and 99 is discriminant
            __result_dict[key]:=dict, representing item of iterative int,
                                key is unique text/line str from __filename
            __result_count:=int, total number of unique keys

            Returns
            -------
            -> bool, True if fuzzy-match found, otherwise Fale
            """
            if fuzz.partial_ratio(key, item) >= self.__fuzzy_matching:
                self.__result_dict[key] += 1
                self.__result_count += 1
                return True
            return False

        def sort_dict(self) -> bool:
            """
            Class: TextAnalysis method: sort_dict() -> bool
            Sorts the __result_dict (dict) in descending order
                keys:=str, text/lines from file __filename
                items:=int, iterative count, init to 0
            ...

            Attributes
            ----------
            __result_dict:=dict, of strings as keys, extracted from __filename

            Returns
            -------
            -> bool, True if other is instance of the class ItemizeFile
            """
            if len(self.__result_dict) > 0:
                self.__result_dict = dict(sorted(
                    self.__result_dict.items(),
                    key=lambda item: item[1], reverse=True))
                return True
            return False

        def run_all(self) -> bool:
            """
            Class: TextAnalysis method: run_all() -> bool
            Validates the following objects then calls method eval_text() -> bool
            ...

            Attributes
            ----------
            __search_text:=dict, used to search for keys from __key_text
            __key_text:=dict, used to search for items in __search_text
            __search_map:=dict, meta data about searches
            __key_map:=dict, meta data about keys

            Methods
            -------
            eval_text() -> bool, True if matches found, otherwise False
                └──:eval_direct_match(key, item) -> bool
                └──:eval_tokenized_match(key, item) -> bool
                └──:eval_fuzzy_match(key, item) -> bool
                └──:result_map(key, item, indx) -> bool
                └──:sort_dict() -> bool

            Returns
            -------
            -> bool, True if required attributes are satisfied
            """
            if len(self.__search_text) > 0 \
                and len(self.__key_text) > 0 \
                    and len(self.__search_map) > 0 \
                    and len(self.__key_map) > 0:
                self.eval_text()
                return True
            return False

    def __init__(
        self,
        fname,
        stopwords=STOP_WORDS,
        logfile=LOG,
        verbose=False,
        fuzzy_matching=99
    ) -> None:
        """
        Class: ItemizeFile method:__init__ to instantiate class attributes
        ...

        Attributes
        ----------
        __timer:=obj, instance of ProcedureTimer("ItemizeFile")
        __filename:=str, set to optional fname parameter
        __file_exists:=bool, True if __filename exists, false otherwise
        __stopwords:=list, words to be removed from the text
        __origin_map:=dict, init to defaultdict(list), for __dict meta data
        __dict:=dict, init to defaultdict(int),
        __indexed:= init to defaultdict(int),
        __log:=list, used for recording event data
        __log_count:=int, iterative for items added to __log
        __unique_items:=int, total num. of unique items added to __dict
        __file_items:=int, total num. of items (lines) of text from __filename
        __logger:=obj, instance of CustomLogger(filename=logfile, phony='yes')
        __other:=obj, another instance of this class to be used for analysis
        __ta:=obj, instance of TextAnalysis(fuzzy_matching)

        Methods
        -------
        self.file_exists(fname) -> bool
            method of Itemizefile, verifies __filename exists
        CustomLogger(filename=logfile, phony='yes') -> obj
            instance for timing events
        TextAnalysis(fuzzy_matching) -> obj
            used to analyze text of other instance of this class

        Parameters
        ----------
        fname:=str, required filename of text to be used by this instance
        stopwords=list, stop words to be removed from text, default=consts.STOP_WORDS
        logfile=str, optional name of file for log, default=consts.LOG
        verbose=bool, optional flag for verbosity, default=False
        fuzzy_matching=int, ratio representation for fuzzy-matching, default=9
        """
        self.__timer = ProcedureTimer("ItemizeFile")
        self.__filename = fname
        self.__file_exists = self.file_exists(fname)
        self.__stopwords = []
        self.__origin_map = defaultdict(list)
        self.__dict = defaultdict(int)
        self.__indexed = defaultdict(int)
        self.__log = []
        self.__log_count = 0
        self.__unique_items = 0
        self.__file_items = 0
        self.__logger = CustomLogger(filename=logfile, phony='yes')
        self.__other = self
        self.__ta = ItemizeFile.TextAnalysis(fuzzy_matching)

    def __repr__(self) -> str:
        return f'{type(self).__name__}(filename={self.__filename}, \
            file_exists={self.__file_exists} stopwords={self.__stopwords} \
            itemized={self.__origin_map})'

    def __eq__(self, obj) -> bool:
        if isinstance(obj, ItemizeFile):
            self.__other = obj
            return True if self.__other.__unique_items > self.__unique_items else False
        else:
            return False

    @property
    def ta(self) -> object:
        """
        Class: ItemizeFile property: __ta
        @property
        def ta(self):
            return self.__ta
        -> obj(class) instance of TextAnalysis
        """
        return self.__ta

    @ta.setter
    def ta(self, obj=None) -> None:
        """
        Class: ItemizeFile property: __ta
        @ta.setter
        def ta(self, value):
            self.__ta = value
        """
        self.__ta = obj

    @property
    def filename(self) -> str:
        """
        Class: ItemizeFile property: __filename
        return self.__filename

        """
        return self.__filename

    @filename.setter
    def filename(self, value) -> None:
        """
        Class: ItemizeFile property: __filename
        self.__filename = value

        """
        self.__filename = value

    @property
    def dict(self) -> dict:
        """
        Class: ItemizeFile property: __dict
        return self.__dict

        """
        return self.__dict

    @dict.setter
    def dict(self, obj=None) -> None:
        """
        Class: ItemizeFile property: __dict, setter
        obj:=list, to set to attribute __dict
        @dict.setter
            def dict(self, obj=None):
            self.__dict = obj
        """
        self.__dict = obj

    @property
    def stopwords(self) -> None:
        """
        Class: ItemizeFile property: __stopwords
        @stopwords.setter
            def stopwords(self, obj=None):
            self.__stopwords = list(obj)
        stopwords() -> list, __stopwords property
        """
        return [x for x in self.__stopwords]

    @stopwords.setter
    def stopwords(self, obj=None) -> None:
        """
        Class: ItemizeFile property: __stopwords, setter
        obj:=list, to set to attribute __stopwords
        @stopwords.setter
            def stopwords(self, obj=None):
            self.__stopwords = list(obj)
        """
        self.__stopwords = list(obj)

    @property
    def log(self) -> list:
        """
        Class: ItemizeFile property: __log
        @log.setter
            def log(self, obj=None):
            self.__log = list(obj)
        log() -> list, __log property
        """
        return self.__log

    @log.setter
    def log(self, obj=None) -> None:
        """
        Class: ItemizeFile property: __log, setter
        obj:=list, to set to attribute __log
        @log.setter
            def log(self, obj=None):
            self.__log = list(obj)
        """
        self.__log = list(obj)

    def unique_items(self) -> int:
        return self.__unique_items

    def file_items(self) -> int:
        return self.__file_items

    def indexed_obj(self) -> dict:
        return self.__indexed

    def dict_obj(self) -> dict:
        return self.__dict

    def itemized_obj(self) -> dict:
        """
        Class: ItemizeFile method:
        def itemized_obj(self):
            return self.__origin_map
        """
        return self.__origin_map

    def run_anlysis(self, other) -> bool:
        """
        Class: ItemizeFile method: run_analysis(other: class) -> bool
        Sets the following attributes from [other] ItemizeFile class
        and attributes for [ta] instance of the TextAnalysis class
        ...

        Attributes
        ----------
        .dict:=dict, contains file text from current ItemizeFile instance (self)
        __other.dict:=dict, contains the dict from [other] to analyze against .dict
        __origin_map:=list, this instances file meta data
        __ta.search_text:=str copy of current instance .dict
        __ta.key_text:=str copy of other instance .dict
        __ta.search_map:=list, current instance of ItemizeFile .dict meta data
        __ta.key_map:=dict other instance .dict meta data
        other.__origin_map:= another instance of ItemizeFile
        __other:= class, another instance of ItemizeFile, used as key items

        Methods
        -------
        __ta.run_all() method from TextAnalysis class

        Parameters
        ----------
        other:=class, containing another instance of ItemizeFile class

        Returns
        -------
        -> bool, True if other is instance of the class ItemizeFile
        """
        if isinstance(other, ItemizeFile):
            self.__other = other
            self.__ta.search_text = self.dict
            self.__ta.key_text = self.__other.dict
            self.__ta.search_map = self.__origin_map
            self.__ta.key_map = other.__origin_map
            self.__ta.run_all()
            return True
        else:
            return False

    def sanitize(self, text) -> str:
        """
        Class: ItemizeFile method: sanitize(text: str) -> str
        Sets all chars to lower case and removes all special chars/end lines

        Parameters
        ----------
        log:=list, meta data about removals from text

        Returns
        -------
        -> str, all lowercase, without special chars, nor end lines
        """
        temp_text = text
        text = str(text) if not isinstance(text, str) else text
        text = text.replace(LINE, '')
        text = text.translate(text.maketrans(
            "",
            "",
            string.punctuation
        ))
        text.lower()
        self.log.append([temp_text, text])
        return text

    def pop_stop_words(self, text) -> str:
        """
        Class: ItemizeFile method: pop_stop_words(text: str) -> str
        Removes stop_words from text: str
        ...

        Attributes
        ----------
        __stopwords:=list, items to remove from text
        log:=list, to append with actions removal meta data

        Parameters
        ----------
        text : str, Text to remove stop words from

        Returns
        -------
        -> str, without stop words
        """
        for i, word in enumerate(self.__stopwords):
            self.log.append([i, word, text])
            print(word)
            return text.replace(" {0} ".format(word), " ")
        self.log.append(['stop-words-removed', text])
        return text

    def file_exists(self, fname=None) -> bool:
        """
        Class: ItemizeFile method: file_exists(fname: str) -> bool
        Verifies fname (filename) exists
        ...

        Attributes
        ----------
        __file_exists:=bool, True if file exists, False if file does not exist
        __text_file:=str, Updates with fname if fname exists

        Parameters
        ----------
        fname : str, The name of the file to be verified

        Returns
        -------
        -> bool (True if file exists, otherwise False)
        """
        if fname is not None:
            if os.path.exists(fname):
                self.__file_exists = True
                self.__text_file = fname
                return self.__file_exists
            else:
                return False

    def get_itemized_file(self) -> dict:
        """
        Class: ItemizeFile method: get_itemized_file() -> dict
        Searches text file (self.__filename) for unique lines of
        text, sanitizes each line of text, adds values to the listed
        attributes
        ...

        Attributes
        ----------
        __file_items:=int, total number of lines of text searched
        __indexed:=list, sanitized lines of text
        __unique_items:=int, total number of unique lines of text
        __self_dict:=dict, "unique text lines": 0
        __origin_map:=list, contains meta data about the text

        Methods
        -------
        self.get_file_list() -> list
        self..sanitize(item) -> str

        Returns
        -------
        -> dict
            keys: uqique lines of text from file
            items: int (0) for future use as iterator
        """
        for self.__file_items, item in enumerate(self.get_file_list()):
            indx = item = self.sanitize(item)
            self.__indexed[indx] = self.__file_items
            if item not in [x for x in self.__dict]:
                self.__unique_items += 1
                item = self.pop_stop_words(item)
                self.__dict[item] = 0
                self.__origin_map[item] = [
                    self.__dict[item],
                    indx, self.__indexed[indx]]
                self.log.append(list([
                    self.__file_items, indx,
                    item, self.__unique_items, self.__origin_map[item]]))
        if self.__file_items > 0:
            return self.__dict
        else:
            return None

    def get_file_list(self) -> list:
        """
        Class: ItemizeFile method: get_file_list() -> list
        Places each line of text from file handler as items in list
        ...

        Attributes
        ----------
        __filename:=str, name of file to extract text from

        Returns
        --------
        -> list [each item is a str as a line from text file]
        """
        with open(self.__filename, 'r') as fh:
            filelist = [
                current_place.rstrip() for current_place in fh.readlines()]
            fh.close()
        return filelist

    def echo_log(self) -> bool:
        """
        Class: ItemizeFile method: echo_log() -> bool
        Prints __log (list) items to console
        ...

        Attributes
        ----------
        __log:=list, each item represents a log event

        Returns
        -------
        -> bool, True if __log contains items
        """
        if len(self.__log) > 1:
            for log in self.__log:
                log = "".join(log)
                log = log.replace(LINE, '')
                print("{0}".format(log))
            return True
        else:
            return False

    def dump_log(self) -> bool:
        """
        Class: ItemizeFile method: dump_log() -> bool
        Dumps all logs to CSV file (log_dump.csv)
        ...

        Attributes
        ----------
        __log:=list, each item represents a log event

        Returns
        -------
        -> bool, True if logs are dumped, otherwise False
        """
        if len(self.__log) > 1:
            joblib.dump(self.__log, 'log_dump.csv')
            return True
        else:
            return False

    def sort_dict(self) -> bool:
        """
        Class: ItemizeFile method: sort_dict() -> bool
        Sorts __dict (dict) by item count (integer)
        ...

        Attributes
        ----------
        __dict:=dict, keys:str representing lines of text from file
                    items: integer value

        Returns
        -------
        -> bool, True if __dict contains items, False otherwise
        """
        if len(self.__dict) != 0:
            self.__dict = dict(sorted(
                self.__dict.items(),
                key=lambda item: item[1], reverse=True))
            return True
        else:
            return False

    def run_all(self) -> bool:
        """
        Class: ItemizeFile method: run_all() -> bool
        Runs all necessary methods to set stage for
        text analysis using the TextAnalysis class as [ta]
        ...

        Methods
        -------
        itemized() -> bool, retrieves unique text/lines from __filename attribute
        echo_log() -> bool, displays logs in __log
        dump_log() -> bool, dumps all logs to CSV file "log_dump.csv"

        Returns
        -------
        -> bool, True if no errors, otherwise False
        """
        if self.get_itemized_file() is not None:
            if self.echo_log():
                if self.dump_log():
                    return True
        return False


class KeyKrawler:
    """
    Class: KeyKrawler

    obj = KeyKrawler(text_file=TEXT, key_file=KEY, csv_file=CSV,
                    limit_result=None, abrev_items=32, log_file=LOG,
                    verbose=False, ubound_limit=None, lbound_limit=None,
                    fuzzy_match=99, logging=False, run_now=False) -> obj

    └──subclass:ItemizeFile:
           obj = Itemizefile(filename: str, [stopwords]: list,
                            [logfile]: str, [verbose]: bool,
                            [fuzzy_matching]: int) -> obj

    └──subclass:ItemizeFile.TextAnalysis:
            obj = ItemizeFile.TextAnalysis([fuzzy_matching]: int, optional) -> obj
    ...
    Features
    --------

    Attributes
    ----------
    __timer = ProcedureTimer("KeyKrawler")
    __text_file = text_file
    __key_file = key_file
    __csv_file = csv_file
    __log_file = log_file
    __valid_files = False
    __key_dict = defaultdict(int)
    __text_dictionary = defaultdict(int)
    __result_dict = defaultdict(int)
    __limit_result = limit_result
    __abrev_items = abrev_items
    __ubound_limit = ubound_limit
    __lbound_limit = lbound_limit
    __fuzzy_matching = fuzzy_match
    __set_verbose = verbose
    __text_count = 0
    __key_count = 0
    __compare_count = 0
    __log_count = 0
    __result_count = 0
    __no_result = True
    __ps = PorterStemmer()
    __logging = logging
    __textobj = ItemizeFile(text_file, STOP_WORDS, TEXT, False, fuzzy_match)
    __keyobj = ItemizeFile(text_file, STOP_WORDS, KEY, False, fuzzy_match)
    __csvobj = ItemizeFile(text_file, STOP_WORDS, CSV, False, fuzzy_match)
    __logobj = ItemizeFile(text_file, STOP_WORDS, LOG, False, fuzzy_match)
    __logger = CustomLogger(phony="yes") if verbose else CustomLogger(phony="no")
    __sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    run_now: self.run()
    __timer.stop_timer(KeyKrawler)

    Methods
    -------
    run()

    Parameters
    ----------
    text_file: str, optional
        Name of the text file to find keys. (default: TEXT)
    key_file: str, optional
        Name of file to read keys. (default: KEY)
    csv_file str, optional
        Name of the file to write results. (default: CSV)
    limit_result: int, optional
        Sets the limit to the number (integer) of results
        where 0 is no limit and any number equal or above
        1 implements a limit (default: 0)
    log_file: str, optional
        Name of the file to write logs (default: LOG)
    verbose: bool, optional
        Verbosity flag where False is off and True is on. (default: False)
    ubound_limit: int, optional
        Upper bound limit to reject key matches above the value.
        Helps eliminate eroneous results when using fuzzy matching.
        (default: 99999)
    lbound_limit: int, optional
        Lower bound limit to reject key matches below the value.
        Helps eliminate eroneous results when using fuzzy matching. (default: 0)
    fuzzy_match: int, optional
        Sets the level of fuzzy matching, range(0:99), where 0 accepts
        nearly everythong and 99 accepts nearly identical matches. (default: 99)
    logging: bool, optional
        Logging flag where False is off and True is on. (default: 0)
    """

    def __init__(
        self,
        text_file=TEXT,
        key_file=KEY,
        csv_file=CSV,
        limit_result=None,
        abrev_items=32,
        log_file=LOG,
        verbose=False,
        ubound_limit=None,
        lbound_limit=None,
        fuzzy_match=99,
        logging=False,
        run_now=False
    ) -> None:
        self.__timer = ProcedureTimer("KeyKrawler")
        self.__text_file = text_file
        self.__key_file = key_file
        self.__csv_file = csv_file
        self.__log_file = log_file
        self.__valid_files = False
        self.__key_dict = defaultdict(int)
        self.__text_dictionary = defaultdict(int)
        self.__result_dict = defaultdict(int)
        self.__limit_result = limit_result
        self.__abrev_items = abrev_items
        self.__ubound_limit = ubound_limit
        self.__lbound_limit = lbound_limit
        self.__fuzzy_matching = fuzzy_match
        self.__set_verbose = verbose
        self.__text_count = 0
        self.__key_count = 0
        self.__compare_count = 0
        self.__log_count = 0
        self.__result_count = 0
        self.__no_result = True
        self.__ps = PorterStemmer()
        self.__logging = logging
        self.__textobj = ItemizeFile(
            text_file,
            STOP_WORDS, TEXT,
            False, fuzzy_match)
        self.__keyobj = ItemizeFile(
            text_file,
            STOP_WORDS, KEY,
            False, fuzzy_match)
        self.__csvobj = ItemizeFile(
            text_file,
            STOP_WORDS, CSV,
            False, fuzzy_match)
        self.__logobj = ItemizeFile(
            text_file,
            STOP_WORDS, LOG,
            False, fuzzy_match)
        self.__logger = CustomLogger(
            phony="yes") if verbose else CustomLogger(
                phony="no")
        self.__sent_detector = nltk.data.load(
            'tokenizers/punkt/english.pickle')
        if run_now:
            self.run()
        self.__timer.stop_timer(KeyKrawler)

    def sanitize(self, text) -> str:
        """
        Class: KeyKrawler method sanitize(text: str) -> str
        Remove special chars/end lines and set to lower case
        ...

        Parameters
        ----------
        text:=str, text (str) to remove special chars/end lines
            and set to lower case
        Attributes
        ----------
        __set_verbose:=bool, True=[verbose ON]|False=[verbose OFF]

        Methods
        -------
        __logger.write_log -> str, a CustomLogger that returns a
            formatted str of the log event
        __verbose(*args) -> None, evaluates verbose message and status

        """
        text = str(text) if not isinstance(text, str) else text
        text = text.replace(LINE, '')
        text = text.translate(text.maketrans(
            "",
            "",
            string.punctuation
        ))
        for word in STOP_WORDS:
            text = text.replace(LOGTXT['stop_word'].format(word), ' ')
        self.__verbose(
            LOGTXT['timer'].format(self.__timer.timestampstr()),
            self.__logger.write_log(LOGTXT['sanitized'].format(
                text)))
        return text.lower()

    def __verbose(self, *args) -> None:
        """
        Class: KeyKrawler method __verbose() -> None
        If _set_verbose:=True then increase output to console
        ...
        Attributes
        ----------
        __set_verbose:=bool, True=[verbose ON]|False=[verbose OFF]

        Methods
        -------
        __logger.write_log -> str, a CustomLogger that returns a
            formatted str of the log event
        """
        if self.__set_verbose and args:
            print(self.__logger.write_log(
                [str(x) for x in args], phony="yes"
            ))

    def limit_result(self) -> bool:
        """
        Class: KeyKrawler method limit_result() -> bool
        Remove items above the __limit_result
        ...
        Attributes
        ----------
        __textobj.ta.result_dict:=dict, matched results of keys found
        __limit_result:=int, limit the number of items in result
        __timer.timestampstr():=float, total to for completion

        Methods
        -------
        purge_limited_items() -> bool, removes items if the number
            of matches are above or below the lower and upper limits
        __verbose(*args) -> None, evaluates verbose message and status

        Return
        ------
        -> bool, True if limit is set for items to be removed from result
        """
        if self.__limit_result is not None:
            for i, item in enumerate([x for x in self.__textobj.ta.result_dict]):
                if i >= self.__limit_result:
                    self.__verbose(
                        LOGTXT['timer'].format(self.__timer.timestampstr()),
                        self.__logger.write_log(
                            LOGTXT['limit_result'].format(
                                item, self.__textobj.ta.result_dict[item])))
                    del self.__textobj.ta.result_dict[item]
            return True
        return False

    def echo_result(self) -> None:
        """
        Class: KeyKrawler method echo_result() -> None
        Print to console results in a table
        ...
        Attributes
        ----------
        __textobj.ta.result_dict:=dict, matched results of keys found

        Methods
        -------
        purge_limited_items() -> bool, removes items if the number
            of matches are above or below the lower and upper limits
        """
        table_data = []
        self.purge_limited_items()
        for i, item in enumerate([x for x in self.__textobj.ta.result_dict]):
            item = LOGTXT['echo_result'].format(
                item[0:self.__abrev_items]
                if len(item) > self.__abrev_items
                else item)
            table_data.append([
                i,
                item,
                self.__textobj.ta.result_dict
            ])
        tt.print(
            table_data,
            header=RTBLHDR,
            style=tt.styles.rounded,
            padding=(0, 0),
            alignment="clc"
        )

    def purge_limited_items(self) -> bool:
        """
        Class: KeyKrawler method purge_limited_items() -> bool
        Remove items with total matches above and below limits
        ...
        Attributes
        ----------
        __lbound_limit is not None:=int, items with total matches
            below this number are excluded from results
        __ubound_limit is not None:=int, items with total matches
            above this number are excluded from results
        __textobj.ta.result_dict:=dict, matched results of keys found
        __timer.timestampstr():=float, total to for completion
        __result_count:=int, to number of matches

        Methods
        -------
        __verbose(*args) -> None, evaluates verbose message and status
        __logger.write_log -> str, a CustomLogger that returns a
            formatted str of the log event

        Return
        ------
        -> bool, True if items were removed outside the limits set
        """
        if self.__lbound_limit is not None \
                and self.__ubound_limit is not None:
            for item in enumerate([x for x in self.__textobj.ta.result_dict]):
                if (self.__textobj.ta.result_dict[item] < self.__lbound_limit) \
                    and (self.__textobj.ta.result_dict[item]
                         > self.__ubound_limit):
                    del self.__textobj.ta.result_dict[item]
                    self.__verbose(
                        LOGTXT['timer'].format(
                            self.__timer.timestampstr()),
                        self.__logger.write_log(
                            LOGTXT['purge_limited_items'].format(
                                item, self.__textobj.ta.result_dict[item])))
                    self.__result_count -= 1
            return True
        return True

    def echo_stats(self) -> None:
        """
        Class: KeyKrawler echo_stats() -> None
        Prints analysis totals in a table to the console
        ...
        Attributes
        ----------
        __key_count:=int, total key items used for analysis
        __text_count:=int, total text items searched for keys
        __result_count:=int, total key items found in text
        __compare_count:=int, total comparisons evaluated
        __logger.log_count:=int, total log events
        __timer.timestamp(True):=float, total run time
        """
        table_data = [
            ["Keys", self.__key_count],
            ["Text", self.__text_count],
            ["Matches", self.__result_count],
            ["Comparisons", self.__compare_count],
            ["Logs", self.__logger.log_count],
            ["Runtime", self.__timer.timestamp(True)]
        ]
        tt.print(
            table_data,
            header=STBLHDR,
            style=tt.styles.rounded,
            padding=(0, 0),
            alignment="lc"
        )

    def reset_log_file(self) -> bool:
        """
        Class: KeyKrawler method reset_log_file() -> bool
        Resets the log file (__log_file) be overwriting it
        ...
        Attributes
        ----------
        __log_file:=str, name of file to write log

        Return
        ------
        -> bool, True if file is written
        """
        with open(self.__log_file, 'w') as fh:
            fh.close()
            return True
        return False

    def write_result2file(self) -> bool:
        """
        Class: KeyKrawler method write_result2file() -> bool
        Get TextAnalysis results from __textobj.ta.result_dict
        and formats to write it to CSV file (__csv_file)
        ...
        Attributes
        ----------
        __csv_file:=str, name of CSV file to write results
        __textobj.ta.result_dict:=dict, results from TextAnalysis
        __timer.timestampstr():=object, containing timestamp

        Methods
        -------
        purge_limited_items() -> bool, removes items if the number
            of matches are above or below the lower and upper limits
        __logger.write_log -> str, a CustomLogger that returns a
            formatted str of the log event
        """
        with open(self.__csv_file, 'w') as fh:
            write_count = 0
            spinner = Halo(
                text=LOGTXT['write_results2file'].format(
                    self.__csv_file),
                spinner='dots'
            )
            spinner.start()
            self.purge_limited_items()
            for item in self.__textobj.ta.result_dict:
                write_count += 1
                csv_formatted_item = LOGTXT['csv_formatted_item'].format(
                    str(item), str(self.__textobj.ta.result_dict), LINE)
                fh.write(csv_formatted_item)
                self.__verbose(
                    LOGTXT['timer'].format(self.__timer.timestampstr()),
                    self.__logger.write_log(
                        write_count, item,
                        self.__textobj.ta.result_dict))
            fh.close()
            spinner.stop_and_persist(
                SYMB['success'],
                "{0} Complete.[{1}]".format(
                    self.__csv_file,
                    self.__timer.timestampstr()
                )
            )
            return True
        return False

    def run(self) -> None:
        """
        Class: KeyKrawler method: run() -> None
        Completes all necessary procedures to evaluate the text
        ...

        Attributes
        ----------
        __textobj.stopwords:=list, words to be removed from text
        __keyobj.stopwords:=list, words to be removed from text

        Methods
        -------
        reset_log_file() -> bool
        __textobj.get_itemized_file() -> dict
        __keyobj.echo_log() -> bool
        __textobj.run_anlysis(self.__keyobj) -> bool
        write_result2file() -> bool
        echo_stats() -> None
        """
        self.reset_log_file()
        spinner = Halo(
            "Itemizing Text",
            spinner='dots'
        )
        spinner.start()
        self.__textobj.stopwords = [x for x in STOP_WORDS]
        self.__textobj.get_itemized_file()
        spinner.stop_and_persist(
            SYMB['success'],
            LOGTXT['extract'].format(
                self.__key_file,
                self.__timer.timestampstr()
            )
        )
        # self.__itemize_keys()
        spinner = Halo(
            "Itemizing Keys",
            spinner='dots'
        )
        spinner.start()
        self.__keyobj.stopwords = [x for x in STOP_WORDS]
        self.__keyobj.get_itemized_file()
        self.__keyobj.echo_log()
        spinner.stop_and_persist(
            SYMB['success'],
            LOGTXT['extract'].format(
                self.__key_file,
                self.__timer.timestampstr()
            )
        )
        spinner = Halo(
            "Itemizing Keys",
            spinner='dots'
        )
        spinner.start()
        self.__textobj.run_anlysis(self.__keyobj)
        spinner.stop_and_persist(
            SYMB['success'],
            LOGTXT['extract'].format(
                self.__key_file,
                self.__timer.timestampstr()
            )
        )
        self.write_result2file()
        # self.__echo_result()
        self.echo_stats()

    def verify_files_exist(self, *args) -> bool:
        """
        Class: KeyKrawler method: verify_files_exist(*args) -> bool
        Verifies all file names (str) passed as args are valid
        ...

        Attributes
        ----------
        __valid_files:=bool, False if any of the files are not valid

        Parameters
        ----------
        *args:=any, all *args that are str will be evaluated as a
            possible file name

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
