#!/usr/bin/env python3

"""
Created on 14 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./scs_mfr/osio_topic_list.py -p /orgs/south-coast-science-dev/uk -v
"""

import sys

from scs_core.data.json import JSONify
from scs_core.osio.manager.schema_manager import SchemaManager
from scs_core.osio.client.api_auth import APIAuth

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_osio_schema_list import CmdOSIOSchemaList


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdOSIOSchemaList()

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # resource...

    http_client = HTTPClient()

    auth = APIAuth.load_from_host(Host)

    if cmd.verbose:
        print(auth, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    manager = SchemaManager(http_client, auth.api_key)

    schemas = manager.find_all()

    for schema in schemas:
        print(JSONify.dumps(schema))
