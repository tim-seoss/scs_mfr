#!/usr/bin/env python3

"""
Created on 18 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./scs_mfr/osio_topic_create.py /orgs/south-coast-science-dev/test/1/status -n "test" -d "test of status" -s 28 -v
"""

import sys

from scs_core.data.json import JSONify
from scs_core.osio.client.device_auth import DeviceAuth

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_osio_device_auth import CmdOSIODeviceAuth


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdOSIODeviceAuth()

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        auth = DeviceAuth(cmd.username, cmd.client_id, cmd.client_password)
        auth.save(Host)

    else:
        auth = DeviceAuth.load_from_host(Host)

    print(JSONify.dumps(auth))
