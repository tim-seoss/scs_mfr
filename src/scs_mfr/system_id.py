#!/usr/bin/env python3

"""
Created on 17 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The system_id utility is used to specify the identity of a sensing device, as it appears on either the South Coast
Science / AWS or OpenSensors.io Community Edition messaging infrastructures.

The identity is also used to tag all environmental sensing records. It is therefore important that a device retains
a fixed identity throughout its lifetime.

When the "verbose" "-v" flag is used, the system_id utility reports all of the identity formats derived from
its specification.

SYNOPSIS
system_id.py [-d VENDOR_ID] [-m MODEL_ID] [-n MODEL_NAME] [-c CONFIG] [-s SYSTEM_SERIAL_NUMBER] [-v]

EXAMPLES
./system_id.py -v -d SCS -m BGX -n Praxis -c BGX -s 401

DOCUMENT EXAMPLE
{"vendor-id": "SCS", "model-id": "BGX", "model": "Praxis", "config": "BGX", "system-sn": 401}

FILES
~/SCS/conf/system_id.json

SEE ALSO
scs_dev/aws_topic_publisher
scs_dev/aws_topic_subscriber
scs_dev/osio_topic_publisher
scs_dev/osio_topic_subscriber
scs_dev/climate_sampler
scs_dev/gases_sampler
scs_dev/particulates_sampler
scs_dev/status_sampler
scs_dev/control_receiver
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
        print("system_id: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # check for existing document...
    system_id = SystemID.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        if system_id is None and not cmd.is_complete():
            print("system_id: No ID is present - you must therefore set all fields.", file=sys.stderr)
            cmd.print_help(sys.stderr)
            exit(2)

        vendor_id = system_id.vendor_id if cmd.vendor_id is None else cmd.vendor_id
        model_id = system_id.model_id if cmd.model_id is None else cmd.model_id
        model_name = system_id.model_name if cmd.model_name is None else cmd.model_name
        configuration = system_id.configuration if cmd.configuration is None else cmd.configuration
        serial_number = system_id.system_serial_number if cmd.serial_number is None else cmd.serial_number

        system_id = SystemID(vendor_id, model_id, model_name, configuration, serial_number)
        system_id.save(Host)

    if system_id:
        print(JSONify.dumps(system_id))

    if cmd.verbose:
        print("-", file=sys.stderr)
        print("box:   %s" % system_id.box_label(), file=sys.stderr)
        print("topic: %s" % system_id.topic_label(), file=sys.stderr)
        print("tag:   %s" % system_id.message_tag(), file=sys.stderr)
