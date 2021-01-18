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
aws_identity.py [-s] [-g GROUP_NAME] [-c CORE_NAME] [-k] [-v]

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

root@scs-cube-116:/etc/systemd/system# cat ~scs/SCS/aws/plain_access_key.json | aws_identity -sk
Logger created
Core created
Cert created
Core attached
Traceback (most recent call last):
  File "/home/scs/SCS/scs_mfr/src/scs_mfr/aws_identity.py", line 98, in <module>
    aws_setup.setup_device()
  File "/home/scs/SCS/scs_core/src/scs_core/aws/greengrass/aws_identity.py", line 72, in setup_device
    self.create_thing()
  File "/home/scs/SCS/scs_core/src/scs_core/aws/greengrass/aws_identity.py", line 106, in create_thing
    policyDocument=json.dumps(policy_doc)
  File "/usr/lib/python3/dist-packages/botocore/client.py", line 357, in _api_call
    return self._make_api_call(operation_name, kwargs)
  File "/usr/lib/python3/dist-packages/botocore/client.py", line 661, in _make_api_call
    raise error_class(parsed_response, operation_name)
botocore.errorfactory.ResourceAlreadyExistsException: An error occurred (ResourceAlreadyExistsException) when calling the CreatePolicy operation: Policy cannot be created - name already exists (name=scs-cube-116-core_basic_policy)
"""

import json
import os
import sys

from botocore.exceptions import NoCredentialsError

from scs_core.aws.client.access_key import AccessKey
from scs_core.aws.client.client import Client
from scs_core.aws.config.aws import AWS
from scs_core.aws.greengrass.aws_identity import AWSSetup

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_aws_identity import CmdAWSIdentity


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    key = None

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

    try:
        key = AccessKey.from_stdin() if cmd.stdin else AccessKey.from_user()
    except ValueError:
        print("aws_identity: invalid key.", file=sys.stderr)
        exit(1)

    # ----------------------------------------------------------------------------------------------------------------
    # run...

    try:
        if cmd.setup:
            iot_client = Client.construct('iot', key)
            gg_client = Client.construct('greengrass', key)

            aws_setup = AWSSetup(iot_client, gg_client, AWS.core_name(), AWS.group_name())
            aws_setup.setup_device()
            aws_setup.save(Host)

        else:
            aws_setup = AWSSetup.load(Host)

            if aws_setup:
                json_file = aws_setup.as_json()
                print(json.dumps(json_file))
            else:
                print("aws_identity: no identity found.", file=sys.stderr)

    except KeyboardInterrupt:
        print(file=sys.stderr)

    except (EOFError, NoCredentialsError):
        print("aws_identity: credentials error.", file=sys.stderr)
        exit(1)
