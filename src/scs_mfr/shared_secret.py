#!/usr/bin/env python3

"""
Created on 2 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Part 3 of 3: Communication:

  > 1: ./shared_secret.py -g
    2: ./system_id.py -d VENDOR_ID -m MODEL_ID -n MODEL_NAME -c CONFIG -s SYSTEM_SERIAL_NUMBER -v
    3: ./osio_api_auth.py -s ORG_ID API_KEY
    4: ./osio_client_auth.py -u USER_ID -l LAT LNG POSTCODE
    5: ./osio_host_project.py -v -s GROUP LOCATION_ID

Creates or deletes SharedSecret document.

document example:
{"key": "sxBhncFybpbMwZUa"}

command line example:
./shared_secret.py -g
"""

import sys

from scs_core.data.json import JSONify

from scs_core.sys.shared_secret import SharedSecret

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_shared_secret import CmdSharedSecret


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdSharedSecret()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print(cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # SHTConf...
    secret = SharedSecret.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.generate:
        secret = SharedSecret(SharedSecret.generate())
        secret.save(Host)

    if cmd.delete and secret is not None:
        secret.delete(Host)
        secret = None

    if secret:
        print(JSONify.dumps(secret))
