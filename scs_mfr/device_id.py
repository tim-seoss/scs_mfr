#!/usr/bin/env python3

"""
Created on 17 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

workflow 1 of 4:
Creates CmdDeviceID document.

command line example:
./scs_mfr/device_id.py -s Praxis BGB 123 -v
"""

import sys

from scs_core.data.json import JSONify
from scs_core.sys.device_id import DeviceID

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_device_id import CmdDeviceID


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdDeviceID()

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        id = DeviceID(cmd.model, cmd.configuration, cmd.serial_number)
        id.save(Host)
    else:
        id = DeviceID.load_from_host(Host)

    print(JSONify.dumps(id))

    if cmd.verbose:
        print("box:   %s" % id.box_label(), file=sys.stderr)
        print("topic: %s" % id.topic_label(), file=sys.stderr)
