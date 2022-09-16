#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Module ct2d_CLI.py Documentation.

This app takes a dictionary file containing words or phrases and
and compares it to a text file, then outputs a file listing the total
number of appearances for each word/phrase from the dictionary.

Todo:
    * Fix command line args
    * Add progress/status bars when populating text data
    * Add progress/status bars when populating dictionary data
    * Add progress/status bars when comparing dictionary to text
    * Migrate text file dictionary extraction to function
    * Migrate dictionary file extraction to function
    * Migrate comparison process to function
    * Consider adding classes

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""
import os
import io
import sys
import urllib
import argparse
import multiprocessing as mp
from pprint import pprint
from ct2d import d2ctxt


class Compare2Dict(object):

    def __init__(self):
        self.__parser = argparse.ArgumentParser()
        self.__parser.add_argument(
            "-c",
            "--csv-file",
            help="CSV output file name")
        self.__parser.add_argument(
            '-d',
            '--dictionary',
            help="dictionary file name")
        self.__parser.add_argument(
            '-f',
            '--fuzzy-matching',
            help="fuzzy matching [0-99]")
        self.__parser.add_argument(
            "-l",
            "--logging",
            help="use logging")
        self.__parser.add_argument(
            '-t',
            '--text-file-results',
            help="name of text file for results")
        self.__parser.add_argument(
            "-v",
            "--verbose",
            help="verbosity (-v, -vv, etc)")
        self.__parser.add_argument(
            '-V',
            '--version',
            version="%(prog)s (version {version})".format(version=__version__))

        def __banner(self):
            banner_text = r'''
                     :::::::: ::::::::::: ::::::::  :::::::::
                    :+:    :+:    :+:    :+:    :+: :+:    :+:
                    +:+           +:+          +:+  +:+    +:+
                    +#+           +#+        +#+    +#+    +:+
                    +#+           +#+      +#+      +#+    +#+
                    #+#    #+#    #+#     #+#       #+#    #+#
                     ########     ###    ########## #########
                       __            __    _ __
                      /  \)          /  \)  ' \)  \)         /
                     /--<  __  ,   /  /    /--' \. \. _   /_
                    /___/_/ (_/_  /__/_o  /  \_(_/_/_)_/ /_
                             /
                            '
            '''
            print(banner_text)
