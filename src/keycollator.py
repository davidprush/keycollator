#!venv/bin/ python3
# -*- coding: utf-8 -*-
"""
Compares text in a file to reference/glossary/key-items/dictionary file.
Copyright (C) 2022 Rush Solutions, LLC
Author: David Rush <davidprush@gmail.com>
License: MIT
Example:
        $ python keycollator.py
        Usage:

Todo:
    ✖ Fix pylint errors
    ✖ Add command line option to add a stopwords file
    ✖ Fix all cli options
    ✖ Add comments
    ✖ Refactor code and remove redunancies
    ✖ Fix pylint errors
    ✖ Add proper error handling
    ✖ Add CHANGELOG.md
    ✖ Create method to KeyKrawler to select and _create missing files_
    ✖ Update CODE_OF_CONDUCT.md
    ✖ Update CONTRIBUTING.md
    ✖ Github: issue and pr templates
    ✖ Workflow Automation
    ✖ Makefile Usage
    ✖ Dockerfile
    ✖ @dependabot configuration
    ✖ Release Drafter (release-drafter.yml)
"""
import sys

import click

from proceduretimer import ProcedureTimer as pt
from extractonator import KeyKrawler as kk

import constants as const

__author__ = "David Rush"
__copyright__ = "Copyright 2022, Rush Solutions, LLC"
__credits__ = ["David Rush", "...", "...", "..."]
__license__ = "MIT"
__version__ = "0.0.5"
__maintainer__ = "David Rush"
__email__ = "davidprush@gmail.com"
__status__ = "Development"


@click.group(
    context_settings=dict(
        ignore_unknown_options=True,
    ),
    invoke_without_command=True)
@click.option(
    '-t', '--text-file',
    default=const.TEXT,
    type=click.Path(exists=True),
    help='''Path/file name of the text to be searched
    for against items in the key file'''
)
@click.option(
    '-k', '--key-file',
    default=const.KEY,
    type=click.Path(exists=True),
    help='''Path/file name of the key file containing a
        dictionary, key items, glossary, or reference
        list used to search the text file'''
)
@click.option(
    '-r', '--result-file',
    default=const.CSV,
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
    '--abreviate',
    default=32,
    help="Limit the text length of the results (default=32)"
)
@click.option(
    '--fuzz-ratio',
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
    default=const.LOG,
    type=click.Path(exists=True),
    help="Path/file name to be used for the log file"
)
def cli(
    verbose,
    fuzz_ratio,
    key_file,
    text_file,
    limit_result,
    result_file,
    abreviate,
    ubound_limit,
    lbound_limit,
    logging,
    log_file,
):
    """
    keycollator is an app that finds keys in a text file.
    """
    appkk = kk(
        text_file=text_file,
        key_file=key_file,
        csv_file=result_file,
        log_file=log_file,
        logging=logging,
        fuzz_ratio=fuzz_ratio,
        limit_result=limit_result,
        abreviate=abreviate,
        verbose=verbose,
        lbound=lbound_limit,
        ubound=ubound_limit
    )
    main(appkk)


def main(obj, **kwargs):
    app_timer = pt(sys._getframe().f_code.co_name)
    obj.get_key2text_matches()
    app_timer.stop_timer(sys._getframe().f_code.co_name)
    app_timer.echo()


if __name__ == '__main__':
    cli()
