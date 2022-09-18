#!/venv/bin/ python3
# -*- coding: utf-8 -*-
"""
┬┌─┌─┐┬ ┬┌─┐┌─┐┬  ┬  ┌─┐┌┬┐┌─┐┬─┐
├┴┐├┤ └┬┘│  │ ││  │  ├─┤ │ │ │├┬┘
┴ ┴└─┘ ┴ └─┘└─┘┴─┘┴─┘┴ ┴ ┴ └─┘┴└─
Module dictionarytextcompare.py documentation

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

        $ python dictionarytextcompare.py

        *Notes

Todo:
    *

"""
import click
from constants import ProCons
from functools import wraps
from extractonator import ProTimerz, KeyKrawler


class Config(object):
    def __init__(self):
        self.verbose = False


pass_config = click.make_pass_decorator(Config, ensure=True)


def pass_obj(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        return ctx.invoke(f, ctx.obj, *args, **kwargs)
    return update_wrapper(new_func, f)


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
    help="verbosity level, True='ON' False='OFF'"
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
    help="""ignores items from the results with
        matches greater than the upper boundary (upper-limit);
        reduce eroneous matches"""
)
@click.option(
    '-L', '--lbound-limit',
    default=0,
    type=click.IntRange(0, 99999, clamp=True),
    help="""ignores items from the results with
        matches less than the lower boundary (lower-limit);
        reduce eroneous matches"""
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
# @click.pass_context
@pass_config
def cli(
    Config,
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
    """ Docstring Here! """

    Config.set_verbose = set_verbose
    Config.fuzzy_matching = fuzzy_matching
    Config.key_file = key_file
    Config.text_file = text_file
    Config.output_file = output_file
    Config.ubound_limit = ubound_limit
    Config.lbound_limit = lbound_limit
    Config.set_logging = set_logging
    Config.log_file = log_file


@cli.group()
# @click.pass_context
@pass_config
def tourney(config):

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

    if config.set_verbose:
        click.echo(f"Verbosity: {config.set_verbose}")
        click.echo(f"Fuzzy Matching: {Config.fuzzy_matching}")
        print(osplit)
        click.echo(f"Upper Boundary for Result: \
             {config.ubound_limit}")
        click.echo(f"Lower Boundary for Result: \
             {config.lbound_limit}")
        click.echo(f"Logging: \
             {config.set_logging}")
        click.echo(f"Log file: \
             {config.log_file}")

    heavy_lifts = KeyKrawler(
        Config.text_file,
        Config.key_file,
        Config.result_file,
        Config.log_file,
        Config.set_verbose,
        Config.ubound_limit,
        Config.lbound_limit,
        Config.fuzzy_matching
    )
    heavy_lifts.write_results()


@cli.group()
@click.pass_context
@pass_config
def main(**kwargs):
    ztimer.stop_timer("main()")
    ztimer.get_duration(False, "main()")


if __name__ == '__main__':
    ztimer = ProTimerz("__main__")
    cli()
    main(ztimer)
