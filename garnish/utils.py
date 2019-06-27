# Copyright 2019-2019 the garnish authors. See copying.md for legal info.

from pymol import cmd
import shutil
import collections
import os
import sys


def get_chain_bb(selection):
    """
    returns dictionary with format {chain: list-of-bb-atoms}
    """
    chains = cmd.get_chains(selection)
    chain_bb = {}
    for c in chains:
        # if chain is empty string, put it in the "all" bin
        if not c:
            c = "*"
        # "chain all" didn't actually select anything
        bb_id = cmd.identify(selection + f" and chain {c} and name BB")
        chain_bb[c] = bb_id
    return chain_bb


def get_gmx(gmx_bin):
    """
    if gmx binary is not given, find it. If it can't be found, raise an exception
    """
    if not gmx_bin:
        gmx_bin = shutil.which('gmx')
    if not gmx_bin:
        raise FileNotFoundError('no gromacs executable found.'
                                'Add it manually with gmx="PATH_TO_GMX"')
    return gmx_bin


def update_recursive(base_dict, input_dict):
    """
    similar to builtin dict.update, but recursively updates all sub-dictionaries
    """
    for k, v in input_dict.items():
        if isinstance(v, collections.Mapping):
            base_dict[k] = update_recursive(base_dict.get(k, {}), v)
        else:
            base_dict[k] = v
    return base_dict


def clean_path(path):
    """
    resolves path variables, `~`, symlinks and returns a clean absolute path
    """
    return os.path.realpath(os.path.expanduser(os.path.expandvars(path)))


def extension(loading_func):
    """
    Decorator/Wrapper for pymol extension functions.
    Will only return the loading function if called by pymol, else returns an empty function
    so no errors are raised.
    These functions can then be called in __init__.py to extend pymol functions to pymol.
    """
    try:
        # check if module was called by pymol
        main_initfile = sys.modules['__main__'].__file__

        # get the name of the parent module
        main_modulename = os.path.basename(clean_path(os.path.join(main_initfile, os.pardir)))
    
    except AttributeError:
        # importing from an interpreter like ipython raises this error
        main_modulename = None

    if main_modulename == 'pymol':
        return loading_func
    else:
        # Just return a passing lambda doing nothing, to avoid errors further downstream
        return lambda: None
