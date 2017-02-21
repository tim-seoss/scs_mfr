#!/usr/bin/env python3

"""
Created on 18 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

workflow 3 of 4:
Requires APIAuth and DeviceID documents.
Creates ClientAuth document.

command line examples:
./scs_mfr/osio_device_create.py -u southcoastscience-dev -l 50.823130 -0.122922 "BN2 0DA" -d "test 1" -v
./scs_mfr/osio_device_create.py -u southcoastscience-dev -l 50.819456, -0.128336 "BN2 1AF" -d "BB development platform" -v
"""

import sys

from scs_core.osio.client.api_auth import APIAuth
from scs_core.osio.client.client_auth import ClientAuth

from scs_core.osio.config.source import Source
from scs_core.osio.manager.device_manager import DeviceManager
from scs_core.sys.device_id import DeviceID

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_osio_device_create import CmdOSIODeviceCreate


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdOSIODeviceCreate()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit()

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # resource...

    api_auth = APIAuth.load_from_host(Host)

    if api_auth is None:
        print("APIAuth not available.")
        exit()

    if cmd.verbose:
        print(api_auth, file=sys.stderr)


    device_id = DeviceID.load_from_host(Host)

    if device_id is None:
        print("DeviceID not available.")
        exit()

    if cmd.verbose:
        print(device_id, file=sys.stderr)


    http_client = HTTPClient()

    manager = DeviceManager(http_client, api_auth.api_key)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    # create prototype...
    device = Source.device(device_id, api_auth, cmd.lat, cmd.lng, cmd.postcode, cmd.description)

    # create device...
    device = manager.create(cmd.user_id, device)
    print(device)

    # create client_auth...
    client_auth = ClientAuth(cmd.user_id, device.client_id, device.password)
    client_auth.save(Host)
    print(client_auth)
