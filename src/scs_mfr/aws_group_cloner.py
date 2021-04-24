#!/usr/bin/env python3

"""
Created on 21 Jan 2021


@author: Jade Page (jade.page@southcoastscience.com)
"""

import sys

from botocore.exceptions import ClientError

from scs_core.aws.client.access_key import AccessKey
from scs_core.aws.client.client import Client
from scs_core.aws.greengrass.aws_deployment_reporter import AWSDeploymentReporter
from scs_core.aws.greengrass.aws_group_clone import AWSGroupCloner

from scs_core.sys.logging import Logging

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_aws_group_cloner import CmdAWSGroupCloner

# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    cmd = CmdAWSGroupCloner()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    # logging...
    Logging.config('aws_group_cloner', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        key = None

        try:
            key = AccessKey.from_user()
        except ValueError:
            logger.error('invalid key.')
            exit(1)

        client = Client.construct('greengrass', key)
        reporter = AWSDeploymentReporter(client)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # get latest deployment
        cloner = AWSGroupCloner(cmd.group_name, cmd.dest, client, cmd.gas, cmd.parts)

        valid_names = cloner.validate_names()
        if not valid_names:
            logger.error("Inputs are not SCS valid group names")
            exit(2)

        res = cloner.run(Host)
        if not res:
            logger.error("There was an error")
            exit(2)


    # ------------------------------------------------------------------------------------------------------------
    # end...

    except ClientError as ex:
        logger.error(ex)

    except KeyboardInterrupt:
        print(file=sys.stderr)

