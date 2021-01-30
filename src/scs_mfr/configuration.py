#!/usr/bin/env python3

"""
Created on 29 Jan 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The configuration utility is used to

SYNOPSIS
configuration.py [-s CONFIGURATION] [-i INDENT] [-v]

EXAMPLES
./configuration.py -i4

DOCUMENT EXAMPLE
{"location-path": "south-coast-science-dev/development/loc/1",
"device-path": "south-coast-science-dev/development/device"}

FILES
~/SCS/aws/configuration.json

SEE ALSO
scs_dev/aws_mqtt_client
scs_mfr/aws_api_auth
scs_mfr/aws_client_auth
"""

from scs_core.data.json import JSONify
from scs_core.estate.configuration import Configuration
from scs_core.sys.logging import Logging

from scs_host.sys.host import Host

from cmd.cmd_configuration import CmdConfiguration


# --------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdConfiguration()

    # logging...
    Logging.config('configuration', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)

    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.save():
        conf = Configuration.construct_from_jstr(cmd.configuration)

        if conf is None:
            logger.error('invalid configuration: %s' % cmd.configuration)
            exit(1)

        conf.save(Host)

    conf = Configuration.load(Host)
    print(JSONify.dumps(conf, indent=cmd.indent))
