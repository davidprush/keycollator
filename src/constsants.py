# -*- coding: utf-8 -*-
"""
Copyright (C) 2022 Rush Solutions, LLC
Author: David Rush <davidprush@gmail.com>
License: MIT
Contains Constants
"""
LOG = "log.log"
TEXT = "text.txt"
CSV = "results.csv"
KEY = "keys.txt"
PFILE = {
    1: ".txt",
    2: ".txt",
    3: ".csv",
    4: ".log"
}
STOP_WORDS = [
    'a', 'about', 'above', 'after', 'again', 'against', 'ain', 'all',
    'am', 'an', 'and', 'any', 'are', 'aren', "aren't", 'as', 'at',
    'be', 'because', 'been', 'before', 'being', 'below', 'between',
    'both', 'but', 'by', 'can', 'couldn', "couldn't", 'd', 'did',
    'didn', "didn't", 'do', 'does', 'doesn', "doesn't", 'doing', 'don',
    "don't", 'down', 'during', 'each', 'few', 'find', 'for', 'from',
    'further', 'had', 'hadn', "hadn't", 'has', 'hasn', "hasn't", 'have',
    'haven', "haven't", 'having', 'he', 'help', 'her', 'here', 'hers',
    'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in', 'into',
    'is', 'isn', "isn't", 'it', "it's", 'its', 'itself', 'just', 'll',
    'm', 'ma', 'make', 'me', 'mightn', "mightn't", 'more', 'most',
    'mustn', "mustn't", 'my', 'myself', 'needn', "needn't", 'no', 'nor',
    'not', 'now', 'o', 'of', 'off', 'on', 'once', 'only', 'or', 'other',
    'our', 'ours', 'ourselves', 'out', 'over', 'own', 'post', 're', 's',
    'same', 'shan', "shan't", 'she', "she's", 'should', "should've",
    'shouldn', "shouldn't", 'so', 'some', 'such', 't', 'take', 'than',
    'that', "that'll", 'the', 'their', 'theirs', 'them', 'themselves',
    'then', 'there', 'these', 'they', 'this', 'those', 'through', 'to',
    'too', 'under', 'until', 'up', 'update', 'use', 've', 'very', 'was',
    'wasn', "wasn't", 'we', 'were', 'weren', "weren't", 'what', 'when',
    'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with',
    'won', "won't", 'work', 'wouldn', "wouldn't", 'y', 'you', "you'd",
    "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves'
]
SEP = "|"
LINE = "\n"
TAB = "\t"
SQT = '\''
FSPC = ' ' * 12
LFMT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DIV = "-" * 80 + "\n"
LOGTXT = {
    "limit_result": "OVER RESULT ITEM LIMIT: Removing result [{0}]:[{1}]",
    "timer": "timer:=[{0}] ",
    "itemize_text": "Extract data from {0}",
    "itemize_keys": "Extract data from {0}",
    "extract": "Extracted {0} items.[{1}] ",
    "match_text2keys": "Match {0} items to {1} items",
    "compare": "Compare {0} to {1} items",
    "purge_limited_items": "Out of bounds [{0}] [{1}]",
    "write_results2file": "Writing results to {0}",
    "echo_result": "{0}...",
    "csv_formatted_item": "{0}, {1} {2}",
    "sanitized": "sanitized [{0}]",
    "__validate_dtformat": "Invalid datetime format: {0} \
                falling back to \'default\': {1} \
                VALID datetime formats: {2}",
    "set_options": "Log[{0}]::[{1}]::INVALID OPTIONS",
    "set_log_msg": "{0} {1}::{2}::",
    "__logger_error": "{0}",
    "logerror": "{0}:{1}",
    "set_symbol": "SYMBOL:= {0} not valid!",
    "__set_params": "{0}: {1}",
    "join": "[ {0} ] ",
    "arg": "{0}",
    "stop_word": " {0} ",
    "file_invalid": "class ItemizeFile missing filename/file {3} {0} \
                    {1}does NOT exist OR missing stopwords! To add filename use: {0} \
                    {1}{1}class_obj = \
                    ItemizeFile({2}filename{2}, stopwords='STOP_WORDS') OR {0} \
                    {1}{1}class_obj.filename = {2}filename{2}} {0} \
                    {1}{1}class_obj.stopwords =  [x for x in STOP_WORDS] {0}",
    # itemized_log vars
    # self.__filename, item, self.__dict[item], self.__unique_items
    "itemized_log": "ITEMIZED/SANITIZED & REMOVED STOP WORDS \
                    from file:={0} item:={1} \
                    dict[{1}]:={2} index:={3},{1}"
}
RTBLHDR = [
    "No.", "Key", "Count"
]
STBLHDR = [
    "Statistic", "Total"
]
DTFMT = {
    'locale': '%c',
    'default': '%d/%m/%Y %H:%M:%S',
    'timeonly': '%H:%M:%S',
    'compressed': '%d%m%Y%H%M%S',
    'long': '%A %B %d, %Y, [%I:%M:%S %p]',
    'micro': '%H:%M:%S:%f'
}
MODES = ['a', 'r', 'w']
DTEMP = [
    '%d', '%m', '%Y',
    '%H', '%M', '%S',
    ' ', ':', '/'
]
DTDFLT = [
    '%d', '/', '%m',
    '/', '%Y', ' ',
    '%H', ':', '%M',
    ':', '%S'
]
SYMB = {
    'info': 'ℹ',
    'success': '✔',
    'warning': '⚠',
    'error': '✖'
}
SYMBFB = {
    'info': '¡',
    'success': 'v',
    'warning': '!!',
    'error': '×'
}
LPARAMS = {
    'filename': LOG,
    'filemode': 'a',
    'level': 'info',
    'dtformat': 'default',
    'message': "",
    'phony': 'no',
}
