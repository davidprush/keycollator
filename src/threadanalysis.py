# -*- coding: utf-8 -*-
"""
Copyright (C) 2022 Rush Solutions, LLC
Author: David Rush <davidprush@gmail.com>
License: MIT
    Class: KeyTextAnalysis
        └──obj = KeyTextAnalysis(text_dict: dict, key_dict: dict,
                                [fuzz_ratio]: int, optional) -> obj

"""
import sys
import joblib
from threading import Thread

from collections import defaultdict

from fuzzywuzzy import fuzz

import nltk
import nltk.data
import nltk.downloader
from nltk.tokenize import word_tokenize
from tqdm import tqdm

import constants as const


"""
Module Requires: "punkt" for nltk
CLI command: python3 -m nltk.downloader punkt
"""
try:
    dler = nltk.downloader.Downloader()
    if dler._status_cache['punkt'] != 'installed':
        dler._update_index()
        dler.download('punkt')
except Exception as ex:
    ex = ex if ex else ''
    pass  # print(ex)  # replace with CustomLogger

__author__ = "David Rush"
__copyright__ = "Copyright 2022, Rush Solutions, LLC"
__credits__ = ["David Rush", "...", "...", "..."]
__license__ = "MIT"
__version__ = "0.0.5"
__maintainer__ = "David Rush"
__email__ = "davidprush@gmail.com"
__status__ = "Development"


class KeyThreader(Thread):
    """
    Class: KeyThreader
        └──obj = KeyThreader(self, key: str, text: dict, fuzz: int) -> None:

    ...

    Attributes
    ----------
    _key:=str,
    _text:=dict,
    _fuzz:=int
    _key_found:=dict,
    _origin:=dict,
    _count:=int,
    _line:=int,
    _flag:=bool,

    Methods
    -------
    run() -> None:

    Parameters
    ----------
    key:=str,
    text:=dict,
    fuzz:=int, ratio for fuzzy-matching
        Uses the fuzzywuzzy library that implements:
            *Levenshtein distance =>
                is a string metric for measuring the difference between
                two sequences. Informally, the Levenshtein distance between
                two words is the minimum number of single-character edits
    """

    def __init__(self, key: str, text: dict, fuzz: int) -> None:
        """
        Class: KeyThreader
            └──obj = KeyThreader(self, key: str, text: dict, fuzz: int) -> None:

        ...

        Attributes
        ----------
        _key:=str,
        _text:=dict,
        _fuzz:=int
        _key_found:=dict,
        _origin:=dict,
        _count:=int,
        _line:=int,
        _flag:=bool,

        Parameters
        ----------
        key:=str,
        text:=dict,
        fuzz:=int, ratio for fuzzy-matching
            Uses the fuzzywuzzy library that implements:
                *Levenshtein distance =>
                    is a string metric for measuring the difference between
                    two sequences. Informally, the Levenshtein distance between
                    two words is the minimum number of single-character edits
        """
        Thread.__init__(self)
        self._key = key
        self._text = text.copy()
        self._fuzz = fuzz
        self._key_found = defaultdict(int)
        self._origin = defaultdict(list)
        self._count = 0
        self._line = 0
        self._flag = False

    @property
    def count(self) -> int:
        """
        KeyThreader => Property: count() -> int
        """
        return self._count

    @property
    def key(self) -> str:
        """
        KeyThreader => Property: key() -> str
        """
        return self._key

    @property
    def key_found(self) -> dict:
        """
        KeyThreader => Property: key_found() -> dict
        """
        return self._key_found

    @property
    def origin(self) -> dict:
        """
        KeyThreader => Property: origin() -> dict
        """
        return self._origin

    @property
    def line(self) -> int:
        """
        KeyThreader => Property: line() -> int
        """
        return self._line

    def run(self) -> None:
        """
        KeyThreader => Property: line() -> None
        """
        for item in self._text:
            self._flag = False
            self._line += 1
            kstr = str([s for s in word_tokenize(self._key) if len(s) > 3])
            istr = str([s for s in word_tokenize(item) if len(s) > 3])
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
    _sort_keys_found() -> bool: Sorts the _keys_found (dict) in descending order
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
        fuzz_ratio=99
    ) -> None:
        """
        (Class:KeyTextAnalysis) => Method:__init__ to instantiate class attributes
            └──obj = KeyTextAnalysis(text_dict: dict, key_dict: dict,
                                    [fuzz_ratio]: int, optional) -> obj

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
        self._total_threads = 0

    def __repr__(self) -> str:
        return f'False{{0}}, _text_dict={{1}}, _key_dict={{2}}, _fuzz_ratio={{3}}, \
            _keys_found={{4}}, =_keys2text_index{{5}}, _total_keys_found={{6}}, \
            _total_comparisons={{7}}, _has_key={{8}}, _total_threads={{9}}'.format(
            {type(self).__name__}, self._text_dict, self._key_dict,
            self._fuzz_ratio, self._keys_found, self._keys2text_index,
            self._total_keys_found, self._total_comparisons, self._has_key,
            self._total_threads)

    def __eq__(self, obj) -> bool:
        if not isinstance(obj, KeyTextAnalysis):
            return NotImplemented
        return self.__self__ is obj.__self__

    def __hash__(self) -> hash:
        return hash(tuple(self))

    @property
    def text_dict(self) -> dict:
        """
        KeyTextAnalysis => Property: text_dict() -> dict
        -> dict, text dictionary
        """
        return self._text_dict

    @text_dict.setter
    def text_dict(self, obj=None) -> dict:
        """
        KeyTextAnalysis => Property: key_dict(obj) -> dict
        """
        self._text_dict = dict(obj).copy

    @property
    def key_dict(self) -> dict:
        """
        KeyTextAnalysis => Property: key_dict() -> dict
        -> dict, text keys dictionary
        """
        return self._key_dict

    @key_dict.setter
    def key_dict(self, obj=None) -> None:
        """
        KeyTextAnalysis => Property: key_dict(obj: dict) -> None
        """
        self._key_dict = dict(obj).copy

    @property
    def total_keys_found(self) -> int:
        """
        KeyTextAnalysis => Property: total_keys_founds() -> int
        -> int, value of _total_keys_found
        """
        return self._total_keys_found

    @property
    def total_comparisons(self) -> int:
        """
        KeyTextAnalysis => Property: total_comparisons() -> int
        -> int, value of _total_comparisons
        """
        return self._total_comparisons

    @property
    def fuzz_ratio(self) -> int:
        """
        KeyTextAnalysis => Property: fuzz_ratio() -> int
        -> int, value of __search_text
        """
        return self._fuzz_ratio

    @fuzz_ratio.setter
    def fuzz_ratio(self, value=None) -> None:
        """
        KeyTextAnalysis => Property: fuzz_ratio(value: int) -> None
        """
        self._fuzz_ratio = value

    @property
    def keys_found(self) -> dict:
        """
        KeyTextAnalysis => Property: keys_found() -> dict
        -> dict, containing the key matches with count totals
        """
        return self._keys_found

    @keys_found.setter
    def keys_found(self, obj=None) -> None:
        """
        KeyTextAnalysis => Property: keys_found(obj: dict) -> None
        """
        self._keys_found = dict(obj).copy

    @property
    def keys2text_index(self) -> dict:
        """
        KeyTextAnalysis => Property: keys2text_index() -> list
        -> list, metadata; incrementers; origin text
        """
        return self._keys2text_index

    def keys2text_find(self) -> bool:
        """
        KeyTextAnalysis => Method: keys2text_find() -> bool
        Evaluates the key dictionary (key_dict) against the text
        dictionary (text_dict), populates the keys_found dictionary
        accordingly with the key and the total number of times
        the key appears in the text


        Methods
        -------
        keys2text_find() -> bool, True if matches found, otherwise False
            └──:_eval_direct_match(key, item) -> bool
                    └──:_eval_tokenized_match(key, item) -> bool
                            └──:_eval_fuzzy_matchy(key, item) -> bool
                                    └──:_sort_keys_found() -> bool

        Returns
        -------
        -> bool, True if matches found, False otherwise
        """
        if len(self._text_dict) != 0 and len(self._key_dict) != 0:
            self._has_key = False
            self._keys2text_index = defaultdict(list)
            self._keys_found = defaultdict(int)
            key_threader = {}
            print("Analyzing text for keys...")
            pbar = tqdm(total=(len(self._key_dict)))
            sys.stdout.flush()
            for key in self._key_dict:
                key_threader[key] = KeyThreader(
                    key,
                    self._text_dict,
                    self._fuzz_ratio
                )
                key_threader[key].start()
                self._total_threads += 1
                pbar.update(1)
                sys.stdout.flush()
            for key in key_threader:
                key_threader[key].join()
                self._keys_found = \
                    self._keys_found | key_threader[key].key_found
                self._keys2text_index = \
                    self._keys2text_index | key_threader[key].key_found
            pbar.close()
            if len(self._keys_found) != 0:
                self._sort_keys_found()
                self._has_key = True
        return self._has_key

    def _eval_direct_match(self, key, item) -> bool:
        """
        KeyTextAnalysis => Method: _eval_direct_match(key, item) -> bool
        Evaluates the key dictionary (key_dict) against the text
        dictionary (text_dict) for direct/exact matches

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
        KeyTextAnalysis => Method: _eval_tokenized_match(key, item) -> bool
        Evaluates the key dictionary (key_dict) against the text
        dictionary (text_dict) for tokenized (very near matches)

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
        KeyTextAnalysis => Method: _eval_fuzzy_match(key: str, item: str) -> bool
        Uses the fuzzywuzzy library implementing:
            *Levenshtein distance =>
                is a string metric for measuring the difference between
                two sequences. Informally, the Levenshtein distance between
                two words is the minimum number of single-character edits

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

    def _sort_keys_found(self) -> bool:
        """
        KeyTextAnalysis => Method: _sort_keys_found() -> bool
        Sorts the keys_found (dict) in descending order
        keys:=str, unique text (lines) from file filename
        items:=int, iterative count, init to 0, increments
        on every match added to the dictionary

        post-condition:=First item/key (unique str) has the greatest
        number of matches found in the text dictionary (text_dict)

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
        KeyTextAnalysis => Method: echo_keys_found() -> bool
        Prints the dictionary of key matches to console
        -> bool, True if has_matches, False otherwise
        """
        if self._sort_keys_found():
            col_dict = defaultdict(list)
            for i, item in enumerate(self._keys_found):
                temp_str = "{0}.{1}".format(i + 1, item)
                col_dict[
                    i // (len(self._keys_found) // 4)
                ].append("{0}[{1}]".format(
                    ((temp_str + const.FSPC[0:(18 - len(temp_str))])
                        if len(temp_str) <= 18
                        else "{0}*".format(temp_str[0:17])),
                    self._keys_found[item]))
            rows = max([
                len(col_dict[0]),
                len(col_dict[1]),
                len(col_dict[2]),
                len(col_dict[3])])
            for row in range(rows):
                print(
                    col_dict[0][row] if row < len(col_dict[0]) else "",
                    const.TAB,
                    col_dict[1][row] if row < len(col_dict[1]) else "",
                    const.TAB,
                    col_dict[2][row] if row < len(col_dict[2]) else "",
                    const.TAB,
                    col_dict[3][row] if row < len(col_dict[3]) else "")
            print(
                "*denotes truncated text [Analysis completed {0} threads]".format(
                    self._total_threads))
            return True
        else:
            return False

    def echo_keys2text_indexed(self) -> bool:
        """
        KeyTextAnalysis => Method: echo_keys2text_indexed() -> bool
        Prints the analysis list to console

            prints to console _keys2text_index:

        [key, self._key_dict[key]],
            [item, self._text_dict[item]],
                [EVAL_TYPE, self._total_keys_found, self._total_comparisons]])

        Returns
        -------
        -> bool, True if it prints, False otherwise
        """
        if len(self._keys2text_index) != 0:
            for item in self._keys2text_index:
                print("[Index:{0}][{1}]".format(
                    str(item),
                    str(self._keys2text_index[item])))
            return True
        else:
            return False

    def dump_keys2text_index(self) -> bool:
        """
        KeyTextAnalysis => Method: dump_keys2text_index() -> bool
        Dumps indexed list data to csv file (indexed_dump.z)

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
        KeyTextAnalysis => Method: dump_keys_found() -> bool
        Dumps all logs to CSV file (keys_found_dump.z)

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
        KeyTextAnalysis => Method: run_keys2text_all() -> bool
        Runs all necessary methods to complete matching analysis
        keys2text_find():
            └──echo_keys_found():
                └──dump_keys_found():
                    └──dump_keys2text_index():

        Returns
        -------
        -> bool, True if all above tasks complete, otherwise False
        """
        if self.keys2text_find():
            if self.echo_keys_found():
                if self.dump_keys_found():
                    if self.dump_keys2text_index():
                        return True
        return False
