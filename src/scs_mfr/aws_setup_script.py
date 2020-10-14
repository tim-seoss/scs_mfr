#!/usr/bin/env python3

"""
Created on 09 Oct 2020
@author: Jade Page (jade.page@southcoastscience.com)
"""

import boto3
import sys

from getpass import getpass

from scs_mfr.cmd.cmd_aws_setup import CmdAWSSetup
from scs_core.aws.greengrass.aws_setup_script import AWSSetup

# --------------------------------------------------------------------------------------------------------------------


def create_aws_clients():
    access_key_secret = ""
    access_key_id = input("Enter AWS Access Key ID or leave blank to use environment variables: ")
    if access_key_id:
        access_key_secret = getpass(prompt="Enter Secret AWS Access Key: ")

    if access_key_id and access_key_secret:
        iot_client = boto3.client(
            'iot',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=access_key_secret,
            region_name='us-west-2'
        )
        gg_client = boto3.client(
            'greengrass',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=access_key_secret,
            region_name='us-west-2'
        )
    else:
        iot_client = boto3.client('iot', region_name='us-west-2')#
        gg_client = boto3.client('greengrass', region_name='us-west-2')
    return iot_client, gg_client


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAWSSetup()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("aws_group_setup: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()
    # ----------------------------------------------------------------------------------------------------------------
    # resources
    group_name = cmd.group_name
    core_name = cmd.core_name
    # ----------------------------------------------------------------------------------------------------------------

    # run...
    iot_client, gg_client = create_aws_clients()
    aws_setup = AWSSetup(iot_client, gg_client, core_name, group_name)
    aws_setup.setup_device()

