#!/usr/bin/env python3

"""
Created on 16 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./scs_mfr/osio_topic_delete.py -v /orgs/south-coast-science-dev/test/b/status
"""

import sys

from scs_core.osio.manager.topic_manager import TopicManager
from scs_core.osio.client.api_auth import APIAuth

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_osio_topic import CmdOSIOTopic


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdOSIOTopic()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit()

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # resource...

    http_client = HTTPClient()

    auth = APIAuth.load_from_host(Host)

    manager = TopicManager(http_client, auth.api_key)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    success = manager.delete(cmd.path)

    if cmd.verbose:
        print("deleted: %s" % success, file=sys.stderr)
