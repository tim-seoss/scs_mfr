#!/usr/bin/env python3

"""
Created on 17 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

workflow:
  1: ./afe_calib -s SERIAL_NUMBER
> 2: ./system_id.py -s VENDOR_ID MODEL_ID MODEL_NAME CONFIG SYSTEM_SERIAL
  3: ./api_auth.py -s ORG_ID API_KEY
  4: ./host_device.py -s -u USER_ID -l LAT LNG POSTCODE -p
  5: ./host_project.py -s GROUP LOCATION_ID -p

Creates SystemID document.

command line example:
./system_id.py -v -s Praxis BGB 2
"""

import sys

from scs_core.data.json import JSONify
from scs_core.sys.system_id import SystemID

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_system_id import CmdSystemID


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdSystemID()

    if cmd.verbose:
        print(cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        system_id = SystemID(cmd.vendor_id, cmd.model_id, cmd.model_name, cmd.configuration, cmd.serial_number)
        system_id.save(Host)
    else:
        system_id = SystemID.load_from_host(Host)

    print(JSONify.dumps(system_id))

    if cmd.verbose and id is not None:
        print("-", file=sys.stderr)
        print("box:   %s" % system_id.box_label(), file=sys.stderr)
        print("topic: %s" % system_id.topic_label(), file=sys.stderr)
        print("tag:   %s" % system_id.message_tag(), file=sys.stderr)
