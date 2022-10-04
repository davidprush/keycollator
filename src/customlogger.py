# -*- coding: utf-8 -*-
"""
Copyright (C) 2022 Rush Solutions, LLC
Author: David Rush <davidprush@gmail.com>
License: MIT
Contains class:
    CustomLogger
        └──usage:
"""
import os
from functools import wraps
from collections import defaultdict
from datetime import datetime
from consts import \
    LOG, SYMB, LINE, LOGTXT, \
    LPARAMS, DTFMT, MODES

__author__ = "David Rush"
__copyright__ = "Copyright 2022, Rush Solutions, LLC"
__credits__ = ["David Rush", "...", "...", "..."]
__license__ = "MIT"
__version__ = "0.0.5"
__maintainer__ = "David Rush"
__email__ = "davidprush@gmail.com"
__status__ = "Development"


# Function for decorator
def custom_logger(CustomLogger):
    """
    wrapper
    Parameters
    ----------
        []]: [type], [required/optional]
    """
    logger = CustomLogger(
        message="Iniate logger",
        filemode=MODES[0],
        filename='LOG',
        level='info',
        dtformat=DTFMT['compressed'])
    logger.write_log(" {0} ".format())
    return logger


def exception(logger):
    """
    exception handler
    Parameters
    ----------
        []]: [type], [required/optional]
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                logger.set_log_msg(
                    "exception in {0}{1}".format(
                        func.__name__, ex))
            raise

        return wrapper
    return decorator


class CustomLogger:
    def __init__(self, *args, **kwargs):
        """
        Constructs and starts the CustomLogger object.
        arguements
        ----------
        *args:
            all args are converted to strings and appended to
                text str for the log message
        parameters
        ----------
        **kwargs:
            text: str, optional
            filemode: str, optional
                valid modes are 'a', 'w', 'r', default is 'a'
            level: str, optional
                valid options are 'info', 'success', 'warning', 'error'
            filename: str, optional
                name of the log file, default is LOG from .consts
            dtformat: str, optional
                format date with:
                    ['locale', 'standar', 'timeonly', 'compressed', 'long', 'micro']
                    locale='%c', default='%d/%m/%Y %H:%M:%S',
                    timeonly='%H:%M:%S', compressed='%d%m%Y%H%M%S',
                    long='%A %B %d, %Y, [%I:%M:%S %p]', micro='%H:%M:%S:%f'
            message: str, optional
                message used for the log
        """
        self._dtstamp = datetime.now()
        self._log_symbol = SYMB['info']
        self._log_msg = ""
        self._err_msg = ""
        self._log_err = False
        self._valid_params = False
        self._log_count = 0
        self._params = defaultdict(str)
        self._params = {
            'filename': LOG,
            'filemode': 'a',
            'level': 'info',
            'dtformat': 'default',
            'message': '',
            'phony': kwargs.get('phony', 'no'),
        }
        if kwargs:
            self.set_options(**kwargs)
        if args:
            self.set_log_msg(*args)

    def _validate_dtformat(self):
        """
        CustomLogger
        Parameters
        ----------
            []]: [type], [required/optional]
        """
        if self._params['dtformat'] in [x for x in DTFMT]:
            self._update_dtstamp
            return True
        else:
            self._log_err = True
            self._logger_error(LOGTXT['_validate_dtformat'].format(
                self._params['dtformat'],
                DTFMT['default'],
                ''.join([LOGTXT['join'].format(key) for key in DTFMT.keys()])
            ))
            self._params['dtformat'] = DTFMT['default']
            self._log_err = False
            return False

    def _logger_error(self, *args):
        """
        CustomLogger
        Parameters
        ----------
            []]: [type], [required/optional]
        """
        if self._log_err:
            self._err_msg = LOGTXT['options'].format(
                str(self._log_count), str(self._update_dtstamp()))
            for arg in args:
                for a in arg:
                    self._err_msg += LOGTXT['_logger_error'].format(str(a))
            if LINE not in self._err_msg[len(self._err_msg) - 2]:
                self._err_msg += LINE
            print(self._err_msg)
            return True
        else:
            return False

    def _update_dtstamp(self):
        """
        CustomLogger
        Parameters
        ----------
            []]: [type], [required/optional]
        """
        self._dtstamp = datetime.now()
        self._dtstamp = \
            self._dtstamp.strftime(DTFMT[self._params['dtformat']])
        return self._dtstamp

    def _set_params(self):
        """
        CustomLogger
        Parameters
        ----------
            []]: [type], [required/optional]
        """
        self._valid_params = True
        self._log_err = False
        param_err = defaultdict()
        if not isinstance(self._params['message'], str):
            self._params['text'] = str(self._params['text'])
        if self._params['filemode'] not in MODES:
            self._valid_params = False
            param_err['filemode'] = self._params['filemode']
            self._params['filemode'] = 'a'
            param_err['filemode'] = self._params['filemode']
        if self._params['level'] not in SYMB.keys():
            self._valid_params = False
            self._params['level'] = 'info'
            param_err['level'] = self._params['level']
        if not os.path.exists(self._params['filename']):
            self._valid_params = False
            param_err['filename'] = self._params['filename']
            self._params['filename'] = LOG
        if not self._validate_dtformat():
            self._valid_params = False
            param_err['dtformat'] = self._params['dtformat']
        if self._params['phony'].lower() not in ['yes', 'no']:
            self._valid_params = False
            param_err['phony'] = self._params['phony']
            self._params['phony'] = 'no'
        if not self._valid_params:
            self._log_err = True
            self._logger_error(
                [LOGTXT['_set_params'].format(
                    str(err), str(param_err[err])) for err in param_err]
            )
            self._log_err = False
        return self._valid_params

    def set_log_msg(self, *args, **kwargs):
        """
        CustomLogger
        Parameters
        ----------
            []]: [type], [required/optional]
        """
        self._log_count += 1
        self._log_msg = ""
        if kwargs:
            self._log_symbol = kwargs.get(
                'symbol', 'info')
            new_kwargs = {k: v for k, v in kwargs.items() if k in ['symbol']}
            self.set_options(**new_kwargs)
        self._log_msg = LOGTXT['set_log_msg'].format(
            SYMB['info'], str(self._log_count), str(self._update_dtstamp()))
        if args:
            for arg in args:
                self._log_msg += LOGTXT['arg'].format(str(arg))
        self._log_msg = self._log_msg.translate(self._log_msg.maketrans(
            "",
            "",
        ))
        self._log_msg += LINE
        return self._log_msg

    def write_log(self, *args, **kwargs):
        """
        CustomLogger
        Parameters
        ----------
            []]: [type], [required/optional]
        """
        if kwargs:
            self.set_options(**kwargs)
        self.set_log_msg(*args)
        if self._params['phony'].lower() == 'no':
            try:
                with open(
                    self._params['filename'],
                        self._params['filemode']) as log_fh:
                    log_fh.write(self._log_msg)
            finally:
                log_fh.close()
        self._params['message'] = self._log_msg
        return self._params['message']

    def set_options(self, *args, **kwargs):
        """
        CustomLogger
        Parameters
        ----------
            []]: [type], [required/optional]
        """
        param_err = defaultdict(str)
        for opt in kwargs:
            if opt not in self._params:
                param_err[opt] = kwargs[opt]
                self._log_err = True
            else:
                self._params[opt] = kwargs[opt]
        for param in [
            li for li in self._params
                if li not in kwargs]:
            if param in LPARAMS:
                self._params[param] = str(LPARAMS[param]) \
                    if not isinstance(LPARAMS[param], str) \
                    else LPARAMS[param]
        if self._log_err:
            self._logger_error(
                [LOGTXT['set_options'].format(
                    str(e), str(param_err[e])) for e in param_err])
            return False
        elif self._set_params():
            return True
        return True

    def log_count(self):
        return self._log_count

    def create_log_file(self):
        with open(
            self._params['filename'],
                self._params['filemode']) as log_fh:
            log_fh.close()

    def set_symbol(self, symbol):
        if symbol not in [SYMB[x] for x in SYMB]:
            self._logger_error(LOGTXT['set_symbol'].format(symbol))
            return False
        else:
            return True

    def reset_log_file(self) -> bool:
        """
        Class: KeyKrawler method reset_log_file() -> bool
        Resets the log file (_log_file) be overwriting it
        ...
        Attributes
        ----------
        _log_file:=str, name of file to write log

        Return
        ------
        -> bool, True if file is written
        """
        with open(self._log_file, 'w') as fh:
            fh.close()
            return True
        return False
