#!/usr/bin/env python3

"""
Created on 17 May 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The mqtt_conf utility is used to control the behaviour of MQTT client scripts. Currently, the only option is to inhibit
publishing - when set to true, the MQTT client will continue to accept messages and echo these to stdout if required,
but will not publish.

The setting is useful when the device is used in an offline mode - in this case data is typically written to a CSV file.

The MQTT client must be restarted for changes to take effect.

Warning: if inhibit publishing is set to true, the MQTT client will still subscribe as required, but will not publish
receipts or responses.

SYNOPSIS
mqtt_conf.py [-p INHIBIT_PUBLISHING] [-q QUEUE_SIZE] [-v]

EXAMPLES
./mqtt_conf.py -p0 -q21000

DOCUMENT EXAMPLE
{"inhibit-publishing": false, "queue-size": 22000}

FILES
~/SCS/conf/mqtt_conf.json

SEE ALSO
scs_dev/aws_mqtt_client
scs_dev/osio_mqtt_client
"""

import sys

from scs_core.comms.mqtt_conf import MQTTConf
from scs_core.data.json import JSONify

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_mqtt_conf import CmdMQTTConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdMQTTConf()

    if cmd.verbose:
        print("mqtt_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # OPCConf...
    conf = MQTTConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        inhibit_publishing = cmd.inhibit_publishing if cmd.inhibit_publishing is not None else conf.inhibit_publishing
        queue_size = cmd.queue_size if cmd.queue_size is not None else conf.queue_size

        if queue_size is None:
            queue_size = MQTTConf.DEFAULT_QUEUE_SIZE

        conf = MQTTConf(inhibit_publishing, queue_size)
        conf.save(Host)

    if conf:
        print(JSONify.dumps(conf))
