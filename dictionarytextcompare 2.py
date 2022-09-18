#!/venv/bin/ python3
# -*- coding: utf-8 -*-
"""Module main.py Documentation.

App that uses click to handle CLI

Example:

        $ python ct2d.py

        *Notes


Todo:
    *

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html
"""
import click
import sys
import os.path
import string
import progressbar
import verboselogs
import logging
# import pandas as pd
from collections import defaultdict
from nltk.stem import PorterStemmer
from time import sleep
from fuzzywuzzy import fuzz
# from nltk.tokenize import word_tokenize


def Config(object):
    def __init__(self):
        self.empty_placeholder = True


pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group(chain=True, invoke_without_command=True)
@pass_config
@click.option(
    '-v',
    '-vv',
    '-vvv',
    '--verbose',
    default=0,
    count=True,
    help='''
        verbosity level, default is nothing (0) [quiet],
        -v (1) [brief], -vv (2) [debug], -vvv (3) [trace],
        --verbose (7) [verbose]
    '''
)
@click.option(
    '-f',
    '--fuzzy',
    '--fuzzy-matching',
    default=99,
    type=click.IntRange(0, 99, clamp=True),
    show_default=True,
    help='''
        fuzzy-matching level, Find possible
        valid matches using edit distances and
        approximate matches, uses acceptance ratio
        values (integers only) from 0 to 99,
        where 0 is not a match and 99 is nearly identical
    '''
)
@click.option(
    '-k',
    '--key-file',
    envvar='KEY_FILE',
    multiple=True,
    type=click.Path(exists=True),
    default=['key.txt'],
    help='''
        path/file name of the key file which
        contains the dictionary, key items, glossary, or
        reference list used to search the text file
    '''
)
@click.option(
    '-t',
    '--text-file',
    envvar='TEXT_FILE',
    multiple=True,
    type=click.Path(exists=True),
    default=['text.txt'],
    help='''
        path/file name of the text file that
        will be searched for the items in the key file
    '''
)
@click.option(
    '-o',
    '--output-file',
    envvar='OUTPUT_FILE',
    multiple=False,
    type=click.Path(exists=True),
    default='results.csv',
    help='''
        path/file name of the output file that
        will contain the results (CSV or TXT)
    '''
)
@click.option(
    '-U',
    '--ubound-limit',
    default=99999,
    type=click.IntRange(1, 99999, clamp=True),
    show_default=True,
    help='''
        ignores items from the results with
        matches greater than the upper boundary (upper-limit);
        reduce eroneous matches
    '''
)
@click.option(
    '-L',
    '--lbound-limit',
    default=0,
    type=click.IntRange(0, 99999, clamp=True),
    show_default=True,
    help='''
        ignores items from the results with
        matches less than the lower boundary (lower-limit);
        reduce eroneous matches
    '''
)
@click.option(
    '-l',
    '--logging',
    is_flag=True,
    show_default=True,
    default=False,
    help='''
        set to True to turn on logging
    '''
)
@click.option(
    '--LF',
    '--log-file',
    envvar='LOG_FILE',
    multiple=False,
    type=click.Path(exists=True),
    default='log.txt',
    help='''
        path/file name to be used for the log file
    '''
)
def cli(
    config,
    verbose,
    fuzzy,
    key_file,
    text_file,
    output_file,
    ubound_limit,
    lbound_limit,
    logging,
    log_file
):
    config.verbose = verbose
    config.fuzzy = fuzzy
    config.key_file = key_file
    config.text_file = text_file
    config.output_file = output_file
    config.ubound_limit = ubound_limit
    config.lbound_limit = lbound_limit
    config.logging = logging
    config.log_file = log_file


@cli.command(context_settings={"ignore_unknown_options": True})
@pass_config
def get_results(config):
    click.echo(f"Verbosity: {config.verbose}")
    click.echo(f"Fuzzy Matching: {config.fuzzy}")
    ksplit = click.ParamType.split_envvar_value(config.key_file)
    for path in config.key_file:
        click.echo(path)
    print(ksplit)
    tsplit = click.ParamType.split_envvar_value(config.text_file)
    for path in config.text_file:
        click.echo(path)
    print(tsplit)
    osplit = click.ParamType.split_envvar_value(config.output_file)
    for path in config.output_file:
        click.echo(path)
    print(osplit)
    click.echo(f"Upper Boundary for Result: \
         {config.ubound_limit}")
    click.echo(f"Lower Boundary for Result: \
         {config.lbound_limit}")
    click.echo(f"Logging: \
         {config.logging}")
    click.echo(f"Log file: \
         {config.log_file}")


def main():
    get_results


if __name__ == '__main__':
    cli()
    main()
