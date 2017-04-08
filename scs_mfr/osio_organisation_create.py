#!/usr/bin/env python3

"""
Created on 8 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Requires APIAuth document.

command line examples:
./scs_mfr/osio_organisation_create.py -v -o test-org-1 -n "Test Org 1" -w www.southcoastscience.com \
-d "a test organisation" -e test1@southcoastscience.com
"""

import sys

from scs_core.data.json import JSONify
from scs_core.osio.client.api_auth import APIAuth
from scs_core.osio.data.organisation import Organisation
from scs_core.osio.manager.organisation_manager import OrganisationManager

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_osio_organisation_create import CmdOSIOOrganisationCreate


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdOSIOOrganisationCreate()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit()

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # resource...

    api_auth = APIAuth.load_from_host(Host)

    if api_auth is None:
        print("APIAuth not available.", file=sys.stderr)
        exit()

    if cmd.verbose:
        print(api_auth, file=sys.stderr)


    http_client = HTTPClient()

    manager = OrganisationManager(http_client, api_auth.api_key)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    # create prototype...
    org = Organisation(cmd.org_id, cmd.name, cmd.website, cmd.description, cmd.email)

    # create device...
    manager.create(org)

    print(JSONify.dumps(org))
