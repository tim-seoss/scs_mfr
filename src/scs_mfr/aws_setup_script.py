#!/usr/bin/env python3

"""
Created on 09 Oct 2020
@author: Jade Page (jade.page@southcoastscience.com)
"""
import json
import os
import socket

import boto3
import sys

from getpass import getpass

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_aws_setup import CmdAWSSetup
from scs_core.aws.greengrass.aws_setup_script import AWSSetup

# --------------------------------------------------------------------------------------------------------------------


# noinspection PyShadowingNames
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
        iot_client = boto3.client('iot', region_name='us-west-2')  #
        gg_client = boto3.client('greengrass', region_name='us-west-2')
    return iot_client, gg_client


def return_group_name():
    host_name = socket.gethostname()
    return host_name + "-group"


def return_core_name():
    host_name = socket.gethostname()
    return host_name + "-core"


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
    # Check sudo
    if os.geteuid() != 0:
        exit("You need to have root privileges to run this script.\nPlease run with 'sudo'.")

    # ----------------------------------------------------------------------------------------------------------------
    # resources
    group_name = cmd.group_name if cmd.group_name else return_group_name()
    core_name = cmd.core_name if cmd.core_name else return_core_name()

    # ----------------------------------------------------------------------------------------------------------------

    # run...
    if cmd.setup:
        iot_client, gg_client = create_aws_clients()
        aws_setup = AWSSetup(iot_client, gg_client, core_name, group_name)
        aws_setup.setup_device()
        aws_setup.save(Host)
    else:
        aws_setup = AWSSetup.load(Host)
        if aws_setup:
            json_file = aws_setup.as_json()
            print(json.dumps(json_file))
        else:
            print("No identity found")

# --------------------------------------------------------------------------------------------------------------------
