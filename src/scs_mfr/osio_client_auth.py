#!/usr/bin/env python3

"""
Created on 18 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The osio_client_auth utility is used to store or read the client ID and client password required by the OpenSensors.io
Community Edition messaging system. This client authentication is required to both subscribe to and publish on any
messaging topic.

When setting the client authentication, the osio_client_auth utility requests a new device identity from the
OpenSensors.io system, then stores the generated tokens on the client. The name of the device is taken to be the
name of the host on which the script is executed. Names (unlike client IDs) are not required to be unique on the
OpenSensors system.

Note that the scs_mfr/osio_mqtt_client process must be restarted for changes to take effect.

SYNOPSIS
osio_client_auth.py [-u USER_ID] [-l LAT LNG POSTCODE] [-d DESCRIPTION] [-d DESCRIPTION] [-v]

EXAMPLES
./osio_client_auth.py -u south-coast-science-test-user -l 50.823204, -0.123005 "BN2 0DF" -v

FILES
~/SCS/osio/osio_client_auth.json

DOCUMENT EXAMPLE
{"user_id": "south-coast-science-test-user", "client-id": "5403", "client-password": "rtxSrK2f"}

SEE ALSO
scs_dev/osio_mqtt_client
scs_mfr/osio_api_auth
scs_mfr/osio_project
"""

import sys

from scs_core.data.json import JSONify

from scs_core.gas.afe_calib import AFECalib

from scs_core.osio.client.api_auth import APIAuth
from scs_core.osio.client.client_auth import ClientAuth
from scs_core.osio.config.project_source import ProjectSource
from scs_core.osio.manager.device_manager import DeviceManager
from scs_core.osio.manager.user_manager import UserManager

from scs_core.sys.system_id import SystemID

from scs_dfe.particulate.opc_conf import OPCConf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_osio_client_auth import CmdOSIOClientAuth


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdOSIOClientAuth()

    if cmd.verbose:
        print("osio_client_auth: %s" % cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # OPCConf...
    opc_conf = OPCConf.load(Host)

    if cmd.verbose:
        print("osio_client_auth: %s" % opc_conf, file=sys.stderr)

    # APIAuth...
    api_auth = APIAuth.load(Host)

    if api_auth is None:
        print("osio_client_auth: APIAuth not available.", file=sys.stderr)
        exit(1)

    if cmd.verbose:
        print("osio_client_auth: %s" % api_auth, file=sys.stderr)

    # SystemID...
    system_id = SystemID.load(Host)

    if system_id is None:
        print("osio_client_auth: SystemID not available.", file=sys.stderr)
        exit(1)

    if cmd.verbose:
        print("osio_client_auth: %s" % system_id, file=sys.stderr)

    # AFECalib...
    afe_calib = AFECalib.load(Host)

    if afe_calib is None:
        print("osio_client_auth: AFECalib not available.", file=sys.stderr)
        exit(1)

    if cmd.verbose:
        print("osio_client_auth: %s" % afe_calib, file=sys.stderr)
        sys.stderr.flush()

    # User manager...
    user_manager = UserManager(api_auth.api_key)

    # Device manager...
    device_manager = DeviceManager(api_auth.api_key)

    # check for existing registration...
    device = device_manager.find_for_name(api_auth.org_id, system_id.box_label())


    # ----------------------------------------------------------------------------------------------------------------
    # validate...

    # TODO: check whether remote device and local client auth match

    if device is None:
        if cmd.set() and not cmd.is_complete():
            print("osio_client_auth: No device is registered. You must therefore set a user and location.",
                  file=sys.stderr)
            cmd.print_help(sys.stderr)
            exit(1)

        if not cmd.set():
            exit(0)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        # User...
        if cmd.user_id:
            user = user_manager.find_public(cmd.user_id)

            if user is None:
                print("osio_client_auth: User not available.", file=sys.stderr)
                exit(1)

        # tags...
        include_particulates = bool(opc_conf is not None)
        tags = ProjectSource.tags(afe_calib, include_particulates)

        if device:
            if cmd.user_id:
                print("osio_client_auth: Device owner-id cannot be updated.", file=sys.stderr)
                exit(1)

            # find ClientAuth...
            client_auth = ClientAuth.load(Host)

            # update Device...
            updated = ProjectSource.update(device, cmd.lat, cmd.lng, cmd.postcode, cmd.description, tags)
            device_manager.update(api_auth.org_id, device.client_id, updated)

            # find updated device...
            device = device_manager.find(api_auth.org_id, device.client_id)

        else:
            # create Device...
            device = ProjectSource.create(system_id, api_auth, cmd.lat, cmd.lng, cmd.postcode, cmd.description, tags)
            device = device_manager.create(cmd.user_id, device)

            # create ClientAuth...
            client_auth = ClientAuth(cmd.user_id, device.client_id, device.password)

            client_auth.save(Host)

    else:
        # find ClientAuth...
        client_auth = ClientAuth.load(Host)

    if cmd.verbose:
        print(client_auth, file=sys.stderr)

    print(JSONify.dumps(device))
