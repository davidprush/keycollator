# -*- coding: utf-8 -*-
"""
Copyright (C) 2022 Rush Solutions, LLC
Author: David Rush <davidprush@gmail.com>
License: MIT
    Class: KeyTextAnalysis
        └──obj = KeyTextAnalysis(text_dict: dict, key_dict: dict,
                                [fuzz_ratio]: int, optional) -> obj

"""
import joblib

from collections import defaultdict

from fuzzywuzzy import fuzz

import nltk
import nltk.data
import nltk.downloader
from nltk.tokenize import word_tokenize
# from nltk.corpus import wordnet as wn

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
        └──obj = KeyTextAnalysis(text_dict: dict, key_dict: dict,
                                [fuzz_ratio]: int, optional) -> obj

    ...

    Attributes
    ----------
    __text_dict:=dict, text_dict parameter passed at instantiation
    __key_dict:=dict, key_dict parameter passed at instantiation
    __fuzz_ratio:=int, init to fuzz_ratio=99, see not below
    __key_matches:=dict, key=>[unique text]: str, item=>[match count], int
    __key2text_index:=list, metadata; incrementers; origin text
    __total_matches:=int, init to 0, total number of key matches
    __total_comparisons:=int, init to 0, total number of key to text evaluations
    __has_match:=bool, init to False

    Methods
    -------
    eval_keys2text() -> bool:Evaluates the key dictionary (key_dict)
        against the text dictionary (text_dict), populates the key_matches
        dictionary with the key and the total number of times the key appears
        in the text
    __sort_dict() -> bool: Sorts the __key_matches (dict) in descending order
    echo_matches() -> bool: Prints the dictionary of key matches to console
    echo_indexed() -> bool: Prints the list of analysis comparisons to console
    dump_indexed() -> bool: Dumps indexed list to file indexed_list_dump.csv
    dump_matches() -> bool: Dumps matches to file key_match_dump.csv
    run_match_analysis() -> bool:
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
        stopwords=None,
        fuzz_ratio=99
    ) -> None:
        """
        Class: KeyTextAnalysis Method:__init__ to instantiate class attributes
            └──obj = KeyTextAnalysis(text_dict: dict, key_dict: dict,
                                    [fuzz_ratio]: int, optional) -> obj

        ...

        Attributes
        ----------
        __text_dict:=dict, text_dict parameter passed at instantiation
        __key_dict:=dict, key_dict parameter passed at instantiation
        __fuzz_ratio:=int, init to fuzz_ratio=99, see not below
        __key_matches:=dict, key=>[unique text]: str, item=>[match count], int
        __key2text_index:=list, metadata; incrementers; origin text
        __total_matches:=int, init to 0, total number of key matches
        __total_comparisons:=int, init to 0, total number of key to text evaluations
        __has_match:=bool, init to False

        Parameters
        ----------
        text_dict:=dict, text_dict parameter passed at instantiation
        key_dict:=dict, key_dict parameter passed at instantiation
        stopwords:=list, stopwords parameter passed at instantiation, upon init
                        the words are tokenized to eliminate all approximates
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

    def __repr__(self) -> str:
        return f'False{{0}}, __text_dict={{1}}, __key_dict={{2}}, __fuzz_ratio={{3}}, \
            __key_matches={{4}}, =__key2text_index{{5}}, __total_matches={{6}}, \
            __total_comparisons={{7}}, __has_match={{8}}, __sent_detect={{9}}'.format(
            {type(self).__name__}, self.__text_dict, self.__key_dict,
            self.__fuzz_ratio, self.__key_matches, self.__key2text_index,
            self.__total_matches, self.__total_comparisons, self.__has_match,
            self.__sent_detect)

    def __eq__(self, obj) -> bool:
        if not isinstance(obj, KeyTextAnalysis):
            return NotImplemented
        return self.__self__ is obj.__self__

    def __hash__(self) -> hash:
        return hash(tuple(self))

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
        Class: KeyTextAnalysis Property: key_dict(obj: dict) -> None
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
        Class: KeyTextAnalysis Property: fuzz_ratio(value: int) -> None
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
        Class: KeyTextAnalysis Property: key_matches(obj: dict) -> None
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
        -> list, metadata; incrementers; origin text
        """
        return self.__key2text_index

    def eval_keys2text(self) -> bool:
        """
        Class: KeyTextAnalysis Method: eval_keys2text() -> bool
        Evaluates the key dictionary (key_dict) against the text
        dictionary (text_dict), populates the key_matches dictionary
        accordingly with the key and the total number of times
        the key appears in the text

        ...

        Methods
        -------
        eval_keys2text() -> bool, True if matches found, otherwise False
            └──:__eval_direct(key, item) -> bool
                    └──:__eval_tokenized(key, item) -> bool
                            └──:__eval_fuzzy(key, item) -> bool
                                    └──:__sort_dict() -> bool

        Returns
        -------
        -> bool, True if matches found, False otherwise
        """
        if len(self.__text_dict) != 0 and len(self.__key_dict) != 0:
            # reset flag for matches
            self.__has_match = False
            # init empty index list
            self.__key2text_index = []
            for key in self.__key_dict:
                for item in self.__text_dict:
                    self.__total_comparisons += 1
                    if self.__eval_direct(key, item):
                        self.__key2text_index.append([
                            [key, self.__key_dict[key]],
                            [item, self.__text_dict[item]],
                            ["Direct", self.__total_matches,
                                self.__total_comparisons]
                        ])
                    elif self.__eval_tokenized(key, item):
                        self.__key2text_index.append([
                            [key, self.__key_dict[key]],
                            [item, self.__text_dict[item]],
                            ["Tokenized", self.__total_matches,
                                self.__total_comparisons]
                        ])
                    elif self.__eval_fuzz(key, item):
                        self.__key2text_index.append([
                            [key, self.__key_dict[key]],
                            [item, self.__text_dict[item]],
                            ["Fuzzy", self.__total_matches,
                                self.__total_comparisons]
                        ])
            if self.__has_match:
                self.__sort_dict()
        return self.__has_match

    def __eval_direct(self, key, item) -> bool:
        """
        Class: KeyTextAnalysis Method: __eval_direct(key, item) -> bool
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
        Class: KeyTextAnalysis Method: __eval_tokenized(key, item) -> bool
        Evaluates the key dictionary (key_dict) against the text
        dictionary (text_dict) for tokenized (very near matches)

        ...

        Returns
        -------
        -> bool, True if tokenized match found, False otherwise
        """
        key_string = str(word_tokenize(key))
        item_string = str(word_tokenize(item))
        if key_string in item_string:
            self.__total_matches += 1
            self.__key_matches[key] += 1
            self.__has_match = True
            return True
        return False

    def __eval_fuzz(self, key, item) -> bool:
        """
        Class: KeyTextAnalysis Method: __eval_fuzz(key: str, item: str) -> bool
        Uses the fuzzywuzzy library implementing:
            *Levenshtein distance =>
                is a string metric for measuring the difference between
                two sequences. Informally, the Levenshtein distance between
                two words is the minimum number of single-character edits

        ...

        Returns
        -------
        -> bool, True if ratio is >= fuzz_ratio, otherwise Fale
        """
        if fuzz.partial_ratio(key, item) >= self.__fuzz_ratio:
            self.__total_matches += 1
            self.__key_matches[key] += 1
            self.__has_match = True
            return True
        return False

    def __sort_dict(self) -> bool:
        """
        Class: KeyTextAnalysis Method: __sort_dict() -> bool
        Sorts the key_matches (dict) in descending order
        keys:=str, unique text (lines) from file filename
        items:=int, iterative count, init to 0, increments
        on every match added to the dictionary

        post-condition:=First item/key (unique str) has the greatest
        number of matches found in the text dictionary (text_dict)

        ...

        Returns
        -------
        -> bool, True if has matches, otherwise False
        """
        if self.__has_match:
            self.__key_matches = dict(sorted(
                self.__key_matches.items(),
                key=lambda item: item[1],
                reverse=True))
            return True
        return False

    def echo_matches(self) -> bool:
        """
        Class: KeyTextAnalysis Method: echo_matches() -> bool
        Prints the dictionary of key matches to console in the
        following format:

        No.     KEY                         MATCH TOTAL
        ---     ---                         -----------
        1.      KEY:="A unique string",     COUNT:=[ 17 ]

        ...

        Returns
        -------
        -> bool, True if has_matches, False otherwise
        """
        if self.__has_match:
            i = 0
            for item in self.__key_matches:
                i += 1
                print("{0}. \t KEY:= {1}, \t\t COUNT:=[ {2} ] ".format(
                    i, item, self.__key_matches[item]))
            return True
        else:
            return False

    def echo_indexed(self) -> bool:
        """
        Class: KeyTextAnalysis Method: echo_indexed() -> bool
        Prints the analysis list to console

        ...

            prints to console __key2text_index:

        [key, self.__key_dict[key]],
            [item, self.__text_dict[item]],
                [EVAL_TYPE, self.__total_matches, self.__total_comparisons]])

        Returns
        -------
        -> bool, True if it prints, False otherwise
        """
        if len(self.__key2text_index) != 0:
            for i, li in enumerate(self.__key2text_index):
                print("Index[{0}][{1}]".format(
                    i, "|".join(li)))
            return True
        else:
            return False

    def dump_indexed(self) -> bool:
        """
        Class: KeyTextAnalysis Method: dump_indexed() -> bool
        Dumps indexed list data to csv file (indexed_dump.csv)

        ...

        Returns
        -------
        -> bool, True if indexed is > 1, otherwise False
        """
        if len(self.__indexed) > 1:
            joblib.dump(self.__indexed, 'index_dump.csv')
            return True
        else:
            return False

    def dump_matches(self) -> bool:
        """
        Class: KeyTextAnalysis Method: dump_matches() -> bool
        Dumps all logs to CSV file (key_matches_dump.csv)

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

    def run_match_analysis(self) -> bool:
        """
        Class: KeyTextAnalysis Method: run_match_analysis() -> bool
        Runs all necessary methods to complete matching analysis
        ...

           eval_keys2text():
                └──echo_indexed():
                    └──echo_matches():
                        └──dump_matches():
                            └──dump_indexed():

        Returns
        -------
        -> bool, True if all above tasks complete, otherwise False
        """
        if self.eval_keys2text():
            if self.echo_indexed():
                if self.echo_matches():
                    if self.dump_matches():
                        if self.dump_indexed():
                            return True
        return False
