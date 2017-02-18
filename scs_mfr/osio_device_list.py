#!/usr/bin/env python3

"""
Created on 18 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./scs_mfr/osio_device_list.py -u -v
"""

import sys

from scs_core.data.json import JSONify
from scs_core.osio.manager.device_manager import DeviceManager
from scs_core.osio.client.api_auth import APIAuth
from scs_core.osio.client.device_auth import DeviceAuth

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_osio_device_list import CmdOSIODeviceList


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdOSIODeviceList()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit()

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # resource...

    http_client = HTTPClient()

    api_auth = APIAuth.load_from_host(Host)

    if cmd.verbose:
        print(api_auth, file=sys.stderr)

    device_auth = DeviceAuth.load_from_host(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    manager = DeviceManager(http_client, api_auth.api_key)

    if cmd.org:
        devices = manager.find_all_for_org(api_auth.org_id)
    else:
        devices = manager.find_all_for_user(device_auth.username)

    for device in devices:
        print(JSONify.dumps(device))
