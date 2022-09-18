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


@click.command()
@click.option(
    '-v',
    '-vv',
    '-vvv',
    '--verbose',
    type=click.Choice([
        'quiet',
        'brief',
        'verbose',
        'debug',
        'trace'],
        case_sensitive=False
    ),
    default=0,
    count=True,
    help="verbosity level, default is nothing (0) [quiet], \
        -v (1) [brief], -vv (2) [debug], -vvv (3) [trace], \
        --verbose (7) [verbose]"
)
def set_verbosity_level(verbose):
    click.echo(f"Verbosity: {verbose}")


@click.command()
@click.option(
    '-f',
    '--fuzzy',
    '--fuzzy-matching',
    default=99,
    type=click.IntRange(0, 99, clamp=True),
    show_default=True,
    help="fuzzy-matching level, Find possible \
        valid matches using edit distances and \
        approximate matches, uses acceptance ratio \
        values (integers only) from 0 to 99, \
        where 0 is not a match and 99 is nearly identical"
)
def set_fuzzy_matching(fuzzy):
    click.echo(f"Fuzzy Matching: {fuzzy}")


@click.command(context_settings={"ignore_unknown_options": True})
@click.option(
    '-k',
    '--key-file',
    envvar='KEY_FILE',
    multiple=True,
    type=click.Path(exists=True),
    help="path/file name of the key file which \
        contains the dictionary, key items, glossary, or \
        reference list used to search the text file"
)
def set_key_file(key_file):
    fsplit = click.ParamType.split_envvar_value(key_file)
    for path in key_file:
        click.echo(path)
    print(fsplit)


@click.command(context_settings={"ignore_unknown_options": True})
@click.option(
    '-t',
    '--text-file',
    envvar='TEXT_FILE',
    multiple=True,
    type=click.Path(exists=True),
    help="path/file name of the text file that \
        will be searched for the items in the key file"
)
def set_text_file(text_file):
    fsplit = click.ParamType.split_envvar_value(text_file)
    for path in text_file:
        click.echo(path)
    print(fsplit)


@click.command(context_settings={"ignore_unknown_options": True})
@click.option(
    '-o',
    '--output-file',
    envvar='OUTPUT_FILE',
    multiple=False,
    type=click.Path(exists=True),
    default='results.csv',
    help="path/file name of the output file that \
        will contain the results (CSV or TXT)"
)
def set_output_file(output_file):
    fsplit = click.ParamType.split_envvar_value(output_file)
    for path in output_file:
        click.echo(path)
    print(fsplit)


@click.command()
@click.option(
    '-U',
    '--ubound-limit',
    default=99999,
    type=click.IntRange(1, 99999, clamp=True),
    show_default=True,
    help="ignores items from the results with \
        matches greater than the upper boundary (upper-limit); \
        reduce eroneous matches"
)
def set_upper_boundary(U):
    click.echo(f"Upper Boundary for Result: \
         {U}")


@click.command()
@click.option(
    '-L',
    '--lbound-limit',
    default=0,
    type=click.IntRange(0, 99999, clamp=True),
    show_default=True,
    help="ignores items from the results with \
        matches less than the lower boundary (lower-limit); \
        reduce eroneous matches"
)
def set_lower_boundary(L):
    click.echo(f"Lower Boundary for Result: \
         {L}")


@click.command(context_settings={"ignore_unknown_options": True})
@click.option(
    "-l",
    "--logging",
    is_flag=True,
    show_default=True,
    default=False,
    help="set to True to turn on logging"
)
@click.option(
    "--LF",
    "--log-file",
    envvar='LOG_FILE',
    multiple=False,
    type=click.Path(exists=True),
    default='log.txt',
    help="path/file name to be used for the log file"
)
def set_logging(logging, log_file):
    click.echo(f"Logging: \
         {logging}")
    click.echo(f"Log file: \
         {log_file}")


@click.option(
    "--br",
    is_flag=True,
    show_default=True,
    default=True,
    help="Add a thematic break"
)
def main():
    set_verbosity_level()
    set_logging()
    set_text_file()
    set_key_file()
    set_lower_boundary()
    set_upper_boundary()
    set


if __name__ == '__main__':

    main()
