# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0201,W0212,W0105,W0613,W0406,W0611,E0102


"main"


import inspect
import os
import readline
import time



from .command import Command
from .default import Default
from .error   import Error, debug
from .event   import Event
from .object  import Object, cdir, spl
from .handler import Handler
from .parse   import parse_command
from .storage import Storage
from .thread  import launch
from .utility import forever


def __dir__():
    return (
        'cmnd',
        'scan'
    )


def cmnd(txt):
    evn = Event()
    evn.txt = txt
    Command.handle(evn)
    evn.wait()
    return evn


def scan(pkg, modstr, initer=False) -> []:
    mods = []
    for modname in spl(modstr):
        module = getattr(pkg, modname, None)
        if not module:
            continue
        for key, cmd in inspect.getmembers(module, inspect.isfunction):
            if key.startswith("cb"):
                continue
            if 'event' in cmd.__code__.co_varnames:
                Command.add(cmd)
        for key, clz in inspect.getmembers(module, inspect.isclass):
            if key.startswith("cb"):
                continue
            if not issubclass(clz, Object):
                continue
            Storage.add(clz)
        if initer and "init" in dir(module):
            module._thr = launch(module.init, name=f"init {modname}")
        mods.append(module)
    return mods
