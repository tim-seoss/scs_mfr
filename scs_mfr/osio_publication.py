#!/usr/bin/env python3

"""
Created on 18 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Requires APIAuth and DeviceID documents.

command line example:
./scs_mfr/osio_publication.py -s uk/test/loc/1 uk/test/device -v
"""

import sys

from scs_core.data.json import JSONify
from scs_core.osio.client.api_auth import APIAuth
from scs_core.osio.config.publication import Publication
from scs_core.osio.manager.topic_manager import TopicManager
from scs_core.sys.device_id import DeviceID

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_osio_publication import CmdOSIOPublication


# --------------------------------------------------------------------------------------------------------------------

class TopicCreator(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic_manager):
        """
        Constructor
        """
        self.__topic_manager = topic_manager


    # ----------------------------------------------------------------------------------------------------------------

    def construct_topic(self, path, name, description, schema_id):
        topic = self.__topic_manager.find(path)

        if topic:
            print("Warning: topic already exists: %s")
            # TODO: update topic with field params
            return

        success = self.__topic_manager.create()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TopicCreator:{topic_manager:%s}" % self.__topic_manager


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdOSIOPublication()

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # resource...

    http_client = HTTPClient()

    auth = APIAuth.load_from_host(Host)

    if auth is None:
        print("APIAuth not available.")
        exit()

    manager = TopicManager(http_client, auth.api_key)

    device_id = DeviceID.load_from_host(Host)

    if device_id is None:
        print("DeviceID not available.")
        exit()

    if cmd.verbose:
        print(device_id, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        pub = Publication.construct(auth.org_id, cmd.location_path, cmd.device_path)
        pub.save(Host)      # TODO: only save if successful

        # TODO: check for existence of topics / create as necessary

    else:
        pub = Publication.load_from_host(Host)

    print(JSONify.dumps(pub))

    climate_topic = pub.climate_topic()
    gasses_topic = pub.gasses_topic()
    particulates_topic = pub.particulates_topic()

    status_topic = pub.status_topic(device_id)
    control_topic = pub.control_topic(device_id)


    if cmd.verbose:
        print("-", file=sys.stderr)
        print("climate_topic:      %s" % climate_topic, file=sys.stderr)
        print("gasses_topic:       %s" % gasses_topic, file=sys.stderr)
        print("particulates_topic: %s" % particulates_topic, file=sys.stderr)

        print("status_topic:       %s" % status_topic, file=sys.stderr)
        print("control_topic:      %s" % control_topic, file=sys.stderr)

    topic = manager.find(gasses_topic)
    print(topic)
