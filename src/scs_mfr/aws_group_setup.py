"""
Created on 21 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)

DESCRIPTION The aws_group_setup utility is designed to automate the creation of AWS Greengrass groups using South
Coast Science's configuration

The group must already exist and the ML lambdas must be associated with the greengrass account for which the IAM auth
keys are given

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
from botocore.exceptions import ClientError

from scs_core.data.json import JSONify
from scs_host.sys.host import Host
from scs_core.aws.greengrass.aws_group_configurator import AWSGroupConfigurator
from scs_core.aws.greengrass.aws_json_reader import AWSGroup
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

    if cmd.verbose:
        print("aws_group_setup: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()

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
        try:
            aws_configurator = AWSGroupConfigurator(aws_group, create_aws_client(), use_ml)
            aws_configurator.collect_information(Host)
            aws_configurator.define_aws_group_resources(Host)
            aws_configurator.define_aws_group_functions()
            aws_configurator.define_aws_group_subscriptions()
            aws_configurator.create_aws_group_definition()
            aws_configurator.save(Host)
        except ClientError as error:
            if error.response['Error']['Code'] == 'BadRequestException':
                print("aws_json_reader: Invalid request.", file=sys.stderr)
            if error.response['Error']['Code'] == 'InternalServerErrorException':
                print("aws_json_reader: AWS server error.", file=sys.stderr)
            else:
                raise error

    if cmd.show_current:
        aws_json_reader = AWSGroup(aws_group, create_aws_client())
        aws_json_reader.__get_group_info_from_name()
        aws_json_reader.__get_group_arns()
        aws_json_reader.__output_current_info()
        print(JSONify.dumps(aws_json_reader))

    # ----------------------------------------------------------------------------------------------------------------
