#!/usr/bin/env python3

"""
Created on 18 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./scs_mfr/osio_publication.py -s /orgs/southcoastscience-dev/uk/test/loc/1 /orgs/southcoastscience-dev/uk/test/device -v
"""

import sys

from scs_core.data.json import JSONify
from scs_core.osio.config.publication import Publication
from scs_core.sys.device_id import DeviceID

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_osio_publication import CmdOSIOPublication


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdOSIOPublication()

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # resource...

    device_id = DeviceID.load_from_host(Host)

    if cmd.verbose:
        print(device_id, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        pub = Publication(cmd.location_path, cmd.device_path)
        pub.save(Host)

        # TODO: check for existence of topics / create as necessary

    else:
        pub = Publication.load_from_host(Host)

    print(JSONify.dumps(pub))

    if cmd.verbose:
        print("-", file=sys.stderr)
        print("climate_topic:      %s" % pub.climate_topic(), file=sys.stderr)
        print("particulates_topic: %s" % pub.particulates_topic(), file=sys.stderr)
        print("gasses_topic:       %s" % pub.gasses_topic(), file=sys.stderr)

        print("status_topic:       %s" % pub.status_topic(device_id), file=sys.stderr)
