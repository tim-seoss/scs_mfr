#!/usr/bin/env python3

"""
Created on 20 Apr 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_mfr

DESCRIPTION
The cognito_device_credentials utility is used to assert the device in the Cognito devices pool, or test the validity
of the Cognito identity for the device. The credentials are derived from the device system ID and shared secret.

In --assert and --test modes, the utility outputs the Cognito device record. Otherwise, the utility outputs the
credentials.

SYNOPSIS
Usage: cognito_device_credentials.py [{ -a | -t }] [-v]

EXAMPLES
./cognito_device_credentials.py -t

DOCUMENT EXAMPLE - CREDENTIALS
{"username": "scs-be2-3", "password": "################"}

DOCUMENT EXAMPLE - DEVICE
{"username": "scs-be2-3", "created": "2023-04-25T10:05:55Z", "last-updated": "2023-04-25T10:05:55Z"}

SEE ALSO
scs_mfr/shared_secret
scs_mfr/system_id
"""

import requests
import sys

from scs_core.aws.security.cognito_device import CognitoDeviceCredentials
from scs_core.aws.security.cognito_device_creator import CognitoDeviceCreator
from scs_core.aws.security.cognito_device_finder import CognitoDeviceIntrospector
from scs_core.aws.security.cognito_login_manager import CognitoLoginManager

from scs_core.client.http_exception import HTTPException, HTTPConflictException

from scs_core.data.json import JSONify

from scs_core.sys.logging import Logging
from scs_core.sys.shared_secret import SharedSecret
from scs_core.sys.system_id import SystemID

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_cognito_device_credentials import CmdCognitoDeviceCredentials


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    auth = None
    logger = None

    try:
        # ------------------------------------------------------------------------------------------------------------
        # cmd...

        cmd = CmdCognitoDeviceCredentials()

        Logging.config('cognito_device_credentials', verbose=cmd.verbose)
        logger = Logging.getLogger()

        logger.info(cmd)


        # ------------------------------------------------------------------------------------------------------------
        # auth...

        system_id = SystemID.load(Host)

        if not system_id:
            logger.error("SystemID not available.")
            exit(1)

        shared_secret = SharedSecret.load(Host)

        if not shared_secret:
            logger.error("SharedSecret not available.")
            exit(1)

        credentials = CognitoDeviceCredentials(system_id.message_tag(), shared_secret.key)
        logger.info(credentials)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        if cmd.assert_device:
            creator = CognitoDeviceCreator(requests)
            report = creator.create(credentials)

        elif cmd.test:
            gatekeeper = CognitoLoginManager(requests)
            auth = gatekeeper.device_login(credentials)

            if auth.is_ok():
                finder = CognitoDeviceIntrospector(requests)
                report = finder.find_self(auth.id_token)

            else:
                logger.error(auth.authentication_status.description)
                exit(1)

        else:
            report = credentials


        # ----------------------------------------------------------------------------------------------------------------
        # end...

        if credentials:
            print(JSONify.dumps(report))

    except KeyboardInterrupt:
        print(file=sys.stderr)

    except HTTPConflictException:
        logger.error("the device is already known to Cognito.")
        exit(1)

    except HTTPException as ex:
        logger.error(ex.data)
        exit(1)
