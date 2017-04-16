#!/usr/bin/env python3

"""
Created on 18 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

workflow:
  1: ./scs_mfr/system_id.py
  2: ./scs_mfr/osio_api_auth.py
> 3: ./scs_mfr/osio_device_create.py
  4: ./scs_mfr/osio_project.py

Requires APIAuth and SystemID documents.
Creates ClientAuth document.

command line examples:
./scs_mfr/osio_device_create.py -v -u south-coast-science-test-user \
 -l 50.823130 -0.122922 "BN2 0DA" -d "test 1"

./scs_mfr/osio_device_create.py -v -u south-coast-science-test-user \
-l 50.819456, -0.128336 "BN2 1AF" -d "BB dev platform"
"""

import sys

from scs_core.osio.client.api_auth import APIAuth
from scs_core.osio.client.client_auth import ClientAuth

from scs_core.osio.config.source import Source
from scs_core.osio.manager.device_manager import DeviceManager
from scs_core.sys.system_id import SystemID

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
    # resources...

    # APIAuth...
    api_auth = APIAuth.load_from_host(Host)

    if api_auth is None:
        print("APIAuth not available.", file=sys.stderr)
        exit()

    if cmd.verbose:
        print(api_auth, file=sys.stderr)

    # SystemID...
    system_id = SystemID.load_from_host(Host)

    if system_id is None:
        print("SystemID not available.", file=sys.stderr)
        exit()

    if cmd.verbose:
        print(system_id, file=sys.stderr)

    # manager...
    manager = DeviceManager(HTTPClient(), api_auth.api_key)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    # TODO: responses should be JSON...

    # create prototype...
    device = Source.create(system_id, api_auth, cmd.lat, cmd.lng, cmd.postcode, cmd.description)

    # create device...
    device = manager.create(cmd.user_id, device)
    print(device)

    # create client_auth...
    client_auth = ClientAuth(cmd.user_id, device.client_id, device.password)
    client_auth.save(Host)
    print(client_auth)
