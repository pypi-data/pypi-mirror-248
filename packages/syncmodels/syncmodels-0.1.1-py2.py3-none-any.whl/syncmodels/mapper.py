"""
Mappers transform plain dict to another dict
converting key and values.

Classes definition are inspired on pydantic

"""
import sys
import traceback

from dateutil.parser import parse
from dateutil.tz import gettz

from . import models

# ---------------------------------------------------------
# Loggers
# ---------------------------------------------------------

from pycelium.tools.logs import logger

log = logger(__name__)

# =========================================================
# Mappers Support
# =========================================================


def I(x):
    return x


def INT(x):
    if x is None:
        return 0
    return int(x)


def BOOL(x):
    if x is None:
        return False
    return bool(x)


TZINFOS = {"UTC": gettz(" Etc/UTC")}


def DATE(x):
    if x is None:
        return None

    return parse(x, tzinfos=TZINFOS)


class Mapper:
    @classmethod
    def _populate(cls):
        cls.MAPPING = {}
        for key in dir(cls):
            value = getattr(cls, key)
            if isinstance(value, tuple):
                l = len(value)
                if l == 2:
                    # is an attribute
                    cls.MAPPING[key] = *value, None
                elif l == 3:
                    cls.MAPPING[key] = value

        return cls.MAPPING

    @classmethod
    def transform(cls, org):
        result = {}
        MAP = getattr(cls, 'MAPPING', None) or cls._populate()
        try:
            for k in set(org).intersection(MAP):
                v = org[k]
                t_name, t_value, t_default = MAP[k]
                name = t_name(k)
                value = t_value(v)
                result[name] = value
        except Exception as why:
            log.error(why)
            log.error("".join(traceback.format_exception(*sys.exc_info())))
            foo = 1
        return result

    @classmethod
    def pydantic(cls, norm):
        """Create a pydantic object as well"""
        klass = getattr(cls, 'PYDANTIC', None)
        if klass:
            item = klass(**norm)
            return item
        log.warning(f"{cls} has not defined a PYDANTIC class")
        return norm
