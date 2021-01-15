#!/usr/bin/env python3

"""
Created on 21 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)

DESCRIPTION
The aws_group_setup utility is designed to automate the creation of AWS Greengrass groups using South
Coast Science's configurations.

The group must already exist and the ML lambdas must be associated with the greengrass account for which the IAM auth
keys are given.

SYNOPSIS
aws_group_setup.py [-s [-m] [-a AWS_GROUP_NAME] [-f]] [-i INDENT] [-v]

EXAMPLES
./aws_group_setup.py -s -a scs-test-001-group -m

FILES
~/SCS/aws/aws_group_config.json

SEE ALSO
scs_mfr/aws_deployment.py
scs_mfr/aws_identity.py

RESOURCES
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html
"""

import boto3
import sys

from botocore.exceptions import ClientError

from scs_core.aws.client.access_key import AccessKey
from scs_core.aws.config.aws import AWS
from scs_core.aws.greengrass.aws_group import AWSGroup
from scs_core.aws.greengrass.aws_group_configurator import AWSGroupConfigurator
from scs_core.aws.greengrass.gg_errors import ProjectMissingError

from scs_core.data.json import JSONify

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_aws_group_setup import CmdAWSGroupSetup


# --------------------------------------------------------------------------------------------------------------------

def create_aws_client():
    key = AccessKey.get()

    if key.ok():
        return boto3.client(
            'greengrass',
            aws_access_key_id=key.id,
            aws_secret_access_key=key.secret,
            region_name=AWS.region()
        )

    return boto3.client('greengrass', region_name=AWS.region())


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAWSGroupSetup()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("aws_group_setup: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # AWSGroupConfigurator...
    conf = AWSGroupConfigurator.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set:
        if conf and not cmd.force:
            user_choice = input("Group configuration already exists. Type Yes to overwrite: ")
            if not user_choice.lower() == "yes":
                exit(0)

        try:
            aws_configurator = AWSGroupConfigurator(AWS.group_name(), create_aws_client(), cmd.use_ml)

            aws_configurator.collect_information(Host)
            aws_configurator.define_aws_group_resources(Host)
            aws_configurator.define_aws_group_functions()
            aws_configurator.define_aws_group_subscriptions()
            # aws_configurator.define_aws_logger()
            aws_configurator.create_aws_group_definition()
            aws_configurator.save(Host)

        except ClientError as error:
            if error.response['Error']['Code'] == 'BadRequestException':
                print("aws_group_setup: Invalid request.", file=sys.stderr)

            if error.response['Error']['Code'] == 'InternalServerErrorException':
                print("aws_group_setup: AWS server error.", file=sys.stderr)

        except ProjectMissingError:
            print("aws_group_setup: Project configuration not set.", file=sys.stderr)

    else:
        try:
            aws_group_info = AWSGroup(AWS.group_name(), create_aws_client())

            aws_group_info.get_group_info_from_name()
            aws_group_info.get_group_arns()
            aws_group_info.output_current_info()

            if cmd.indent:
                print(JSONify.dumps(aws_group_info, indent=cmd.indent))
            else:
                print(JSONify.dumps(aws_group_info))

        except KeyError:
            print("aws_group_setup: group may not have been configured", file=sys.stderr)
