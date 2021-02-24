#!/usr/bin/env python3

"""
Created on 24 Feb 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The configuration utility is used to

SYNOPSIS
git_pull.py [-v]

EXAMPLES
./git_pull.py -vp

DOCUMENT EXAMPLE
{"pulled-on": "2021-02-24T17:35:08Z", "success": true,
"installed": ["scs_core", "scs_dev", "scs_dfe_eng", "scs_host_cpc", "scs_mfr", "scs_psu"],
"updated": ["scs_core", "scs_dev", "scs_dfe_eng", "scs_host_cpc", "scs_mfr", "scs_psu"]}

FILES
~/SCS/conf/git_pull.json
"""

import os
import sys

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.estate.git_pull import GitPull

from scs_core.sys.logging import Logging

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_git_pull import CmdGitPull


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    pulled = []
    success = True

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdGitPull()

    # logging...
    Logging.config('git_pull', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    start = LocalizedDatetime.now()

    root = Host.scs_path()
    installed = GitPull.dirs(root)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    try:
        if cmd.pull:
            for repo in installed:
                if GitPull.excludes(repo):
                    logger.info("%s: excluded - skipping" % repo)
                    continue

                path = os.path.join(root, repo)

                if not GitPull.is_clone(path):
                    logger.error("%s: not a git clone - skipping" % repo)
                    success = False
                    continue

                try:
                    logger.info(repo)
                    repo_success, stdout, stderr = GitPull.pull_repo(path, cmd.timeout)

                    if cmd.verbose:
                        print(stdout, end='')
                        print(stderr, end='', file=sys.stderr)

                    if not repo_success:
                        logger.error("%s: pull failed" % repo)
                        success = False
                        continue

                except TimeoutError:
                    logger.error("%s: timed out" % repo)
                    success = False
                    continue

                pulled.append(repo)

            git = GitPull(start, success, installed, pulled)
            git.save(Host)

        else:
            git = GitPull.load(Host, default=None)

        print(JSONify.dumps(git))

    except KeyboardInterrupt:
        print(file=sys.stderr)
