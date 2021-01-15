#!/usr/bin/env python3

"""
Created on 11 Jan 2021

@author: Jade Page (jade.page@southcoastscience.com)

DESCRIPTION
The aws_group_deployment utility is used to invoke a deployment by the AWS cloud to the device. The deployment
configuration should already be in place - see aws_identity.py and aws_group_setup.py.

The greengrass service must be running for the deployment to complete.

SYNOPSIS
aws_deployment.py [-k] [-w] [-i INDENT] [-v]

EXAMPLES
./aws_deployment.py -vw

DOCUMENT EXAMPLE - OUTPUT
{"ResponseMetadata": {"RequestId": "72fce673", "HTTPStatusCode": 200,
"HTTPHeaders": {"date": "Fri, 15 Jan 2021 11:50:15 GMT", "content-type": "application/json", "content-length": "220",
"connection": "keep-alive", "x-amzn-requestid": "72fce673", "x-amzn-greengrass-trace-id": "Root=1-60018176",
"x-amz-apigw-id": "ZMEqkE-KvHcFibw=", "x-amzn-trace-id": "Root=1-60018176"}, "RetryAttempts": 0},
"DeploymentArn": "arn:aws:greengrass:us-west-2:696437392763:/greengrass/groups//deployments/cb645f98-7737",
"DeploymentId": "cb645f98-7737"}

SEE ALSO
scs_mfr/aws_group_setup.py
scs_mfr/aws_identity.py
"""

import sys
import time

from botocore.exceptions import NoCredentialsError

from scs_core.aws.client.access_key import AccessKey
from scs_core.aws.client.client import Client
from scs_core.aws.config.aws import AWS
from scs_core.aws.greengrass.aws_deployer import AWSGroupDeployer

from scs_core.data.json import JSONify

from scs_mfr.cmd.cmd_aws_deployment import CMDAWSDeployment


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    response = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CMDAWSDeployment()

    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    key = AccessKey.from_stdin() if cmd.stdin else AccessKey.from_user()
    client = Client.construct('greengrass', key)

    # AWSGroupDeployer...
    deployer = AWSGroupDeployer(AWS.group_name(), client)

    if cmd.verbose:
        print(deployer, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    try:
        # run...
        try:
            response = deployer.deploy()
        except KeyError:
            print("aws_group_deployment: group may not have been configured.", file=sys.stderr)
            exit(1)

        if cmd.verbose:
            if cmd.indent:
                print(JSONify.dumps(response, indent=cmd.indent))
            else:
                print(JSONify.dumps(response))

        # wait...
        while True:
            status = deployer.status(response)

            if status == AWSGroupDeployer.FAILURE:
                print("aws_group_deployment: deployment failed.", file=sys.stderr)
                exit(1)

            if cmd.verbose:
                print("aws_group_deployment: %s" % status, file=sys.stderr)

            if not cmd.wait or status == AWSGroupDeployer.SUCCESS:
                break

            time.sleep(5.0)

    except KeyboardInterrupt:
        print(file=sys.stderr)

    except (EOFError, NoCredentialsError):
        print("aws_group_deployment: credentials error.", file=sys.stderr)
        exit(1)
