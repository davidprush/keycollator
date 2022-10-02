# -*- coding: utf-8 -*-
"""
Copyright (C) 2022 Rush Solutions, LLC
Author: David Rush <davidprush@gmail.com>
License: MIT
Contains class:

    └──subclass:KeyTextAnalysis:
            obj = ItemizeFile.KeyTextAnalysis([fuzz_ratio]: int, optional) -> obj

Todo:
    ✖ Fix pylint errors
    ✖ Add proper error handling
    ✖ Create method to KeyKrawler to select and _create missing files
"""
import joblib

from fuzzywuzzy import fuzz
from collections import defaultdict

import nltk.data
from nltk.tokenize import word_tokenize

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


class KeyTextAnalysis:
    """
    Class: KeyTextAnalysis

            obj = KeyTextAnalysis(text_dict: dict,
                                    key_dict: dict,
                                    [fuzz_ratio]: int, optional)

    ...

    Attributes
    ----------
    __text_dict:=dict, text_dict parameter passed at instantiation
    __key_dict:=dict, key_dict parameter passed at instantiation
    __fuzz_ratio:=int,
        inti to fm_level=99, used for fuzz-matching see not below
    __key_matches:= , defaultdict(int)
    __key2text_index:=list, maps all matches to original text
        and stores all count totals
    __total_matches:=int, init to 0, total number of key matches
    __total_comparisons:=int, init to 0, total number of key to text evaluations
    __has_match:=bool, init to False

    Methods
    -------
    eval_keys2text() -> bool:Evaluates the key dictionary (key_dict)
        against the text dictionary (text_dict), populates the key_matches
        dictionary with the key and the total number of times the key appears
        in the text
    sort_dict() -> bool: Sorts the __key_matches (dict) in descending order
    echo_key_matches() -> bool: Prints the dictionary of key matches to console
    echo_indexed() -> bool: Prints the list of analysis comparisons to console
    dump_indexed() -> bool: Dumps indexed list to file indexed_list_dump.csv
    dump_matches() -> bool: Dumps matches to file key_match_dump.csv
    run_all() -> bool:
    __eval_direct(key, item) -> bool:
    __eval_tokenized(skey, item) -> bool:
    __eval_fuzz(key, item) -> bool:

    Parameters
    ----------
    text_dict:=dict, text_dict parameter passed at instantiation
    key_dict:=dict, key_dict parameter passed at instantiation
    fuzz_ratio:=int, ratio for fuzzy-matching
        Uses the fuzzywuzzy library that implements:
            *Levenshtein distance =>
                is a string metric for measuring the difference between
                two sequences. Informally, the Levenshtein distance between
                two words is the minimum number of single-character edits
    """

    def __init__(
        self,
        text_dict,
        key_dict,
        fuzz_ratio=99
    ) -> None:
        """
        Class: KeyTextAnalysis method:__init__ to instantiate class attributes

            obj = KeyTextAnalysis(text_dict: dict,
                                    key_dict: dict,
                                    [fuzz_ratio]: int, optional)

        ...


        Attributes
        ----------
        __text_dict:=dict, text_dict parameter passed at instantiation
        __key_dict:=dict, key_dict parameter passed at instantiation
        __fuzz_ratio:=int,
            inti to fm_level=99, used for fuzz-matching see not below
        __key_matches:= , defaultdict(int)
        __key2text_index:=list, maps all matches to original text
            and stores all count totals
        __total_matches:=int, init to 0, total number of key matches
        __total_comparisons:=int, init to 0, total number of key to text evaluations
        __has_match:=bool, init to False

        Parameters
        ----------
        text_dict:=dict, text_dict parameter passed at instantiation
        key_dict:=dict, key_dict parameter passed at instantiation
        fuzz_ratio:=int, ratio for fuzzy-matching
            Uses the fuzzywuzzy library that implements:
                *Levenshtein distance =>
                    is a string metric for measuring the difference between
                    two sequences. Informally, the Levenshtein distance between
                    two words is the minimum number of single-character edits
        """
        self.__text_dict = text_dict
        self.__key_dict = key_dict
        self.__fuzz_ratio = fuzz_ratio
        self.__key_matches = defaultdict(int)
        self.__key2text_index = []
        self.__total_matches = 0
        self.__total_comparisons = 0
        self.__has_match = False
        self.eval_keys2text()

    @property
    def text_dict(self) -> dict:
        """
        Class: KeyTextAnalysis Property: text_dict() -> dict
        ...
        Returns
        -------
        -> dict, text dictionary
        """
        return self.__text_dict

    @text_dict.setter
    def text_dict(self, obj=None) -> dict:
        """
        Class: KeyTextAnalysis Property: key_dict(obj) -> dict
        ...
        """
        self.__text_dict = dict(obj).copy

    @property
    def key_dict(self) -> dict:
        """
        Class: KeyTextAnalysis Property: key_dict() -> dict
        ...
        Returns
        -------
        -> dict, text keys dictionary
        """
        return self.__key_text

    @key_dict.setter
    def key_dict(self, obj=None) -> None:
        """
        Class: KeyTextAnalysis Property: key_dict(obj) -> None
        ...
        """
        self.__key_dict = dict(obj).copy

    @property
    def total_matches(self) -> int:
        """
        Class: KeyTextAnalysis Property: total_matches() -> int
        ...
        Returns
        -------
        -> int, value of __total_matches
        """
        return self.__total_matches

    @property
    def total_comparisons(self) -> int:
        """
        Class: KeyTextAnalysis Property: total_comparisons() -> int
        ...
        Returns
        -------
        -> int, value of __total_comparisons
        """
        return self.__total_comparisons


    @property
    def fuzz_ratio(self) -> int:
        """
        Class: KeyTextAnalysis Property: fuzz_ratio() -> int
        ...
        Returns
        -------
        -> int, value of __search_text
        """
        return self.__fuzz_ratio

    @fuzz_ratio.setter
    def fuzz_ratio(self, value=None) -> None:
        """
        Class: KeyTextAnalysis Property: fuzz_ratio(value) -> None
        ...
        """
        self.__fuzz_ratio = value

    @property
    def key_matches(self) -> dict:
        """
        Class: KeyTextAnalysis Property: key_matches() -> dict
        ...
        Returns
        -------
        -> dict, containing the key matches with count totals
        """
        return self.__key_matches

    @key_matches.setter
    def key_matches(self, obj=None) -> None:
        """
        Class: KeyTextAnalysis Property: key_matches(obj) -> None
        ...
        """
        self.__key_matches = dict(obj).copy

    @property
    def key2text_index(self) -> list:
        """
        Class: KeyTextAnalysis Property: key2text_index() -> list
        ...
        Returns
        -------
        -> list, analysis data
        """
        return self.__key2text_index

    def eval_keys2text(self) -> bool:
        """
        Class: KeyTextAnalysis method: eval_keys2text() -> bool
        Evaluates the key dictionary (key_dict) against the text
        dictionary (text_dict), populates the key_matches dictionary
        with the key and the total number of times the key appears
        in the text

        ...

        Methods
        -------
        eval_keys2text() -> bool, True if matches found, otherwise False
            └──:eval_direct(key, item) -> bool
            └──:eval_tokenized(key, item) -> bool
            └──:eval_fuzzy(key, item) -> bool
            └──:sort_dict() -> bool

        Returns
        -------
        -> bool, True if matches found, False otherwise
        """
        if len(self.__text_dict) != 0 and len(self.__key_dict) != 0:
            self.__has_match = False
            self.__key2text_index = []
            for key in self.__key_dict:
                for item in self.__text_dict:
                    self.__total_comparisons += 1
                    if self.__eval_direct(key, item):
                        self.__key2text_index.append([
                            [key, self.__key_dict[key]],
                            [item, self.__text_dict[item]],
                            ["Direct", self.__total_matches, self.__total_comparisons]
                        ])
                    elif self.__eval_tokenized(key, item):
                        self.__key2text_index.append([
                            [key, self.__key_dict[key]],
                            [item, self.__text_dict[item]],
                            ["Tokenized", self.__total_matches, self.__total_comparisons]
                        ])
                    elif self.__eval_fuzz(key, item):
                        self.__key2text_index.append([
                            [key, self.__key_dict[key]],
                            [item, self.__text_dict[item]],
                            ["Fuzzy", self.__total_matches, self.__total_comparisons]
                        ])
            if self.__has_match:
                self.sort_dict()
        return self.__has_match

    def __eval_direct(self, key, item) -> bool:
        """
        Class: KeyTextAnalysis method: __eval_direct(key, item) -> bool
        Evaluates the key dictionary (key_dict) against the text
        dictionary (text_dict) for direct/exact matches

        ...

        Returns
        -------
        -> bool, True if direct match found, False otherwise
        """
        if key in item:
            self.__total_matches += 1
            self.__key_matches[key] += 1
            self.__has_match = True
            return True
        return False

    def __eval_tokenized(self, key, item) -> bool:
        """
        Class: KeyTextAnalysis method: __eval_tokenized(key, item) -> bool
        Evaluates the key dictionary (key_dict) against the text
        dictionary (text_dict) for tokenized/near matches

        ...

        Returns
        -------
        -> bool, True if tokenized match found, False otherwise
        """
        tokenized_key = word_tokenize(key)
        key_string = str(tokenized_key)
        item_tokenized = word_tokenize(item)
        item_string = str(item_tokenized)
        if key_string in item_string:
            self.__total_matches += 1
            self.__key_matches[key] += 1
            self.__has_match = True
            return True
        return False

    def __eval_fuzz(self, key, item) -> bool:
        """
        Class: KeyTextAnalysis method: __eval_fuzz(key: str, item: str) -> bool
        Uses the fuzzywuzzy library implementing:
            *Levenshtein distance =>
                is a string metric for measuring the difference between
                two sequences. Informally, the Levenshtein distance between
                two words is the minimum number of single-character edits

        ...

        Returns
        -------
        -> bool, True if ratio is above __fuzz_ratio, otherwise Fale
        """
        if fuzz.partial_ratio(key, item) >= self.__fuzz_ratio:
            self.__total_matches += 1
            self.__key_matches[key] += 1
            self.__has_match = True
            return True
        return False

    def sort_dict(self) -> bool:
        """
        Class: KeyTextAnalysis method: sort_dict() -> bool
        Sorts the __key_matches (dict) in descending order
            keys:=str, text/lines from file __filename
            items:=int, iterative count, init to 0

        ...

        Returns
        -------
        -> bool, True if sorted, otherwise False
        """
        if self.__has_match:
            self.__key_matches = dict(sorted(
                self.__key_matches.items(),
                key=lambda item: item[1],
                reverse=True))
            return True
        return False

    def echo_key_matches(self) -> bool:
        """
        Class: KeyTextAnalysis method: echo_key_matches() -> bool
        Prints the dictionary of key matches to console

        ...

        Returns
        -------
        -> bool, True if it prints, False otherwise
        """
        if self.__has_match:
            i = 0
            for item in self.__key_matches:
                i += 1
                print("{0}. KEY:= {1}, COUNT:= [ {2} ] ".format(
                    i, item, self.__key_matches[item]))
            return True
        else:
            return False

    def echo_indexed(self) -> bool:
        """
        Class: KeyTextAnalysis method: echo_indexed() -> bool
        Prints the analysis list to console
        ...
            prints to console self.__key2text_index

            [key, self.__key_dict[key]],
                [item, self.__text_dict[item]],
                    [EVAL_TYPE, self.__total_matches, self.__total_comparisons]])

        Returns
        -------
        -> bool, True if it prints, False otherwise
        """
        if len(self.__key2text_index) != 0:
            i = 0
            for li in enumerate(self.__key2text_index):
                i += 1
                print("Index[{0}][{1}]".format(
                    i, "|".join(li)))
            return True
        else:
            return False

    def dump_indexed(self) -> bool:
        """
        Class: ItemizeFile method: dump_indexed() -> bool
        Dumps indexed list to CSV file (indexed_dump.csv)

        ...


        Returns
        -------
        -> bool, True if indexed is dumped, otherwise False
        """
        if len(self.__indexed) > 1:
            joblib.dump(self.__indexed, 'index.csv')
            return True
        else:
            return False

    def dump_matches(self) -> bool:
        """
        Class: ItemizeFile method: dump_matches() -> bool
        Dumps all logs to CSV file (log_dump.csv)

        ...


        Returns
        -------
        -> bool, True if logs are dumped, otherwise False
        """
        if len(self.__log) > 1:
            key_match_list = []
            for key in self.__key_matches:
                key_match_list.append([key, self.__key_matches[key]])
            joblib.dump(key_match_list, 'key_matches_dump.csv')
            return True
        else:
            return False

    def run_all(self) -> bool:
        """
        Class: ItemizeFile method: run_all() -> bool
        Runs all necessary methods to set stage for
        text analysis using the KeyTextAnalysis class as [ta]

        ...


        Returns
        -------
        -> bool, True if no errors, otherwise False
        """
        if self.get_itemized_file() is not None:
            if self.echo_log():
                if self.dump_matches():
                    return True
        return False
