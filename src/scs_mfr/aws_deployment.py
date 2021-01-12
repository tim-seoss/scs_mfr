#!/usr/bin/env python3

"""
Created on 11 Jan 2021

@author: Jade Page (jade.page@southcoastscience.com)

Usage:
Run script
"""

import socket
import sys

from scs_core.aws.greengrass.aws_deployment import AWSGroupDeployer
from scs_core.data.json import JSONify

from scs_mfr.cmd.cmd_aws_deployment import CMDAWSDeployment


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CMDAWSDeployment()

    # ----------------------------------------------------------------------------------------------------------------
    # run...

    group_name = socket.gethostname() + "-group"
    deployer = AWSGroupDeployer(group_name)
    result = None

    try:
        result = deployer.deploy()
    except KeyError:
        print("aws_group_deployment: group may not have been configured.", file=sys.stderr)
        exit(1)

    if cmd.verbose:
        if cmd.indent:
            print(JSONify.dumps(result, indent=cmd.indent))
        else:
            print(JSONify.dumps(result))
