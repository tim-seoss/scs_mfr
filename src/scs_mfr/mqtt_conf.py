#!/usr/bin/env python3

"""
Created on 17 May 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The mqtt_conf utility is used to control the behaviour of MQTT client scripts.

The INHIBIT_PUBLISHING field determines whether the MQTT client will publish messages. If inhibit is set to true,
then the client will continue to accept messages and echo these to stdout if required, but will not publish. This
setting is useful when the device is used in an offline mode - in this case data is typically written to a CSV file.

The QUEUE_SIZE field determines how many messages can be buffered before publication. Where a device is being used in
an environment with unreliable communications, this could potentially be a large number of messages - the
default queue size is 21000, equivalent to just over 24 hours of data under a normal sampling regime.

The REPORT_FILE parameter, if set, indicates where the latest queue length value should be stored.

The MQTT client must be restarted for changes to take effect.

Warning: if inhibit publishing is set to true, the MQTT client will still subscribe as required, but will not publish
receipts or responses.

SYNOPSIS
mqtt_conf.py { [-p INHIBIT_PUBLISHING] [-q QUEUE_SIZE] [-f REPORT_FILE]  | -d } [-v]

EXAMPLES
./mqtt_conf.py -p 0 -q 21000 -f /tmp/southcoastscience/mqtt_queue_length.json

DOCUMENT EXAMPLE
{"inhibit-publishing": false, "queue-size": 21000, "report-file": "/tmp/southcoastscience/mqtt_queue_length.json"}

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
        report_file = cmd.report_file if cmd.report_file is not None else conf.report_file

        if queue_size is None:
            queue_size = MQTTConf.DEFAULT_QUEUE_SIZE

        conf = MQTTConf(inhibit_publishing, queue_size, report_file)
        conf.save(Host)

    elif cmd.delete and conf is not None:
        conf.delete(Host)
        conf = None


    if conf:
        print(JSONify.dumps(conf))
