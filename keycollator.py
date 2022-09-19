#!venv/bin/ python3
# -*- coding: utf-8 -*-
"""
┬┌─┌─┐┬ ┬┌─┐┌─┐┬  ┬  ┌─┐┌┬┐┌─┐┬─┐
├┴┐├┤ └┬┘│  │ ││  │  ├─┤ │ │ │├┬┘
┴ ┴└─┘ ┴ └─┘└─┘┴─┘┴─┘┴ ┴ ┴ └─┘┴└─
Module keycollator.py documentation

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

Example:

        $ python keycollator.py

        *Notes

Todo:

        *

"""
import sys
import click
from constants import ProCons
from extractonator import ProTimerz, KeyKrawler


@click.group(
    context_settings=dict(
        ignore_unknown_options=True,
    ),
    invoke_without_command=True)
@click.option(
    '-v', '--set-verbose',
    is_flag=True,
    # default=0,
    # type=click.IntRange(0, 5, clamp=True),
    help="set verbose=[True/False], True=ON False=OFF"
)
@click.option(
    '-f', '--fuzzy-matching',
    default=99,
    type=click.IntRange(0, 99, clamp=True),
    help='''find valid matches using edit distances or
        approximate matches, uses acceptance ratio of
        integer values from 0 to 99, where 99 is near identical'''
)
@click.option(
    '-k', '--key-file',
    default=ProCons.KEYZ,
    type=click.Path(exists=True),
    help='''path/file name of the key file containing a
        dictionary, key items, glossary, or reference
        list used to search the text file'''
)
@click.option(
    '-t', '--text-file',
    default=ProCons.TXTS,
    type=click.Path(exists=True),
    help='''path/file name of the text to be searched
    for against items in the key file'''
)
@click.option(
    '-o', '--output-file',
    default=ProCons.REZF,
    type=click.Path(exists=True),
    help="path/file name of the output file that \
        will contain the results (CSV or TXT)"
)
@click.option(
    '-U', '--ubound-limit',
    default=99999,
    type=click.IntRange(1, 99999, clamp=True),
    help="""
        ignores items from the results with
        matches greater than the upper boundary (upper-limit);
        reduce eroneous matches
        """
)
@click.option(
    '-L', '--lbound-limit',
    default=0,
    type=click.IntRange(0, 99999, clamp=True),
    help="""
        ignores items from the results with
        matches less than the lower boundary (lower-limit);
        reduce eroneous matches
        """
)
@click.option(
    '-l', '--set-logging',
    default=False,
    help="set to True to turn on logging"
)
@click.option(
    '-Z', '--log-file',
    default=ProCons.LOGZ,
    type=click.Path(exists=True),
    help="path/file name to be used for the log file"
)
def cli(
    set_verbose,
    fuzzy_matching,
    key_file,
    text_file,
    output_file,
    ubound_limit,
    lbound_limit,
    set_logging,
    log_file,
):
    """
    keycollator is an app that finds occurances of keys in a text file
    """
    heavy_lifts = KeyKrawler(
        text_file,
        key_file,
        output_file,
        log_file,
        set_verbose,
        ubound_limit,
        lbound_limit,
        fuzzy_matching
    )
    heavy_lifts.cool_stats()


def main(**kwargs):
    ztimer.stop_timerz(sys._getframe().f_code.co_name)
    ztimer.echo_timerz(False, sys._getframe().f_code.co_name)


if __name__ == '__main__':
    ztimer = ProTimerz(sys._getframe().f_code.co_name)
    cli()
    main(ztimer)
