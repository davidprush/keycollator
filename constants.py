#!/venv/bin/ python3
# -*- coding: utf-8 -*-
"""
┌─┐┌─┐┌┐┌┌─┐┌┬┐┌─┐┌┐┌┌┬┐┌─┐
│  │ ││││└─┐ │ ├─┤│││ │ └─┐
└─┘└─┘┘└┘└─┘ ┴ ┴ ┴┘└┘ ┴ └─┘
Module constants.py documentation

 #     # ### #######    #       ###  #####  ####### #     #  #####  #######
 ##   ##  #     #       #        #  #     # #       ##    # #     # #
 # # # #  #     #       #        #  #       #       # #   # #       #
 #  #  #  #     #       #        #  #       #####   #  #  #  #####  #####
 #     #  #     #       #        #  #       #       #   # #       # #
 #     #  #     #       #        #  #     # #       #    ## #     # #
 #     # ###    #       ####### ###  #####  ####### #     #  #####  #######

[[Copyright (c) 2022 David P. Rush]]Permission is hereby granted, free of charge, to
any person obtaining a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished to
do so, subject to the following conditions: The above copyright notice and this
permission notice shall be included in all copies or substantial portions of the
Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR
A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


Contains the following constants:

                ->END_LINE
                ->APP_NAME
                ->BANNER_APP
                ->DIV_LINE
                ->APP_DESCRIPTION
                ->APP_EPILOG
                ->RESULTS_HDR
                ->BANNER_RESULTS
                ->RESULTS_HDR_TXT
                ->RESULTS_FTR
                ->PERFORMANCE
                ->STATISTICS = PERFORMANCE

Notes:

    -

Todo:

    *

"""


class ProCons:
    LOGZ = "log.txt"
    TXTS = "text.txt"
    REZF = "results.csv"
    KEYZ = "keys.txt"
    END_LINE = "\n"
    APP_NAME = "ct2d.py"
    BANNER_APP = '''

     #    # ###### #   #  ####   ####  #      #        ##   #####  ####  #####
     #   #  #       # #  #    # #    # #      #       #  #    #   #    # #    #
     ####   #####    #   #      #    # #      #      #    #   #   #    # #    #
     #  #   #        #   #      #    # #      #      ######   #   #    # #####
     #   #  #        #   #    # #    # #      #      #    #   #   #    # #   #
     #    # ######   #    ####   ####  ###### ###### #    #   #    ####  #    #

    '''
    DIV_LINE = END_LINE + '''
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #########################################################################################
    ''' + END_LINE
    APP_DESCRIPTION = '''
                App takes two files, a dictionary file and a
                  and a text file, and counts how many times
                  each line in the dictionary file appears in
                  the text file. The app can output the results
                  to the console and/or csv/text file. Matching
                  will use fuzzy matching to get desired results.'''

    APP_EPILOG = '''
                End of help.'''
    RESULTS_HDR = '''

     #####  ######  ####  #    # #      #####  ####
     #    # #      #      #    # #        #   #
     #    # #####   ####  #    # #        #    ####
     #####  #           # #    # #        #        #
     #   #  #      #    # #    # #        #   #    #
     #    # ######  ####   ####  ######   #    ####

    '''
    BANNER_RESULTS = RESULTS_HDR
    RESULTS_HDR_TXT = \
        "The following is a list of dcitionary items found in the text file:"
    RESULTS_FTR = DIV_LINE
    PERFORMANCE = "Stats for this run... \n \
    Total Dictionary Items: {0} \n \
    Total Text File Items: {0} \n \
    Total Keys Added to List: {0} \n \
    Total Comparisons: {0} \n \
    Total Runtime: {0} \n \n"
    STATISTICS = PERFORMANCE
    NO_MATCHES = "<<<<**** [ NO MATCHES FOUND! ] ****>>>>"
