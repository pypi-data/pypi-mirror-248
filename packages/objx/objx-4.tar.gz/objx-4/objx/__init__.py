# This file is placed in the Public Domain.
#
# pylint: disable=E0603,E0402,W0401,W0614,W0611,W0622


"the python3 bot namespace"


from . import command, default, errors, handler, object
from . import storage, thread, timer, utility


from .command import *
from .default import *
from .errors  import *
from .event   import *
from .find    import *
from .group   import *
from .object  import *
from .parse   import *
from .handler import *
from .storage import *
from .thread  import *
from .timer   import *
from .utility import *


def __parse__():
    return (
        'NoDate',
        'cmnd',
        'fetch',
        'today',
        'get_day',
        'get_time',
        'find',
        'ident',
        'laps',
        'get_hour',
        'last',
        'now',
        'parse_command',
        'hms',
        'parse_time',
        'scan',
        'to_time',
        'sync',
        'to_day',
        'year'
    ) + __parse__()


def __dir__():
    return (
        'Commands',
        'Config',
        'Default',
        'Errors',
        'Event',
        'Hander',
        'Object',
        'Output',
        'Repeater',
        'Storage',
        'Thread',
        'Timer',
        'cfg',
        'construct',
        'debug',
        'dump',
        'dumps',
        'edit',
        'error',
        'fetch',
        'find',
        'fmt',
        'fns',
        'fntime',
        'forever',
        'fqn',
        'hook',
        'ident',
        'items',
        'keys',
        'laps',
        'last',
        'launch',
        'load',
        'loads', 
        'read',
        'search',
        'sync',
        'update',
        'values',
        'write'
    )



__all__ = __dir__()
