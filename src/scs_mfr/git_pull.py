#!/usr/bin/env python3

"""
Created on 24 Feb 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The configuration utility is used to

SYNOPSIS
git_pull.py [-v]

EXAMPLES
./git_pull.py -v
"""

import os
import sys

from subprocess import Popen, PIPE

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.sys.filesystem import Filesystem
from scs_core.sys.logging import Logging

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_verbose import CmdVerbose


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    excluded = ('scs_exegesis', )
    timeout = 1

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdVerbose()

    # logging...
    Logging.config('git_pull', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)

    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    root = Host.scs_path()
    repos = [item.name for item in Filesystem.ls(root) if item.name.startswith("scs_")]


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    try:
        for repo in repos:
            if repo in excluded:
                logger.info("'%s' is excluded - skipping" % repo)
                continue

            print(JSONify.dumps(repo))

            path = os.path.join(root, repo)
            contents = [item.name for item in Filesystem.ls(path)]

            if '.git' not in contents:
                logger.error("'%s' is not a git clone - skipping" % repo)
                continue

            p = Popen(['git', '-C', path, 'pull'], stdout=PIPE, stderr=PIPE)
            stdout_bytes, stderr_bytes = p.communicate(None, timeout)

            if cmd.verbose:
                print(stdout_bytes.decode(), end='')
                print(stderr_bytes.decode(), end='', file=sys.stderr)

            if p.returncode != 0:
                logger.error("'%s' pull return code: %d" % (repo, p.returncode))
                exit(1)

    except KeyboardInterrupt:
        print(file=sys.stderr)
