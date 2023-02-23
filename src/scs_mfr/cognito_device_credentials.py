#!/usr/bin/env python3

"""
Created on 20 Apr 2022

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_mfr

DESCRIPTION
The cognito_device_credentials utility is used to test the validity of the Cognito identity for the device.

SYNOPSIS
Usage: cognito_device_credentials.py [-t] [-i INDENT] [-v]

EXAMPLES
./cognito_device_credentials.py -R

DOCUMENT EXAMPLE
{"username": "scs-opc-1", "password": "Ytzglk6oYpzJY0FB"}

SEE ALSO
scs_analysis/cognito_user_credentials
"""

import requests
import sys

from scs_core.aws.security.cognito_login_manager import CognitoDeviceLoginManager
from scs_core.aws.security.cognito_device import CognitoDeviceCredentials

from scs_core.data.json import JSONify

from scs_core.sys.http_exception import HTTPException
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

        logger.info(system_id)

        shared_secret = SharedSecret.load(Host)

        if not shared_secret:
            logger.error("SharedSecret not available.")
            exit(1)

        logger.info(shared_secret)

        credentials = CognitoDeviceCredentials(system_id.message_tag(), shared_secret.key)
        logger.info(credentials)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        if cmd.test:
            gatekeeper = CognitoDeviceLoginManager(requests)

            auth = gatekeeper.login(credentials)
            logger.info(auth)

            if auth is None:                            # TODO: fix
                logger.error("invalid auth.")
                exit(1)


        # ----------------------------------------------------------------------------------------------------------------
        # end...

        if credentials:
            print(JSONify.dumps(credentials))

    except KeyboardInterrupt:
        print(file=sys.stderr)

    except HTTPException as ex:
        logger.error(ex.data)
        exit(1)
