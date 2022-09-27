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
    LOG, SYMB, LINE, LOGTXT, LPARAMS, DTFMT, MODES, DIV


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
        self.__dtstamp = datetime.now()
        self.__log_symbol = SYMB['info']
        self.__log_msg = ""
        self.__err_msg = ""
        self.__log_err = False
        self.__valid_params = False
        self.__log_count = 0
        self.__params = defaultdict(str)
        self.__params = {
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

    def __validate_dtformat(self):
        """
        CustomLogger
        Parameters
        ----------
            []]: [type], [required/optional]
        """
        if self.__params['dtformat'] in [x for x in DTFMT]:
            self.__update_dtstamp
            return True
        else:
            self.__log_err = True
            self.__logger_error(LOGTXT['__validate_dtformat'].format(
                self.__params['dtformat'],
                DTFMT['default'],
                ''.join([LOGTXT['join'].format(key) for key in DTFMT.keys()])
            ))
            self.__params['dtformat'] = DTFMT['default']
            self.__log_err = False
            return False

    def __logger_error(self, *args):
        """
        CustomLogger
        Parameters
        ----------
            []]: [type], [required/optional]
        """
        if self.__log_err:
            self.__err_msg = LOGTXT['options'].format(
                str(self.__log_count), str(self.__update_dtstamp()))
            for arg in args:
                for a in arg:
                    self.__err_msg += LOGTXT['__logger_error'].format(str(a))
            if LINE not in self.__err_msg[len(self.__err_msg) - 2]:
                self.__err_msg += LINE
            print(self.__err_msg)
            return True
        else:
            return False

    def __update_dtstamp(self):
        """
        CustomLogger
        Parameters
        ----------
            []]: [type], [required/optional]
        """
        self.__dtstamp = datetime.now()
        self.__dtstamp = \
            self.__dtstamp.strftime(DTFMT[self.__params['dtformat']])
        return self.__dtstamp

    def __set_params(self):
        """
        CustomLogger
        Parameters
        ----------
            []]: [type], [required/optional]
        """
        self.__valid_params = True
        self.__log_err = False
        param_err = defaultdict()
        if not isinstance(self.__params['message'], str):
            self.__params['text'] = str(self.__params['text'])
        if self.__params['filemode'] not in MODES:
            self.__valid_params = False
            param_err['filemode'] = self.__params['filemode']
            self.__params['filemode'] = 'a'
            param_err['filemode'] = self.__params['filemode']
        if self.__params['level'] not in SYMB.keys():
            self.__valid_params = False
            self.__params['level'] = 'info'
            param_err['level'] = self.__params['level']
        if not os.path.exists(self.__params['filename']):
            self.__valid_params = False
            param_err['filename'] = self.__params['filename']
            self.__params['filename'] = LOG
        if not self.__validate_dtformat():
            self.__valid_params = False
            param_err['dtformat'] = self.__params['dtformat']
        if self.__params['phony'].lower() not in ['yes', 'no']:
            self.__valid_params = False
            param_err['phony'] = self.__params['phony']
            self.__params['phony'] = 'no'
        if not self.__valid_params:
            self.__log_err = True
            self.__logger_error(
                [LOGTXT['__set_params'].format(
                    str(err), str(param_err[err])) for err in param_err]
            )
            self.__log_err = False
        return self.__valid_params

    def set_log_msg(self, *args, **kwargs):
        """
        CustomLogger
        Parameters
        ----------
            []]: [type], [required/optional]
        """
        self.__log_count += 1
        self.__log_msg = ""
        if kwargs:
            self.__log_symbol = kwargs.get(
                'symbol', 'info')
            new_kwargs = {k: v for k, v in kwargs.items() if k in ['symbol']}
            self.set_options(**new_kwargs)
        self.__log_msg = LOGTXT['set_log_msg'].format(
            SYMB['info'], str(self.__log_count), str(self.__update_dtstamp()))
        if args:
            for arg in args:
                self.__log_msg += LOGTXT['arg'].format(str(arg))
        self.__log_msg = self.__log_msg.translate(self.__log_msg.maketrans(
            "",
            "",
        ))
        self.__log_msg += LINE
        return self.__log_msg

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
        if self.__params['phony'].lower() == 'no':
            try:
                with open(
                    self.__params['filename'],
                        self.__params['filemode']) as log_fh:
                    log_fh.write(self.__log_msg)
            finally:
                log_fh.close()
        self.__params['message'] = self.__log_msg
        return self.__params['message']

    def set_options(self, *args, **kwargs):
        """
        CustomLogger
        Parameters
        ----------
            []]: [type], [required/optional]
        """
        param_err = defaultdict(str)
        for opt in kwargs:
            if opt not in self.__params:
                param_err[opt] = kwargs[opt]
                self.__log_err = True
            else:
                self.__params[opt] = kwargs[opt]
        for param in [
            li for li in self.__params
                if li not in kwargs]:
            if param in LPARAMS:
                self.__params[param] = str(LPARAMS[param]) \
                    if not isinstance(LPARAMS[param], str) \
                    else LPARAMS[param]
        if self.__log_err:
            self.__logger_error(
                [LOGTXT['set_options'].format(
                    str(e), str(param_err[e])) for e in param_err])
            return False
        elif self.__set_params():
            return True
        return True

    def log_count(self):
        return self.__log_count

    def create_log_file(self):
        with open(
            self.__params['filename'],
                self.__params['filemode']) as log_fh:
            log_fh.close()

    def set_symbol(self, symbol):
        if symbol not in [SYMB[x] for x in SYMB]:
            self.__logger_error(LOGTXT['set_symbol'].format(symbol))
            return False
        else:
            return True
