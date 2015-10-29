#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, print_function, absolute_import,
                        unicode_literals)

__version__ = "0.1.1"

import os
import re
import subprocess
import warnings

def run_command(cmd):
    """
    Open a child process, and return its exit status and stdout.

    """
    child = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out = [s for s in child.stdout]
    err = [s for s in child.stderr]
    w = child.wait()
    return os.WEXITSTATUS(w), out, err


# Check to make sure that the required environment variable is present.
try:
    ev = os.environ["SPS_HOME"]
except KeyError:
    raise ImportError("You need to have the SPS_HOME environment variable")

# Check the githashes to make sure the required FSPS updates are
# present, and if not or there are no githashes, raise an error
REQUIRED_GITHASHES = ['6ad1058\n']

cmd = 'cd {0}; git log --format="format:%h"'.format(ev)
stat, githashes, err = run_command(cmd)
accepted = (len(githashes) > 0) and (len(err) == 0)
if not accepted:
    raise ImportError("Your FSPS version is not under git version "
                      "control. FSPS is now available on github at "
                      "https://github.com/cconroy20/fsps")
accepted = [req in githashes for req in REQUIRED_GITHASHES]
if not accepted:
    reqs = ",".join([r[:-2] for r in REQUIRED_GITHASHES])
    raise ImportError("Your FSPS version does not have correct history.  "
                      "Please make sure that you have the following commits "
                      "in your git history: {0}".format(reqs))
else:
    # Store the githash.  If any version checking is going to happen,
    # it should happen here
    fsps_vers = githashes[0]
    
# Only import the module if not run from the setup script.
try:
    __FSPS_SETUP__
except NameError:
    __FSPS_SETUP__ = False
if not __FSPS_SETUP__:
    __all__ = ["StellarPopulation", "find_filter", "get_filter",
               "list_filters"]
    from .fsps import StellarPopulation
    from .filters import find_filter, get_filter, list_filters
