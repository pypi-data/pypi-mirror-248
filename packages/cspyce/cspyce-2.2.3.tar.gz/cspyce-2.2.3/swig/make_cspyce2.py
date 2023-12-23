################################################################################
# cspyce/cspyce2.py
#
# This module re-declares every cspyce1 function explicitly, with its list of
# argument names as used by CSPICE. The practical effect is that functions in
# cspyce2 module can be called in a fully Python-like way, the rightmost inputs
# in any order and identified by their names.
#
# Used internally by cspyce; not intended for direct import.
################################################################################

from itertools import groupby
from operator import itemgetter
import sys
from types import ModuleType

#####################
#  When this file is run, the packages _cspyce0.py and cspyce2.py don't yet exist.
#  Yet, the simple fact of loading cspyce.cspyce1, which we need, will cause them to
#  be loaded.  So we lie to Python and tell it that we've already loaded those two
#  modules, and it doesn't need to look for them.
#
#  Likewise, cspyce1 may make calls to cspyce0, which is just a Python veneer over
#  _cspyce0.  So although we load cspyce0, we overwrite all of its methods to be noops.
#
#  This is ugly, but it works.
######################


# Creates a fake module.  Python won't reload a module if it already thinks it's loaded.
def new_module(name, doc=None):
    m = ModuleType(name, doc)
    m.__file__ = name + '.py'
    sys.modules[name] = m
    return m


# Create empty versions of these two modules.
new_module("cspyce.cspyce2")
new_module("cspyce._cspyce0")

import cspyce.cspyce1 as cspyce1
import keyword


HEADER = """
################################################################################
# cspyce/cspyce2.py
#
# This module re-declares every cspyce1 function explicitly, with its list of
# argument names as used by CSPICE. The practical effect is that functions in
# cspyce2 module can be called in a fully Python-like way, the rightmost inputs
# in any order and identified by their names.
#
# Used internally by cspyce; not intended for direct import.
#
# This file is automatically generated by the program make_cspyce2.py. 
# Do not modify. 
################################################################################

import cspyce.cspyce1 as cs1

def __copy_attributes_from(function, old_function):
    for key, value in vars(old_function).items():
        if callable(value):
            value = globals()[value.__name__]
        setattr(function, key, value)

"""


TRAILER = """
erract('SET', 'EXCEPTION')
"""


def make_cspyce2(file_name):
    with open(file_name, "w") as file:
        populate_cspyce2(file)


def populate_cspyce2(file):
    file.write(HEADER.lstrip())

    population = [(name.partition('_')[0], name, func)
                  for name, func in vars(cspyce1).items()
                  if callable(func) and hasattr(func, 'ARGNAMES')]
    population.sort()

    for root, group in groupby(population, itemgetter(0)):
        group = list(group)
        file.write(f'#########################\n')
        file.write(f'# {root}\n')
        file.write(f'#########################\n\n')
        for _root, name, func in group:
            argnames = [(x + "_" if keyword.iskeyword(x) else x) for x in func.ARGNAMES]
            call_list = ", ".join(argnames)
            parameters = argnames[:]
            for index in range(len(func.__defaults__ or ())):
                # x[~index] gives you the index-th element from the end.
                parameters[~index] += " = " + repr(func.__defaults__[~index])
            parameter_list = ', '.join(parameters)
            file.write(f"def {name}({parameter_list}):\n")
            if func.__doc__:
                file.write('    """\n')
                for line in func.__doc__.strip().splitlines():
                    file.write("    " + line + "\n");
                file.write('    """\n')
            file.write(f"    return cs1.{name}({call_list})\n\n")

        for _root, name, func in group:
            file.write(f'__copy_attributes_from({name}, cs1.{name})\n')

        file.write("\n")

    file.write(TRAILER.lstrip())
