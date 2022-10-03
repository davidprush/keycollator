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
*__sanitize_text(text) -> str, elseit cycles through each key in __dict and
*runs__sanitize_text(text) on each key of text and updatesaccordingly
*pop_stop_words(self, text=None) -> str
    =>Removes stop_words from text: str
*file_exists(self, file_name=None) -> bool
    =>Verifies file_name (filename) exists
*itemize_file(self) -> dict
    =>Searches text file (self.__filename) for unique lines oftext, sanitizes each
*line of text, adds values to the listed attributes
*__sort_dict(self) -> bool
    =>Sorts __dict (dict) by item count (integer)
"""
import os.path
import string

from collections import defaultdict

import nltk
import nltk.data
from nltk.corpus import stopwords as stpw
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from consts import LINE, STOP_WORDS


class ItemizeFileData:
    """
    Class: ItemizeFile

    obj = Itemizefile(filename: str, [stopwords]: list, optional)

    ...

    Attributes
    ----------
    __filename:=str, set to optional file_name parameter
    __file_exists:=bool, True if __filename exists, false otherwise
    __raw:=list, raw list of text from the file
    __stopwords:=list, words to be removed from the text
    __dict:=dict, init to defaultdict(int),
    __origin:= init to defaultdict(int),
    __unique_item_count:=int, total num. of unique items added to __dict
    __file_item_count:=int, total num. of items (lines) of text from __filename

    Methods
    -------
    get_raw() -> list =>Opens the file (filename) and creates a list containing
                    unique items for each line of text
    sanitize(text=None) -> str =>If text is passed to method it will be sanitized
                    usingthe private method __sanitize_text(text) -> str, elseit
                    cycles through each key in __dict and runs__sanitize_text(text)
                    on each key of text and updatesaccordingly
    pop_stop_words(text=None) -> str =>Removes stop_words from text: str
    file_exists(file_name=None) -> bool =>Verifies file_name (filename) exists
    itemize_file() -> dict =>Searches text file (self.__filename) for
                    unique lines oftext, sanitizes each line of text, adds values to
                    the listed attributes
    __sort_dict() -> bool =>Sorts __dict (dict) by item count (integer)

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
        Class: ItemizeFile Method:__init__ to instantiate class attributes

        ...

        obj = Itemizefile(filename: str, [stopwords]: list)

        Parameters
        ----------
        file_name:=str, required filename of text to be used by this instance
        stopwords=list, stop words to be removed from text, default=consts.STOP_WORDS
        """
        self.__filename = file_name
        self.__file_exists = self.file_exists(file_name)
        self.__stopwords = self.expand_stopwords(stop_words)
        self.__raw = []
        self.__dict = defaultdict(int)
        self.__origin = defaultdict(int)
        self.__unique_item_count = 0
        self.__file_item_count = 0
        self.__stopwords_popped = 0
        self.__populated = False

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
            {type(self).__name__}, self.__filename,
            self.__file_exists, self.__stopwords, self.__raw,
            self.__dict, self.__origin, self.__unique_item_count,
            self.__file_item_count, self.__stopwords_popped)

    @property
    def filename(self) -> str:
        """
        Class: ItemizeFile
        Property: __filename
        return self.__filename
        """
        return self.__filename

    @filename.setter
    def filename(self, value) -> None:
        """
        Class: ItemizeFile
        Property: __filename, setter
        self.__filename = value
        """
        self.__filename = value

    @property
    def dict(self) -> dict:
        """
        Class: ItemizeFile
        Property: __dict
        return self.__dict
        """
        return self.__dict

    @dict.setter
    def dict(self, obj=None) -> None:
        """
        Class: ItemizeFile
        Property: __dict, setter
        self.__dict = obj
        """
        self.__dict = obj

    @property
    def stopwords(self) -> list:
        """
        Class: ItemizeFile
        Property: __stopwords
        return list(self.__stopwords)
        """
        return list(self.__stopwords)

    @stopwords.setter
    def stopwords(self, obj=None) -> None:
        """
        Class: ItemizeFile
        Property: __stopwords, setter
        self.__stopwords = list(obj)
        """
        self.__stopwords = list(obj)

    @property
    def unique_item_count(self) -> int:
        """
        Class: ItemizeFile
        Property: __unique_item_count
        return self.__unique_item_count
        """
        return self.__unique_item_count

    @unique_item_count.setter
    def unique_item_count(self, value) -> None:
        """
        Class: ItemizeFile
        Property: __unique_item_count, setter
        self.__unique_item_count = value
        """
        self.__unique_item_count = value

    @property
    def file_item_count(self) -> int:
        """
        Class: ItemizeFile
        Property: __stopwords
        return self.__file_item_count
        """
        return self.__file_item_count

    @file_item_count.setter
    def file_item_count(self, value) -> None:
        """
        Class: ItemizeFile
        Property: __stopwords, setter
        self.__file_item_count = value
        """
        self.__file_item_count = value

    def get_raw(self) -> list:
        """
        Class: ItemizeFile Method: get_raw(self) -> list
        Opens the file (filename) and creates a list containing
        items for each line of text

        ...

        Returns
        -------
        -> list
            each item of the list is a line of text from the file
            assigned to the class instance:
        """
        if self.__file_exists:
            with open(self.__filename, 'r') as fh:
                self.__raw = [line for line in fh.readlines()]
                fh.close()
            return self.__raw
        print("The file: {0} does not exist!".format(self.__filename))
        return []

    def sanitize(self, text=None) -> str:
        """
        Class: ItemizeFile Method: sanitize(text: str) -> str
        If text is passed to method it will be sanitized using
        the private method __sanitize_text(text) -> str, else
        it cycles through each key in __dict and runs
        __sanitize_text(text) on each key of text and updates
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
            return self.__sanitize_text(text)
        elif self.__file_exists and len(self.__dict) > 1:
            for item in self.__dict:
                text = self.__sanitize_text(item)
                dict_value = self.__dict[item]
                del dict[item]
                self.__dict[text] = dict_value
        else:
            return None

    def pop_stop_words(self, text=None) -> str:
        """
        Class: ItemizeFile Method: pop_stop_words(text: str) -> str
        Removes stop_words from text: str

        ...

        Parameters
        ----------
        text : str, Text to remove stop words from


        Returns
        -------
        -> str, without stop words
        """
        if isinstance(self.__stopwords, list) and \
                self.__stopwords is not None and \
                text is not None:
            for word in enumerate(self.__stopwords):
                whole_word = " {0} ".format(word)
                if whole_word in text:
                    self.__stopwords_popped += 1
                    text = text.replace(whole_word, " ")
        return text

    def file_exists(self, file_name=None) -> bool:
        """
        Class: ItemizeFile Method: file_exists(file_name: str) -> bool
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
                self.__file_exists = True
                self.__text_file = file_name
                return True
            else:
                return False

    def itemize_file(self) -> dict:
        """
        Class: ItemizeFile Method: itemize_file() -> dict
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
            if __dict has no items
        """
        for self.__file_item_count, item in enumerate(self.get_raw()):
            indx = item = self.sanitize(item)
            self.__origin[indx] = self.__file_item_count
            if item not in [x for x in self.__dict]:
                self.__unique_item_count += 1
                item = self.pop_stop_words(item)
                self.__dict[item] = 0
            self.__populated = True
        if self.__file_item_count > 0:
            self.__populated = True
            return self.__dict
        else:
            return None

    def expand_stopwords(self, stopwords) -> list:
        """
        Class: ItemizeFile Method: expand_stopwords() -> list
        Uses supplied stopwords and expands them using lemmatize,
        PorterStemmer(), and nltk stopwords.

        ...

        Returns
        -------
        -> list, expanded stopword list (appends nltk stopwords)
        """
        if stopwords is not None:
            sw = []
            ps = PorterStemmer()
            wnl = WordNetLemmatizer()
            for word in stopwords:
                sw.append(word_tokenize(ps.stem(wnl.lemmatize(word))))
                for s in sw:
                    if len(s) > 1 and s not in stopwords:
                        sw.append(s)
            for w in sw:
                if w not in stopwords:
                    stopwords.append(w)
            sw = []
            for w in stpw.words('english'):
                if w not in stopwords:
                    stopwords.append(w)
            self.__stopwords = stopwords.copy()
            self.__stopwords = sorted(self.__stopwords, key=lambda x: str(x))
        return stopwords

    def __sort_dict(self) -> bool:
        """
        Class: ItemizeFile Method: __sort_dict() -> bool
        Sorts __dict (dict) by item count (integer)

        ...

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

    def __sanitize_text(self, text=None) -> str:
        """
        Class: ItemizeFile Method: __sanitize_text(text) -> str
        Removes all punctuation and end lines then converts it
        to all lower case

        ...

        Returns
        -------
        -> str, sanitized text
        """
        if text is not None:
            text = str(text) if not isinstance(text, str) else text
            text = text.replace(LINE, '')
            text = text.translate(text.maketrans(
                "",
                "",
                string.punctuation
            ))
            text.lower()
            return text
