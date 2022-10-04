# -*- coding: utf-8 -*-
"""
extractfile.py
Copyright (C) 2022 Rush Solutions, LLC
Author: David Rush <davidprush@gmail.com>
License: MIT

 ...

Text File
    └──> Extracts Raw Text
            └──> Sanitizes text
                (removes punctionation/end-lines/converts to all lower case)
                    └──> Extracts Raw Text

This module provides a class ItemizeFileData (filename, [stopwords]) which stores
data from the file using the following methods:

 ...

*get_raw(self) -> list
    =>Opens the file (filename) and creates a list containing items for each line of text
*sanitize(self, text=None) -> str
    =>If text is passed to method it will be sanitized usingthe private method
*_sanitize_text(text) -> str, elseit cycles through each key in _dict and
*runs_sanitize_text(text) on each key of text and updatesaccordingly
*pop_stop_words(self, text=None) -> str
    =>Removes stop_words from text: str
*file_exists(self, file_name=None) -> bool
    =>Verifies file_name (filename) exists
*itemize_file(self) -> dict
    =>Searches text file (self._filename) for unique lines oftext, sanitizes each
*line of text, adds values to the listed attributes
*_sort_dict(self) -> bool
    =>Sorts _dict (dict) by item count (integer)
"""
import os.path
import string
import threading

from collections import defaultdict

import nltk
import nltk.data
from nltk.corpus import stopwords as stpw
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from consts import LINE, STOP_WORDS

__author__ = "David Rush"
__copyright__ = "Copyright 2022, Rush Solutions, LLC"
__credits__ = ["David Rush", "...", "...", "..."]
__license__ = "MIT"
__version__ = "0.0.5"
__maintainer__ = "David Rush"
__email__ = "davidprush@gmail.com"
__status__ = "Development"


class ItemizeFileData:
    """
    (Class:ItemizeFileData) =>

    obj = Itemizefile(filename: str, [stopwords]: list, optional)

    ...

    Attributes
    ----------
    _filename:=str, set to optional file_name parameter
    _file_exists:=bool, True if _filename exists, false otherwise
    _raw:=list, raw list of text from the file
    _stopwords:=list, words to be removed from the text
    _dict:=dict, init to defaultdict(int),
    _origin:= init to defaultdict(int),
    _unique_item_count:=int, total num. of unique items added to _dict
    _file_item_count:=int, total num. of items (lines) of text from _filename

    Methods
    -------
    get_raw() -> list =>Opens the file (filename) and creates a list containing
                    unique items for each line of text
    sanitize(text=None) -> str =>If text is passed to method it will be sanitized
                    usingthe private method _sanitize_text(text) -> str, elseit
                    cycles through each key in _dict and runs_sanitize_text(text)
                    on each key of text and updatesaccordingly
    pop_stop_words(text=None) -> str =>Removes stop_words from text: str
    file_exists(file_name=None) -> bool =>Verifies file_name (filename) exists
    itemize_file() -> dict =>Searches text file (self._filename) for
                    unique lines oftext, sanitizes each line of text, adds values to
                    the listed attributes
    _sort_dict() -> bool =>Sorts _dict (dict) by item count (integer)

    Parameters
    ----------
    file_name:=str, required filename of text to be used by this instance
    stopwords=list, stop words to be removed from text, default=consts.STOP_WORDS
    """

    def __init__(
        self,
        file_name,
        stop_words=[]
    ) -> None:
        """
        (Class:ItemizeFileData) => Method:__init__ to instantiate class attributes

        ...

        obj = Itemizefile(filename: str, [stopwords]: list)

        Parameters
        ----------
        file_name:=str, required filename of text to be used by this instance
        stopwords=list, stop words to be removed from text, default=consts.STOP_WORDS
        """
        self._filename = file_name
        self._file_exists = self.file_exists(file_name)
        self._stopwords = self.expand_stopwords(stop_words)
        self._raw = []
        self._dict = defaultdict(int)
        self._origin = defaultdict(int)
        self._unique_item_count = 0
        self._file_item_count = 0
        self._stopwords_popped = 0
        self._populated = False
        self.thread = threading.Thread(target=self.itemize_file, args=())
        if self._stopwords is not None:
            if len(self._stopwords) != 0:
                self.expand_stopwords()

    def __eq__(self, obj) -> bool:
        if not isinstance(obj, ItemizeFileData):
            return NotImplemented
        return self.__self__ is obj.__self__

    def __hash__(self) -> hash:
        return hash(tuple(self))

    def __repr__(self) -> str:
        return f'{{0}}(filename={{1}}, file_exists={{2}}, stopwords={{3}}, \
            raw={{4}}, dict={{5}}, origin={{6}}, unique_item_count={{7}}, \
            file_item_count={{8}}, stopwords_pooped={{9}})'.format(
            {type(self).__name__}, self._filename,
            self._file_exists, self._stopwords, self._raw,
            self._dict, self._origin, self._unique_item_count,
            self._file_item_count, self._stopwords_popped)

    @property
    def filename(self) -> str:
        """
        (Class:ItemizeFileData) =>
        Property: _filename
        return self._filename
        """
        return self._filename

    @filename.setter
    def filename(self, value) -> None:
        """
        (Class:ItemizeFileData) =>
        Property: _filename, setter
        self._filename = value
        """
        self._filename = value

    @property
    def dict(self) -> dict:
        """
        (Class:ItemizeFileData) =>
        Property: _dict
        return self._dict
        """
        return self._dict

    @dict.setter
    def dict(self, obj=None) -> None:
        """
        (Class:ItemizeFileData) =>
        Property: _dict, setter
        self._dict = obj
        """
        self._dict = obj

    @property
    def stopwords(self) -> list:
        """
        (Class:ItemizeFileData) =>
        Property: _stopwords
        return list(self._stopwords)
        """
        return list(self._stopwords)

    @stopwords.setter
    def stopwords(self, obj=None) -> None:
        """
        (Class:ItemizeFileData) =>
        Property: _stopwords, setter
        self._stopwords = list(obj)
        """
        self._stopwords = list(obj)

    @property
    def unique_item_count(self) -> int:
        """
        (Class:ItemizeFileData) =>
        Property: _unique_item_count
        return self._unique_item_count
        """
        return self._unique_item_count

    @unique_item_count.setter
    def unique_item_count(self, value) -> None:
        """
        (Class:ItemizeFileData) =>
        Property: _unique_item_count, setter
        self._unique_item_count = value
        """
        self._unique_item_count = value

    @property
    def file_item_count(self) -> int:
        """
        (Class:ItemizeFileData) =>
        Property: _stopwords
        return self._file_item_count
        """
        return self._file_item_count

    @file_item_count.setter
    def file_item_count(self, value) -> None:
        """
        (Class:ItemizeFileData) =>
        Property: _stopwords, setter
        self._file_item_count = value
        """
        self._file_item_count = value

    def get_raw(self) -> list:
        """
        (Class:ItemizeFileData) => Method: get_raw(self) -> list
        Opens the file (filename) and creates a list containing
        items for each line of text

        ...

        Returns
        -------
        -> list
            each item of the list is a line of text from the file
            assigned to the class instance:
        """
        if self._file_exists:
            with open(self._filename, 'r') as fh:
                self._raw = [line for line in fh.readlines()]
                fh.close()
            return self._raw
        print("The file: {0} does not exist!".format(self._filename))
        return []

    def sanitize(self, text=None) -> str:
        """
        (Class:ItemizeFileData) => Method: sanitize(text: str) -> str
        If text is passed to method it will be sanitized using
        the private method _sanitize_text(text) -> str, else
        it cycles through each key in _dict and runs
        _sanitize_text(text) on each key of text and updates
        accordingly

        ...

        Parameters
        ----------
        text : str, Text to sanitize

        Returns
        -------
        -> str, all lowercase, without special chars, nor end lines
        """
        if text is not None:
            return self._sanitize_text(text)
        elif self._file_exists and len(self._dict) != 0:
            for item in self._dict:
                text = self._sanitize_text(item)
                dict_value = self._dict[item]
                del dict[item]
                self._dict[text] = dict_value
        else:
            return None

    def pop_stop_words(self, text=None) -> str:
        """
        (Class:ItemizeFileData) => Method: pop_stop_words(text: str) -> str
        Removes stop_words from text: str

        ...

        Parameters
        ----------
        text : str, Text to remove stop words from


        Returns
        -------
        -> str, without stop words
        """
        if isinstance(self._stopwords, list) and \
                self._stopwords is not None and \
                text is not None:
            for word in enumerate(self._stopwords):
                whole_word = " {0} ".format(word)
                if whole_word in text:
                    self._stopwords_popped += 1
                    text = text.replace(whole_word, " ")
        return text

    def echo_stopwords(self) -> bool:
        """
        (Class:ItemizeFileData) => Method: echo_stopwords() -> bool
        Prints stopwords in with columns of 10

        ...

        Returns
        -------
        -> bool (True if there are stopwords, otherwise False)
        """
        if self._stopwords is not None:
            if len(self._stopwords) != 0:
                col = 0
                row = []
                for w in self.stopwords:
                    col += 1
                    row.append(w)
                    if col % 10 == 0:
                        print("\t".join(row))
                        row = []
                return True
        return False

    def file_exists(self, file_name=None) -> bool:
        """
        (Class:ItemizeFileData) => Method: file_exists(file_name: str) -> bool
        Verifies file_name (filename) exists

        ...

        Parameters
        ----------
        file_name : str, The name of the file to be verified


        Returns
        -------
        -> bool (True if file exists, otherwise False)
        """
        if file_name is not None:
            if os.path.exists(file_name):
                self._file_exists = True
                self.__text_file = file_name
                return True
            else:
                return False

    def itemize_file(self) -> dict:
        """
        (Class:ItemizeFileData) => Method: itemize_file() -> dict
        Searches the text file (filename) for unique lines of text,
        sanitizes each line of text, adds init incrementers value
        for each key as a total count of the matches

        ...

        Returns
        -------
        -> dict
            keys: uqique lines of text from file as str
            items: int (0) for future use as iterator
        -> None
            if _dict has no items
        """
        for self._file_item_count, item in enumerate(self.get_raw()):
            indx = item = self.pop_stop_words(self.sanitize(item))
            self._origin[indx] = self._file_item_count
            if item not in [x for x in self._dict]:
                self._unique_item_count += 1
                self._dict[item] = 0
            self._populated = True
        if self._file_item_count != 0:
            self._populated = True
            return self._dict
        else:
            return None

    def expand_stopwords(self, stopwords=None) -> list:
        """
        (Class:ItemizeFileData) => Method: expand_stopwords() -> list
        Uses supplied stopwords and expands them using lemmatize,
        PorterStemmer(), and nltk stopwords.

        ...

        Returns
        -------
        -> list, expanded stopword list (appends nltk stopwords)
        """
        if stopwords is not None:
            sw = stopwords.copy()
            ps = PorterStemmer()
            wnl = WordNetLemmatizer()
            tword = sli = []
            for word in stopwords:
                tword = list(word_tokenize(word))
                for s in tword:
                    sli = list(wnl.lemmatize(str(s)))
                    for li in sli:
                        li = self.sanitize(str(s))
                        if li not in stopwords:
                            sw.append(li)
                        tword = ps.stem(li)
                        if tword not in stopwords:
                            sw.append(str(tword))
            stopwords = sw.copy()
            for w in stpw.words('english'):
                w = str(self.sanitize(w))
                if w not in stopwords:
                    stopwords.append(w)
            stopwords = [*set(stopwords)]
            stopwords = sorted(stopwords, key=lambda x: str(x))
            self._stopwords = stopwords.copy()
        return stopwords

    def _sort_dict(self) -> bool:
        """
        (Class:ItemizeFileData) => Method: _sort_dict() -> bool
        Sorts _dict (dict) by item count (integer)

        ...

        Returns
        -------
        -> bool, True if _dict contains items, False otherwise
        """
        if len(self._dict) != 0:
            self._dict = dict(sorted(
                self._dict.items(),
                key=lambda item: item[1], reverse=True))
            return True
        else:
            return False

    def _sanitize_text(self, text=None) -> str:
        """
        (Class:ItemizeFileData) => Method: _sanitize_text(text) -> str
        Removes all punctuation and end lines then converts it
        to all lower case

        ...

        Returns
        -------
        -> str, sanitized text
        """
        if text is not None:
            text = str(text) if not isinstance(text, str) else text
            while '  ' in text:
                text = text.replace('  ', '')
            text = text.replace(LINE, '')
            text = text.translate(text.maketrans(
                "",
                "",
                string.punctuation
            ))
            text.lower()
            return text
