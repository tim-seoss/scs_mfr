#!/usr/bin/env python3

"""
Created on 18 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./scs_mfr/osio_device_auth.py -v -s southcoastscience-dev 5406 jtxSrK2e
"""

import sys

from scs_core.data.json import JSONify
from scs_core.osio.client.api_auth import APIAuth

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_osio_api_auth import CmdOSIOAPIAuth


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdOSIOAPIAuth()

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        auth = APIAuth(cmd.org_id, cmd.api_key)
        auth.save(Host)

    else:
        auth = APIAuth.load_from_host(Host)

    print(JSONify.dumps(auth))
