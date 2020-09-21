"""
Created on 21 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)

DESCRIPTION
The aws_group_setup utility is designed to automate the creation of AWS Greengrass groups using South Coast Science's configuration

The group must already exist and the ML lambdas must be associated with the greengrass account for which the IAM auth keys are given

SYNOPSIS
aws_group_setup.py [{ [-a AWS_Group_Name] [-c] | -m }] [-v]

EXAMPLES
./aws_group_setup.py -a scs-test-001-group -m

FILES
A conf file is placed in a default directory referencing the group name and when it was created

https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrass.html
"""


import sys
from getpass import getpass

import boto3

from scs_host.sys.host import Host
from scs_mfr.aws_group_configurator import AWSGroupConfigurator
from scs_mfr.aws_json_reader import AWSJsonReader
from scs_mfr.cmd.cmd_aws_group_setup import CmdAWSGroupSetup


# --------------------------------------------------------------------------------------------------------------------


def create_aws_client():
    access_key_secret = ""
    access_key_id = input("Enter AWS Access Key ID or leave blank to use environment variables: ")
    if access_key_id:
        access_key_secret = getpass(prompt="Enter Secret AWS Access Key: ")

    if access_key_id and access_key_secret:
        client = boto3.client(
            'greengrass',
            aws_access_key_id=access_key_id,
            aws_secret_access_key=access_key_secret,
            region_name='us-west-2'
        )
    else:
        client = boto3.client('greengrass')
    return client


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
    # run...
    if not cmd.is_valid():
        print("aws_group_setup: Invalid options ", file=sys.stderr)
        cmd.print_help(sys.stderr)
        exit(1)
    use_ml = True if cmd.use_ml else False
    aws_group = cmd.aws_group_name

    # ClientAuth...
    awsGroupConf = AWSGroupConfigurator.load(Host)

    if cmd.set():
        if awsGroupConf:
            user_choice = input("Group configuration already exists. Type Yes to update: ")
            print("")
            if not user_choice.lower() == "yes":
                print("Operation cancelled")
                exit()

        aws_configurator = AWSGroupConfigurator(aws_group, create_aws_client(), use_ml)
        aws_configurator.collect_information()
        aws_configurator.define_aws_group_resources()
        aws_configurator.define_aws_group_functions()
        aws_configurator.define_aws_group_subscriptions()
        aws_configurator.create_aws_group_definition()
        aws_configurator.save(Host)

    if cmd.show_current:
        aws_json_reader = AWSJsonReader(aws_group, create_aws_client())
        aws_json_reader.get_group_info_from_name()
        aws_json_reader.get_group_arns()
        aws_json_reader.output_current_info()

    # ----------------------------------------------------------------------------------------------------------------
