#!/usr/bin/env python3

"""
Created on 21 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)

DESCRIPTION
The mqtt_peer_setup utility is designed to

SYNOPSIS
mqtt_peer_setup.py [-s TEMPLATE [-a AWS_GROUP_NAME] [-f]] [-k] [-i INDENT] [-v]

EXAMPLES
./mqtt_peer_setup.py -s oE.1 -a scs-test-001-group -f

EXAMPLE DOCUMENT
{"group-name": "scs-test-001-group", "time-initiated": "2021-09-21T13:00:31Z","unix-group": 987, "ml": "oE.1"}

FILES
~/SCS/aws/aws_group_config.json

SEE ALSO
scs_mfr/aws_deployment.py
scs_mfr/aws_identity.py
"""

import sys

from botocore.exceptions import ClientError, NoCredentialsError

from scs_core.aws.client.access_key import AccessKey
from scs_core.aws.client.client import Client
from scs_core.aws.config.aws import AWS
from scs_core.aws.greengrass.aws_group import AWSGroup
from scs_core.aws.greengrass.aws_group_configuration import AWSGroupConfiguration
from scs_core.aws.greengrass.gg_errors import ProjectMissingError

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.sys.logging import Logging

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_mqtt_peer_setup import CmdAWSGroupSetup


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    key = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAWSGroupSetup()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    # logging...
    Logging.config('mqtt_peer_setup', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)

    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    try:
        key = AccessKey.from_stdin() if cmd.stdin else AccessKey.from_user()
    except ValueError:
        logger.error('invalid key.')
        exit(1)

    except KeyboardInterrupt:
        print(file=sys.stderr)
        exit(0)

    client = Client.construct('greengrass', key)

    # AWSGroupConfigurator...
    conf = AWSGroupConfiguration.load(Host)
    logger.info(conf)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    try:
        if cmd.set is not None:
            if conf and not cmd.force:
                user_choice = input("Group configuration already exists. Type Yes to overwrite: ")
                if not user_choice.lower() == "yes":
                    exit(0)

            try:
                now = LocalizedDatetime.now()
                conf = AWSGroupConfiguration(AWS.group_name(), now, ml=cmd.set)
                configurator = conf.configurator(client)

                configurator.collect_information(Host)
                configurator.define_aws_group_resources(Host)
                configurator.define_aws_group_functions()
                configurator.define_aws_group_subscriptions()
                # configurator.define_aws_logger()
                configurator.create_aws_group_definition()

                conf.save(Host)

                print(JSONify.dumps(conf, indent=cmd.indent))

            except ClientError as error:
                if error.response['Error']['Code'] == 'BadRequestException':
                    logger.error("Invalid request.")

                if error.response['Error']['Code'] == 'InternalServerErrorException':
                    logger.error("AWS server error.")

            except ProjectMissingError:
                logger.error("Project configuration not set.")

        else:
            try:
                aws_group_info = AWSGroup(AWS.group_name(), client)

                aws_group_info.get_group_info_from_name()
                aws_group_info.get_group_arns()
                aws_group_info.output_current_info()

                print(JSONify.dumps(aws_group_info, indent=cmd.indent))

            except KeyError:
                logger.error("group may not have been configured.")

    except KeyboardInterrupt:
        print(file=sys.stderr)

    except (EOFError, NoCredentialsError):
        logger.error("credentials error.")
