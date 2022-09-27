#!venv/bin/ python3
# -*- coding: utf-8 -*-
"""
┬┌─┌─┐┬ ┬┌─┐┌─┐┬  ┬  ┌─┐┌┬┐┌─┐┬─┐
├┴┐├┤ └┬┘│  │ ││  │  ├─┤ │ │ │├┬┘
┴ ┴└─┘ ┴ └─┘└─┘┴─┘┴─┘┴ ┴ ┴ └─┘┴└─
Description:
    Compares text in a file to reference/glossary/key-items/dictionary file.
Copyright (C) 2022 Rush Solutions, LLC
Author: David Rush <davidprush@gmail.com>
License: MIT
Example:

        $ python keycollator.py

        Usage:

Todo:

    ***See Extractonator Todo Notes***

"""
import sys
from proceduretimer import ProcedureTimer
import click
from extractonator import KeyKrawler
from consts import LOG, TEXT, CSV, KEY


@click.group(
    context_settings=dict(
        ignore_unknown_options=True,
    ),
    invoke_without_command=True)
@click.option(
    '-t', '--text-file',
    default=TEXT,
    type=click.Path(exists=True),
    help='''Path/file name of the text to be searched
    for against items in the key file'''
)
@click.option(
    '-k', '--key-file',
    default=KEY,
    type=click.Path(exists=True),
    help='''Path/file name of the key file containing a
        dictionary, key items, glossary, or reference
        list used to search the text file'''
)
@click.option(
    '-r', '--result-file',
    default=CSV,
    type=click.Path(exists=True),
    help="Path/file name of the output file that \
        will contain the results (CSV or TXT)"
)
@click.option(
    '--limit-result',
    default=None,
    help="Limit the number of results"
)
@click.option(
    '--abreviate-result-items',
    default=32,
    help="Limit the text length of the results (default=32)"
)
@click.option(
    '--fuzzy-match-ratio',
    default=99,
    type=click.IntRange(0, 99, clamp=True),
    help='''Set the level of fuzzy matching (default=99) to
        validate matches using approximations/edit distances,
        uses acceptance ratios with integer values from 0 to 99,
        where 99 is nearly identical and 0 is not similar'''
)
@click.option(
    '--ubound-limit',
    default=None,
    type=click.IntRange(1, 99999, clamp=True),
    help="""
        Ignores items from the results with
        matches greater than the upper boundary (upper-limit);
        reduce eroneous matches
        """
)
@click.option(
    '--lbound-limit',
    default=None,
    type=click.IntRange(0, 99999, clamp=True),
    help="""
        Ignores items from the results with
        matches less than the lower boundary (lower-limit);
        reduce eroneous matches
        """
)
@click.option(
    '-v', '--verbose',
    is_flag=True,
    # default=0,
    # type=click.IntRange(0, 5, clamp=True),
    help="Turn on verbose"
)
@click.option(
    '-l', '--logging',
    is_flag=True,
    help="Turn on logging"
)
@click.option(
    '-L', '--log-file',
    default=LOG,
    type=click.Path(exists=True),
    help="Path/file name to be used for the log file"
)
def cli(
    verbose,
    fuzzy_match_ratio,
    key_file,
    text_file,
    limit_result,
    result_file,
    abreviate_result_items,
    ubound_limit,
    lbound_limit,
    logging,
    log_file,
):
    """
==================================================================\n
keycollator is an app that finds occurances of keys in a text file\n
==================================================================\n
    """
    KeyKrawler(
        text_file,
        key_file,
        result_file,
        limit_result,
        abreviate_result_items,
        log_file,
        verbose,
        ubound_limit,
        lbound_limit,
        fuzzy_match_ratio,
        logging,
        True
    )


def main(**kwargs):
    pt.stop_timer(sys._getframe().f_code.co_name)
    pt.echo(False, sys._getframe().f_code.co_name)


if __name__ == '__main__':
    pt = ProcedureTimer(sys._getframe().f_code.co_name)
    cli()
    main(pt)
