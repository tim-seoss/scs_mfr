#!/usr/bin/env python3

"""
Created on 18 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

workflow:
  1: ./scs_mfr/system_id.py
  2: ./scs_mfr/api_auth.py
  3: ./scs_mfr/host_device.py
> 4: ./scs_mfr/host_project.py

Requires APIAuth, SystemID and AFECalib documents.
Creates Project document.

Warning: schema IDs are not updated when an existing topic is updated - create a new topic instead. 

command line example:
./scs_mfr/host_project.py -v -s field-trial 2
"""

import sys

from scs_core.data.json import JSONify
from scs_core.osio.client.api_auth import APIAuth
from scs_core.osio.config.project import Project
from scs_core.osio.config.project_schema import ProjectSchema
from scs_core.osio.data.topic import Topic
from scs_core.osio.data.topic_info import TopicInfo
from scs_core.osio.manager.topic_manager import TopicManager
from scs_core.sys.system_id import SystemID

from scs_dfe.gas.afe_calib import AFECalib

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_host_project import CmdHostProject


# --------------------------------------------------------------------------------------------------------------------

class HostProject(object):
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

    def construct_topic(self, path, schema):
        topic = self.__topic_manager.find(path)

        print("-")

        if topic:
            print("topic already exists: %s" % path)

            updated = Topic(None, schema.name, schema.description, topic.is_public, topic.info, None, None)
            print(updated)

            self.__topic_manager.update(topic.path, updated)

        else:
            info = TopicInfo(TopicInfo.FORMAT_JSON, None, None, None)     # for the v2 API, schema_id goes in Topic
            topic = Topic(path, schema.name, schema.description, True, True, info, schema.schema_id)
            print(topic)

            self.__topic_manager.create(topic)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "HostProject:{topic_manager:%s}" % self.__topic_manager


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdHostProject()

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # APIAuth...
    auth = APIAuth.load_from_host(Host)

    if auth is None:
        print("APIAuth not available.", file=sys.stderr)
        exit()


    # SystemID...
    system_id = SystemID.load_from_host(Host)

    if system_id is None:
        print("SystemID not available.", file=sys.stderr)
        exit()

    if cmd.verbose:
        print(system_id, file=sys.stderr)


    # AFECalib...
    afe_calib = AFECalib.load_from_host(Host)

    if afe_calib is None:
        print("AFECalib not available.", file=sys.stderr)
        exit()

    if cmd.verbose:
        print(afe_calib, file=sys.stderr)


    # manager...
    manager = TopicManager(HTTPClient(), auth.api_key)

    creator = HostProject(manager)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        project = Project.construct(auth.org_id, cmd.group, cmd.location_id)

        gases_schema = ProjectSchema.find_gas_schema(afe_calib.gas_names())

        creator.construct_topic(project.climate_topic_path(), ProjectSchema.CLIMATE)
        creator.construct_topic(project.gases_topic_path(), gases_schema)
        creator.construct_topic(project.particulates_topic_path(), ProjectSchema.PARTICULATES)
        creator.construct_topic(project.status_topic_path(system_id), ProjectSchema.STATUS)
        creator.construct_topic(project.control_topic_path(system_id), ProjectSchema.CONTROL)

        project.save(Host)

    project = Project.load_from_host(Host)
    print(JSONify.dumps(project))

    if cmd.verbose:
        print("-", file=sys.stderr)
        print("climate_topic:      %s" % project.climate_topic_path(), file=sys.stderr)
        print("gases_topic:        %s" % project.gases_topic_path(), file=sys.stderr)
        print("particulates_topic: %s" % project.particulates_topic_path(), file=sys.stderr)

        print("status_topic:       %s" % project.status_topic_path(system_id), file=sys.stderr)
        print("control_topic:      %s" % project.control_topic_path(system_id), file=sys.stderr)
