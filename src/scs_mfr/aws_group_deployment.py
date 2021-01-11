#!/usr/bin/env python3

"""
Created on 11 Jan 2021

@author: Jade Page (jade.page@southcoastscience.com)

Usage:
Run script
"""

# --------------------------------------------------------------------------------------------------------------------
import socket
import sys

from scs_core.aws.greengrass.aws_deployment import AWSGroupDeployer
from scs_core.data.json import JSONify
from scs_mfr.cmd.cmd_aws_group_deployment import CMDAWSDeployment


def return_group_name():
    host_name = socket.gethostname()
    return host_name + "-group"


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CMDAWSDeployment()

    # ----------------------------------------------------------------------------------------------------------------
    # run...
    group_name = return_group_name()
    deployer = AWSGroupDeployer(group_name)
    result = None

    try:
        result = deployer.deploy()
    except KeyError:
        print("Group may not have been configured", file=sys.stderr)

    if cmd.verbose:
        if cmd.indent:
            print(JSONify.dumps(result, indent=cmd.indent))
        else:
            print(JSONify.dumps(result))
