# This file is placed in the Public Domain.
#
# pylint: disable=E0603,E0402,W0401,W0614,W0611,W0622


"program"


from .objects import *
from .storage import *
from .default import *
from .excepts import *
from .locates import *
from .brokers import *
from .handler import *
from .parsers import *
from .threads import *


def __object__():
    return (
            'Default',
            'Object',
            'construct',
            'dump',
            'dumps',
            'edit',
            'fmt',
            'fqn',
            'ident',
            'items',
            'keys',
            'load',
            'loads',
            'update',
            'values',
           )


def __dir__():
    return (
        'Client',
        'Command',
        'Error',
        'Event',
        'Storage',
        'byorig',
        'cdir',
        'fetch',
        'find',
        'fns',
        'fntime',
        'ident',
        'launch',
        'last',
        'parse_command',
        'read',
        'sync',
        'write',
        'Storage',
    ) + __object__()


__all__ = __dir__()



def scan(pkg, modstr, initer=False, wait=True) -> []:
    mds = []
    for modname in spl(modstr):
        module = getattr(pkg, modname, None)
        if not module:
            continue
        for _key, cmd in inspect.getmembers(module, inspect.isfunction):
            if 'event' in cmd.__code__.co_varnames:
                Command.add(cmd)
        for _key, clz in inspect.getmembers(module, inspect.isclass):
            if not issubclass(clz, Object):
                continue
            Storage.add(clz)
        if initer and "init" in dir(module):
            module._thr = launch(module.init, name=f"init {modname}")
            mds.append(module)
    if wait and initer:
        for mod in mds:
            mod._thr.join()
    return mds
