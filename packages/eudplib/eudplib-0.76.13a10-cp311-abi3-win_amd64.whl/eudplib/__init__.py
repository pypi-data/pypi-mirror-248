#!/usr/bin/python
# Copyright 2014 by trgk.
# All rights reserved.
# This file is part of EUD python library (eudplib),
# and is released under "MIT License Agreement". Please see the LICENSE
# file that should have been included as part of this package.

import builtins
import keyword
import types

__version__ = "0.76.13a10"

oldGlobals = set(globals().keys())

from .core import *
from .ctrlstru import *
from .epscript import (
    EPS_SetDebug,
    EPSLoader,
    epsCompile,
    IsSCDBMap,
)
from .eudlib import *
from .maprw import *
from .offsetmap import CSprite, CUnit, EPDCUnitMap
from .trigger import *
from .trigtrg.runtrigtrg import (
    GetFirstTrigTrigger,
    GetLastTrigTrigger,
    RunTrigTrigger,
    TrigTriggerBegin,
    TrigTriggerEnd,
)
from .utils import *

# remove modules from __all__

_alllist = []
for _k, _v in dict(globals()).items():
    if _k in oldGlobals:
        continue
    elif _k != "stocktrg" and isinstance(_v, types.ModuleType):
        continue
    elif _k[0] == "_":
        continue
    _alllist.append(_k)

__all__ = _alllist


del _k
del _v


def eudplibVersion():
    return __version__


_alllist.append("eudplibVersion")


from .epscript import epscompile

epscompile._set_eps_globals(_alllist)
epscompile._set_py_keywords(keyword.kwlist)
epscompile._set_py_builtins(dir(builtins))
