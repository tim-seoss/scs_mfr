#!/usr/bin/env python3

"""
Created on 09 Oct 2020
@author: Jade Page (jade.page@southcoastscience.com)

DESCRIPTION
The aws_identity script allows the user to change the identity of an already-configured greengrass install,
in our use case it is to change the greengrass identity of a device which was setup using a cloned
base image without having to reinstall the greengrass software

The script could also be used to setup a "blank" greengrass install, which does not already have an identity, but
does already have the greengrass software.

If no group name is provided, the host name will be read from the device to generate it.
If no core name is provided, the host name will be read from the device to generate it.
If the set flag is not provided, the current identity will be read from the persistent file.

SYNOPSIS
aws_identity.py [-s] [-g GROUP_NAME] [-c CORE_NAME] [-v]

EXAMPLES
./aws_identity.py -s -g scs-test-003-group -c scs-test-003-core -v

FILES
A persistent file is placed in the conf directory when the identity is set, so that it can be read again later.

SEE ALSO
scs_mfr/aws_deployment.py
scs_mfr/aws_group_setup.py

REFERENCES
Created with reference to amazon's own device setup script (URL may change if updated)
https://d1onfpft10uf5o.cloudfront.net/greengrass-device-setup/downloads/gg-device-setup-latest.sh
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot.html
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html

NOTES
ATS_ROOT_CA_RSA_2048_REMOTE_LOCATION in core.aws.greengrass aws_identity is a certificate provided by
amazon itself and may be subject to change e.g. via obsolescence - check here:
https://docs.aws.amazon.com/iot/latest/developerguide/server-authentication.html
"""

import boto3
import json
import os
import sys

from scs_core.aws.client.access_key import AccessKey
from scs_core.aws.config.aws import AWS
from scs_core.aws.greengrass.aws_identity import AWSSetup

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_aws_identity import CmdAWSIdentity


# --------------------------------------------------------------------------------------------------------------------

def create_aws_clients():
    key = AccessKey.get()

    if key.ok():
        boto_iot_client = boto3.client(
            'iot',
            aws_access_key_id=key.id,
            aws_secret_access_key=key.secret,
            region_name=AWS.region()
        )
        boto_gg_client = boto3.client(
            'greengrass',
            aws_access_key_id=key.id,
            aws_secret_access_key=key.secret,
            region_name=AWS.region()
        )

    else:
        boto_iot_client = boto3.client('iot', region_name=AWS.region())
        boto_gg_client = boto3.client('greengrass', region_name=AWS.region())

    return boto_iot_client, boto_gg_client


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAWSIdentity()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("aws_identity: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()

    # ----------------------------------------------------------------------------------------------------------------
    # Check sudo

    if os.geteuid() != 0:
        print("aws_identity: you need to have root privileges to run this script.", file=sys.stderr)
        exit(1)

    # ----------------------------------------------------------------------------------------------------------------
    # resources

    # run...
    if cmd.setup:
        iot_client, gg_client = create_aws_clients()
        aws_setup = AWSSetup(iot_client, gg_client, AWS.core_name(), AWS.group_name())
        aws_setup.setup_device()
        aws_setup.save(Host)

    else:
        aws_setup = AWSSetup.load(Host)
        if aws_setup:
            json_file = aws_setup.as_json()
            print(json.dumps(json_file))
        else:
            print("aws_identity: no identity found.")
