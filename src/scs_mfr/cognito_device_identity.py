#!/usr/bin/env python3

"""
Created on 24 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

source repo: scs_analysis

DESCRIPTION
The cognito_device_identity utility is used to retrieve or test the Cognito identity for the device.


SYNOPSIS
Usage: cognito_device_identity.py [-t] [-i INDENT] [-v]

EXAMPLES
./cognito_device_identity.py -R

DOCUMENT EXAMPLE
{"username": "8", "creation-date": "2021-11-24T12:51:12Z", "confirmation-status": "CONFIRMED", "enabled": true,
"email": "bruno.beloff@southcoastscience.com", "given-name": "Bruno", "family-name": "Beloff", "is-super": true}

SEE ALSO
scs_analysis/cognito_credentials

RESOURCES
https://docs.aws.amazon.com/cognito/latest/developerguide/signing-up-users-in-your-app.html
https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-settings-policies.html
"""

import requests
import sys

from scs_core.aws.security.cognito_device_finder import CognitoDeviceFinder
from scs_core.aws.security.cognito_login_manager import CognitoDeviceLoginManager
from scs_core.aws.security.cognito_device import CognitoDeviceCredentials, CognitoDeviceIdentity

from scs_core.data.json import JSONify

from scs_core.sys.http_exception import HTTPException
from scs_core.sys.logging import Logging
from scs_core.sys.shared_secret import SharedSecret
from scs_core.sys.system_id import SystemID

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_cognito_device_identity import CmdCognitoDeviceIdentity


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    logger = None
    gatekeeper = None
    credentials = None
    auth = None
    finder = None
    report = None

    try:
        # ------------------------------------------------------------------------------------------------------------
        # cmd...

        cmd = CmdCognitoDeviceIdentity()

        Logging.config('cognito_device_identity', verbose=cmd.verbose)
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

        gatekeeper = CognitoDeviceLoginManager(requests)

        try:
            auth = gatekeeper.login(credentials)

        except HTTPException as ex:
            logger.error(ex.data)
            exit(1)

        logger.info(auth)

        exit(0)

        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # finder = CognitoDeviceFinder(requests)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # report = finder.find_by_tag(auth.id_token, credentials.tag)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

        if credentials is not None:
            print(JSONify.dumps(credentials, indent=cmd.indent))

    except KeyboardInterrupt:
        print(file=sys.stderr)
