# -*- coding: utf-8 -*-
"""
Copyright (C) 2022 Rush Solutions, LLC
Author: David Rush <davidprush@gmail.com>
License: MIT
    ProcedureTimer
        └──usage:
"""
import time


class ProcedureTimer:
    def __init__(
        self,
        msg="ProcedureTimer"
    ):
        """
        Constructs and starts the ProcedureTimer object.
        Parameters
        ----------
        msg : str, optional
            name of process where instance is created
        """
        self._tic = time.perf_counter()
        self._msg = str(msg)
        self._toc = self._tic
        self._tspan = time.perf_counter()
        self._fspan = str(self._tspan)
        self._tstr = ""
        self._sflag = False

    @property
    def tic(self) -> float:
        """
        Property tic for start time
        """
        return self._tic

    @property
    def msg(self) -> str:
        """
        Property msg for timestamp
        """
        return self._msg

    @property
    def toc(self) -> float:
        """
        Property toc for timestamp
        """
        return self._toc

    @property
    def tspan(self) -> float:
        """
        Property tspan for timestamp
        """
        return self._tspan

    @property
    def fspan(self) -> float:
        """
        Property fspan for timestamp
        """
        return self._fspan

    @property
    def tstr(self) -> str:
        """
        Property tstr for timestamp
        """
        return self._tstr

    @property
    def sflag(self) -> bool:
        """
        Property sflag for timestamp
        """
        return self._sflag

    def _t2s(self):
        """
        Formats/strips _fspanas str with
        2 decimals and ensures msg is str
        """
        self._fspan = str(f"{self._tspan:0.2f}")

    def _cupdate(self, c):
        """
        Updates _msg with new msg
        """
        if not self._sflag:
            if c:
                c = str(c)
            if c != self._msg:
                self._msg = c

    def _tupdate(self):
        """
        Updates _toc and calculates _span
        Condition
        ----------
        _sflag must be False
        """
        if not self._sflag:
            self._toc = time.perf_counter()
            self._tspan = self._toc - self._tic
        self._t2s()

    def _ftstr(self):
        """
        Creates a formatted str for console output.
        """
        self._t2s()
        self.__fstr = "[{0}]seconds".format(
            self._fspan
        )
        return self.__fstr

    def stop_timer(self, msg="stop_timer"):
        """
        Updates _toc and calculates _span
        Arguement
        ----------
        msg: str, optional can be anything to assign text to
        the formatted str _sflag to give context to the timestamp
        """
        if not self._sflag:
            self._cupdate(msg)
            self._tupdate()
            self._t2s()
            self._sflag = True

    def echo(self):
        """
        Updates _toc and calculates _span
        Condition
        ----------
        _sflag must be False
        """
        if not self._sflag:
            self._tupdate
        self._t2s()
        print(self._ftstr())

    def timestamp(self, as_str=False):
        """
        Updates the timer and returns time
        as str or unformatted time str
        Arguement
        ----------
        as_str: bool, optional
        """
        self._tupdate()
        if as_str:
            return str(self._fspan)
        else:
            return self._tspan

    def timestampstr(self):
        """
        Updates timer and returns formatted
        time in a string
        Arguement
        ----------
        as_str: bool, optional
            Updates the timer and returns time
            as str or unformatted time str
        """
        self._tupdate()
        return self._ftstr()
