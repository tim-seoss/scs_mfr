#!/usr/bin/env python3

"""
Created on 09 Oct 2020
@author: Jade Page (jade.page@southcoastscience.com)

DESCRIPTION The aws_greengrass_identity script allows the user to change the identity of an already configured green-
grass install, in our use case it is to change the greengrass identity of a device which was setup using a cloned
base image without having to reinstall the greengrass software

The script could also be used to setup a "blank" greengrass install, which does not already have an identity, but
does already have the greengrass software

SYNOPSIS
aws_identity.py [{ [-s] [-g GROUP_NAME] [-c CORE_NAME] [-v] }]
If no group name is provided, the host name will be read from the device to generate it.
If no core name is provided, the host name will be read from the device to generate it.
If the set flag is not provided, the current identity will be read from the persistent file.

EXAMPLES
./aws_setup_script.py -s -g scs-test-003-group -c scs-test-003-core -v

FILES
A persistent file is placed in the conf directory when the identity is set, so that it can be read again later.

REFERENCES
Created with reference to amazon's own device setup script (URL may change if updated)
https://d1onfpft10uf5o.cloudfront.net/greengrass-device-setup/downloads/gg-device-setup-latest.sh
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html

NOTES
ATS_ROOT_CA_RSA_2048_REMOTE_LOCATION in core.aws.greengrass aws_greengrass_identity is a certificate provided by
amazon itself and may be subject to change e.g. via obsolescence - check here:
https://docs.aws.amazon.com/iot/latest/developerguide/server-authentication.html
"""

import boto3
import json
import os
import socket
import sys

from getpass import getpass

from scs_core.aws.greengrass.aws_identity import AWSSetup

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_aws_greengrass_identity import CmdAWSSetup


# --------------------------------------------------------------------------------------------------------------------

def create_aws_clients():
    access_key_secret = ""
    access_key_id = input("Enter AWS Access Key ID or leave blank to use environment variables: ")
    if access_key_id:
        access_key_secret = getpass(prompt="Enter Secret AWS Access Key: ")

    if access_key_id and access_key_secret:
        boto_iot_client = boto3.client(
            'iot',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=access_key_secret,
            region_name='us-west-2'
        )
        boto_gg_client = boto3.client(
            'greengrass',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=access_key_secret,
            region_name='us-west-2'
        )
    else:
        boto_iot_client = boto3.client('iot', region_name='us-west-2')  #
        boto_gg_client = boto3.client('greengrass', region_name='us-west-2')
    return boto_iot_client, boto_gg_client


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
        exit("You need to have root privileges to run this script.")

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
