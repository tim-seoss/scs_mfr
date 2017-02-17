#!/usr/bin/env python3

"""
Created on 16 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./scs_mfr/osio_topic_create.py /orgs/south-coast-science-dev/test/1/status -n "test" -d "test of status" -s 28 -v
"""

import sys

from scs_core.osio.data.topic import Topic
from scs_core.osio.data.topic_info import TopicInfo
from scs_core.osio.manager.topic_manager import TopicManager
from scs_core.osio.client.api_auth import APIAuth

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_osio_topic_create import CmdOSIOTopicCreate


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdOSIOTopicCreate()

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

    topic_info = TopicInfo(TopicInfo.FORMAT_JSON, None, None, None)         # for the v2 API, schema_id goes in Topic

    topic = Topic(cmd.path, cmd.name, cmd.description, True, True, topic_info, cmd.schema_id)

    if cmd.verbose:
        print(topic, file=sys.stderr)

    success = manager.create(topic)

    if cmd.verbose:
        print("created: %s" % success, file=sys.stderr)
