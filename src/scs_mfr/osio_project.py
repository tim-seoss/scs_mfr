#!/usr/bin/env python3

"""
Created on 18 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The osio_project utility is used to specify the topic path names for devices using the OpenSensors.io Community Edition
messaging infrastructure. For each device, topics are divided into two groups:

Location path, e.g.:

* /orgs/south-coast-science-dev/development/loc/1/climate
* /orgs/south-coast-science-dev/development/loc/1/gases
* /orgs/south-coast-science-dev/development/loc/1/particulates

Device path, e.g.:

* /orgs/south-coast-science-dev/development/device/alpha-pi-eng-000006/control
* /orgs/south-coast-science-dev/development/device/alpha-pi-eng-000006/status

Typically, the device paths should remain fixed throughout the lifetime of the device. In contrast, a given set of
location paths are used by the device only when it is installed at a given location.

The location ID must be an integer.

When the osio_project utility is executed, any topics required are created on the OpenSensors.io infrastructure.

When the "verbose" "-v" flag is used, the osio_project utility reports all of the topic paths derived from
its specification.

Note that the scs_mfr/osio_mqtt_client process must be restarted for changes to take effect.

SYNOPSIS
osio_project.py [-s GROUP LOCATION_ID] [-v]

EXAMPLES
./osio_client_auth.py -u south-coast-science-test-user -l 50.823204, -0.123005 "BN2 0DF" -v

DOCUMENT EXAMPLE
{"location-path": "/orgs/south-coast-science-dev/development/loc/3",
"device-path": "/orgs/south-coast-science-dev/development/device"}

FILES
~/SCS/osio/osio_project.json

SEE ALSO
scs_dev/osio_mqtt_client
scs_mfr/osio_api_auth
scs_mfr/osio_client_auth

BUGS
If a topic is deleted on the OpenSensors.io infrastructure, any future attempt to re-create it results in a
server error.
"""

import sys

from scs_core.data.json import JSONify

from scs_core.gas.afe_calib import AFECalib

from scs_core.osio.client.api_auth import APIAuth
from scs_core.osio.config.project import Project
from scs_core.osio.config.project_topic import ProjectTopic
from scs_core.osio.data.topic import Topic
from scs_core.osio.data.topic_info import TopicInfo
from scs_core.osio.manager.topic_manager import TopicManager

from scs_core.sys.system_id import SystemID

from scs_dfe.particulate.opc_conf import OPCConf

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_osio_project import CmdOSIOProject


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

        if topic:
            updated = Topic(None, schema.name, schema.description, topic.is_public, topic.info, None, None)

            self.__topic_manager.update(topic.path, updated)

        else:
            info = TopicInfo(TopicInfo.FORMAT_JSON, None, None, None)     # for the v2 API, schema_id goes in Topic
            constructed = Topic(path, schema.name, schema.description, True, info, True, schema.schema_id)

            self.__topic_manager.create(constructed)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "HostProject:{topic_manager:%s}" % self.__topic_manager


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdOSIOProject()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # OPCConf...
    opc_conf = OPCConf.load(Host)

    if cmd.verbose:
        print(opc_conf, file=sys.stderr)

    # APIAuth...
    api_auth = APIAuth.load(Host)

    if api_auth is None:
        print("osio_project: APIAuth not available.", file=sys.stderr)
        exit(1)

    if cmd.verbose:
        print(api_auth, file=sys.stderr)

    # SystemID...
    system_id = SystemID.load(Host)

    if system_id is None:
        print("osio_project: SystemID not available.", file=sys.stderr)
        exit(1)

    if cmd.verbose:
        print(system_id, file=sys.stderr)

    # AFECalib...
    afe_calib = AFECalib.load(Host)

    if afe_calib is None:
        print("osio_project: AFECalib not available.", file=sys.stderr)
        exit(1)

    if cmd.verbose:
        print(afe_calib, file=sys.stderr)
        sys.stderr.flush()

    # manager...
    manager = TopicManager(HTTPClient(), api_auth.api_key)

    creator = HostProject(manager)

    # gases schema...
    gases_topic = ProjectTopic.get_gases_topic(afe_calib.gas_names())


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    include_particulates = False if opc_conf is None else opc_conf.has_monitor()

    # set...
    if cmd.set():
        project = Project.construct(api_auth.org_id, cmd.group, cmd.location_id)

        # existing gases topic...
        existing_gases_topics = manager.find_for_org(api_auth.org_id, project.gases_topic_path())
        existing_gases_topic = existing_gases_topics[0] if len(existing_gases_topics) else None

        if existing_gases_topic and existing_gases_topic.schema_id != gases_topic.schema_id:
            print("warning: existing OpenSensors gases schema (%s) does not match device gases schema (%s)" %
                  (existing_gases_topic.schema_id, gases_topic.schema_id), file=sys.stderr)

        # set topics...
        creator.construct_topic(project.climate_topic_path(), ProjectTopic.CLIMATE)
        creator.construct_topic(project.gases_topic_path(), gases_topic)

        if include_particulates:
            creator.construct_topic(project.particulates_topic_path(), ProjectTopic.PARTICULATES)

        creator.construct_topic(project.status_topic_path(system_id), ProjectTopic.STATUS)
        creator.construct_topic(project.control_topic_path(system_id), ProjectTopic.CONTROL)

        project.save(Host)

    project = Project.load(Host)
    print(JSONify.dumps(project))

    # report...
    if cmd.verbose and project is not None:
        print("-", file=sys.stderr)

        print("     gases_project: %s" % gases_topic, file=sys.stderr)
        print("-", file=sys.stderr)

        found = manager.find(project.climate_topic_path())

        if found is not None:
            print("     climate_topic: %s" % found.path, file=sys.stderr)

        found = manager.find(project.gases_topic_path())

        if found is not None:
            print("       gases_topic: %s" % found.path, file=sys.stderr)

        if include_particulates:
            found = manager.find(project.particulates_topic_path())

            if found is not None:
                print("particulates_topic: %s" % found.path, file=sys.stderr)

        found = manager.find(project.status_topic_path(system_id))

        if found is not None:
            print("      status_topic: %s" % found.path, file=sys.stderr)

        found = manager.find(project.control_topic_path(system_id))

        if found is not None:
            print("     control_topic: %s" % found.path, file=sys.stderr)
