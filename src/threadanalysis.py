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
import threading

from collections import defaultdict

from fuzzywuzzy import fuzz

import nltk
import nltk.data
import nltk.downloader
from nltk.tokenize import word_tokenize

__author__ = "David Rush"
__copyright__ = "Copyright 2022, Rush Solutions, LLC"
__credits__ = ["David Rush", "...", "...", "..."]
__license__ = "MIT"
__version__ = "0.0.5"
__maintainer__ = "David Rush"
__email__ = "davidprush@gmail.com"
__status__ = "Development"


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


class KeyThreader:
    def __init__(self, key: str, text: dict, fuzz: int) -> None:
        self._key = key
        self._text = text.copy()
        self._fuzz = fuzz
        self._key_found = defaultdict(int)
        self._origin = defaultdict(list)
        self._count = 0
        self._line = 0
        self._flag = False
        self._thread = threading.Thread(target=self._needle)

    @property
    def count(self) -> int:
        return self._count

    @property
    def key(self) -> str:
        return self._key

    @property
    def key_found(self) -> dict:
        return self._key_found

    @property
    def origin(self) -> dict:
        return self._origin

    @property
    def line(self) -> int:
        return self._line

    def _needle(self) -> None:
        for item in self._text:
            self._flag = False
            self._line += 1
            kstr = str(word_tokenize(self._key))
            istr = str(word_tokenize(item))
            if self._key in item:
                self._count += 1
                self._flag = True
            elif kstr in istr:
                self._count += 1
                self._flag = True
            elif fuzz.partial_ratio(self._key, item) >= self._fuzz:
                self._count += 1
                self._flag = True
            if self._flag:
                self._origin[self._key] = [
                    "Line:=", self._line,
                    "Text:=", item,
                    "Count:=", self._count,
                    "Key:=", self._key
                ]
        if self._count > 0:
            self._key_found[self._key] = self._count
            self._flag = True

    def start(self) -> None:
        self._thread.start()

    def join(self) -> None:
        self._thread.join()

    def is_alive(self) -> bool:
        return self._thread.is_alive()


class KeyTextAnalysis:
    """
    Class: KeyTextAnalysis
        └──obj = KeyTextAnalysis(text_dict: dict, key_dict: dict,
                                [fuzz_ratio]: int, optional) -> obj

    ...

    Attributes
    ----------
    _text_dict:=dict, text_dict parameter passed at instantiation
    _key_dict:=dict, key_dict parameter passed at instantiation
    _fuzz_ratio:=int, init to fuzz_ratio=99, see not below
    _keys_found:=dict, key=>[unique text]: str, item=>[match count], int
    _keys2text_index:=list, metadata; incrementers; origin text
    _total_keys_found:=int, init to 0, total number of key matches
    _total_comparisons:=int, init to 0, total number of key to text evaluations
    _has_key:=bool, init to False

    Methods
    -------
    keys2text_find() -> bool:Evaluates the key dictionary (key_dict)
        against the text dictionary (text_dict), populates the keys_found
        dictionary with the key and the total number of times the key appears
        in the text
    _sort_dict() -> bool: Sorts the _keys_found (dict) in descending order
    echo_keys_found() -> bool: Prints the dictionary of key matches to console
    echo_keys2text_indexed() -> bool: Prints the list of analysis comparisons to console
    dump_keys2text_index() -> bool: Dumps indexed list to file indexed_list_dump.z
    dump_keys_found() -> bool: Dumps matches to file key_match_dump.z
    run_keys2text_all() -> bool:
    _eval_direct_match(key, item) -> bool:
    _eval_tokenized_match(skey, item) -> bool:
    _eval_fuzzy_match(key, item) -> bool:

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
        (Class:KeyTextAnalysis) => Method:__init__ to instantiate class attributes
            └──obj = KeyTextAnalysis(text_dict: dict, key_dict: dict,
                                    [fuzz_ratio]: int, optional) -> obj

        ...

        Attributes
        ----------
        _text_dict:=dict, text_dict parameter passed at instantiation
        _key_dict:=dict, key_dict parameter passed at instantiation
        _fuzz_ratio:=int, init to fuzz_ratio=99, see not below
        _keys_found:=dict, key=>[unique text]: str, item=>[match count], int
        _keys2text_index:=list, metadata; incrementers; origin text
        _total_keys_found:=int, init to 0, total number of key matches
        _total_comparisons:=int, init to 0, total number of key to text evaluations
        _has_key:=bool, init to False

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
        self._text_dict = text_dict
        self._key_dict = key_dict
        self._fuzz_ratio = fuzz_ratio
        self._keys_found = defaultdict(int)
        self._keys2text_index = defaultdict(list)
        self._total_keys_found = 0
        self._total_comparisons = 0
        self._has_key = False

    def __repr__(self) -> str:
        return f'False{{0}}, _text_dict={{1}}, _key_dict={{2}}, _fuzz_ratio={{3}}, \
            _keys_found={{4}}, =_keys2text_index{{5}}, _total_keys_found={{6}}, \
            _total_comparisons={{7}}, _has_key={{8}}, _sent_detect={{9}}'.format(
            {type(self).__name__}, self._text_dict, self._key_dict,
            self._fuzz_ratio, self._keys_found, self._keys2text_index,
            self._total_keys_found, self._total_comparisons, self._has_key,
            self._sent_detect)

    def __eq__(self, obj) -> bool:
        if not isinstance(obj, KeyTextAnalysis):
            return NotImplemented
        return self.__self__ is obj.__self__

    def __hash__(self) -> hash:
        return hash(tuple(self))

    @property
    def text_dict(self) -> dict:
        """
        (Class:KeyTextAnalysis) => Property: text_dict() -> dict
        ...
        Returns
        -------
        -> dict, text dictionary
        """
        return self._text_dict

    @text_dict.setter
    def text_dict(self, obj=None) -> dict:
        """
        (Class:KeyTextAnalysis) => Property: key_dict(obj) -> dict
        ...
        """
        self._text_dict = dict(obj).copy

    @property
    def key_dict(self) -> dict:
        """
        (Class:KeyTextAnalysis) => Property: key_dict() -> dict
        ...
        Returns
        -------
        -> dict, text keys dictionary
        """
        return self._key_dict

    @key_dict.setter
    def key_dict(self, obj=None) -> None:
        """
        (Class:KeyTextAnalysis) => Property: key_dict(obj: dict) -> None
        ...
        """
        self._key_dict = dict(obj).copy

    @property
    def total_keys_found(self) -> int:
        """
        (Class:KeyTextAnalysis) => Property: total_keys_founds() -> int
        ...
        Returns
        -------
        -> int, value of _total_keys_found
        """
        return self._total_keys_found

    @property
    def total_comparisons(self) -> int:
        """
        (Class:KeyTextAnalysis) => Property: total_comparisons() -> int
        ...
        Returns
        -------
        -> int, value of _total_comparisons
        """
        return self._total_comparisons

    @property
    def fuzz_ratio(self) -> int:
        """
        (Class:KeyTextAnalysis) => Property: fuzz_ratio() -> int
        ...
        Returns
        -------
        -> int, value of __search_text
        """
        return self._fuzz_ratio

    @fuzz_ratio.setter
    def fuzz_ratio(self, value=None) -> None:
        """
        (Class:KeyTextAnalysis) => Property: fuzz_ratio(value: int) -> None
        ...
        """
        self._fuzz_ratio = value

    @property
    def keys_found(self) -> dict:
        """
        (Class:KeyTextAnalysis) => Property: keys_found() -> dict
        ...
        Returns
        -------
        -> dict, containing the key matches with count totals
        """
        return self._keys_found

    @keys_found.setter
    def keys_found(self, obj=None) -> None:
        """
        (Class:KeyTextAnalysis) => Property: keys_found(obj: dict) -> None
        ...
        """
        self._keys_found = dict(obj).copy

    @property
    def keys2text_index(self) -> dict:
        """
        (Class:KeyTextAnalysis) => Property: keys2text_index() -> list
        ...
        Returns
        -------
        -> list, metadata; incrementers; origin text
        """
        return self._keys2text_index

    def keys2text_find(self) -> bool:
        """
        (Class:KeyTextAnalysis) => Method: keys2text_find() -> bool
        Evaluates the key dictionary (key_dict) against the text
        dictionary (text_dict), populates the keys_found dictionary
        accordingly with the key and the total number of times
        the key appears in the text

        ...

        Methods
        -------
        keys2text_find() -> bool, True if matches found, otherwise False
            └──:_eval_direct_match(key, item) -> bool
                    └──:_eval_tokenized_match(key, item) -> bool
                            └──:_eval_fuzzy_matchy(key, item) -> bool
                                    └──:_sort_dict() -> bool

        Returns
        -------
        -> bool, True if matches found, False otherwise
        """
        if len(self._text_dict) != 0 and len(self._key_dict) != 0:
            self._has_key = False
            self._keys2text_index = defaultdict(list)
            self._keys_found = defaultdict(int)
            key_threader = {}
            i = 0
            for key in self._key_dict:
                key_threader[key] = KeyThreader(
                    key,
                    self._text_dict,
                    self._fuzz_ratio
                )
                key_threader[key].start()
                i += 1
                print("Total threads {0}".format(threading.active_count()))
                # if threading.active_count() > MAX_THREADS:
                #     for key in key_threader:
                #         key_threader[key].join()
            for key in key_threader:
                if key_threader[key].is_alive():
                    key_threader[key].join()
            for key in key_threader:
                self._keys_found = \
                    self._keys_found | key_threader[key].key_found
                self._keys2text_index = \
                    self._keys2text_index | key_threader[key].key_found
            if len(self._keys_found) != 0:
                self._sort_dict()
                self._has_key = True
        return self._has_key

    def _eval_direct_match(self, key, item) -> bool:
        """
        (Class:KeyTextAnalysis) => Method: _eval_direct_match(key, item) -> bool
        Evaluates the key dictionary (key_dict) against the text
        dictionary (text_dict) for direct/exact matches

        ...

        Returns
        -------
        -> bool, True if direct match found, False otherwise
        """
        if key in item:
            self._total_keys_found += 1
            self._keys_found[key] += 1
            self._has_key = True
            return True
        return False

    def _eval_tokenized_match(self, key, item) -> bool:
        """
        (Class:KeyTextAnalysis) => Method: _eval_tokenized_match(key, item) -> bool
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
            self._total_keys_found += 1
            self._keys_found[key] += 1
            self._has_key = True
            return True
        return False

    def _eval_fuzzy_match(self, key, item) -> bool:
        """
        (Class:KeyTextAnalysis) => Method: _eval_fuzzy_match(key: str, item: str) -> bool
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
        if fuzz.partial_ratio(key, item) >= self._fuzz_ratio:
            self._total_keys_found += 1
            self._keys_found[key] += 1
            self._has_key = True
            return True
        return False

    def _sort_dict(self) -> bool:
        """
        (Class:KeyTextAnalysis) => Method: _sort_dict() -> bool
        Sorts the keys_found (dict) in descending order
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
        if self._has_key:
            self._keys_found = dict(sorted(
                self._keys_found.items(),
                key=lambda item: item[1],
                reverse=True))
            return True
        return False

    def echo_keys_found(self) -> bool:
        """
        (Class:KeyTextAnalysis) => Method: echo_keys_found() -> bool
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
        if self._has_key:
            i = 0
            for item in self._keys_found:
                i += 1
                print("{0}.{1}:=[{2}]".format(
                    i, item, self._keys_found[item]))
            return True
        else:
            return False

    def echo_keys2text_indexed(self) -> bool:
        """
        (Class:KeyTextAnalysis) => Method: echo_keys2text_indexed() -> bool
        Prints the analysis list to console

        ...

            prints to console _keys2text_index:

        [key, self._key_dict[key]],
            [item, self._text_dict[item]],
                [EVAL_TYPE, self._total_keys_found, self._total_comparisons]])

        Returns
        -------
        -> bool, True if it prints, False otherwise
        """
        if len(self._keys2text_index) != 0:
            for i, li in enumerate(self._keys2text_index):
                print("Index[{0}][{1}]".format(
                    i, str(li)))
            return True
        else:
            return False

    def dump_keys2text_index(self) -> bool:
        """
        (Class:KeyTextAnalysis) => Method: dump_keys2text_index() -> bool
        Dumps indexed list data to csv file (indexed_dump.z)

        ...

        Returns
        -------
        -> bool, True if indexed is not equal to 0, otherwise False
        """
        if len(self._keys2text_index) != 0:
            joblib.dump(self._keys2text_index, 'index_dump.z')
            return True
        else:
            return False

    def dump_keys_found(self) -> bool:
        """
        (Class:KeyTextAnalysis) => Method: dump_keys_found() -> bool
        Dumps all logs to CSV file (keys_found_dump.z)

        ...

        Returns
        -------
        -> bool, True if logs are dumped, otherwise False
        """
        if len(self._keys_found) != 1:
            key_match_list = []
            for key in self._keys_found:
                key_match_list.append([key, self._keys_found[key]])
            joblib.dump(key_match_list, 'keys_found_dump.z')
            return True
        else:
            return False

    def run_keys2text_all(self) -> bool:
        """
        (Class:KeyTextAnalysis) => Method: run_keys2text_all() -> bool
        Runs all necessary methods to complete matching analysis
        ...

           keys2text_find():
                └──echo_keys2text_indexed():
                    └──echo_keys_found():
                        └──dump_keys_found():
                            └──dump_keys2text_index():

        Returns
        -------
        -> bool, True if all above tasks complete, otherwise False
        """
        if self.keys2text_find():
            if self.echo_keys2text_indexed():
                if self.echo_keys_found():
                    if self.dump_keys_found():
                        if self.dump_keys2text_index():
                            return True
        return False
