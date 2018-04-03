#!/usr/bin/env python3

"""
Created on 3 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
xxx

EXAMPLES
./aws_client_auth.py -e asrft7e5j5ecz.iot.us-west-2.amazonaws.com -c bruno -i 9f08402232

FILES
~/SCS/aws/aws_client_auth.json

~/SCS/aws/certs/XXX-certificate.pem.crt
~/SCS/aws/certs/XXX-private.pem.key
~/SCS/aws/certs/XXX-public.pem.key
~/SCS/aws/certs/root-CA.crt

DOCUMENT EXAMPLE
{"endpoint": "asrft7e5j5ecz.iot.us-west-2.amazonaws.com", "client-id": "bruno", "cert-id": "9f08402232"}

SEE ALSO
scs_dev/aws_mqtt_client
"""

import sys

from scs_core.aws.config.project import Project

from scs_core.data.json import JSONify

from scs_core.sys.system_id import SystemID

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_aws_project import CmdAWSProject


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAWSProject()

    if cmd.verbose:
        print(cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # SystemID...
    if cmd.verbose:
        system_id = SystemID.load(Host)

        if system_id is None:
            print("aws_project: SystemID not available.", file=sys.stderr)
            exit(1)

        print(system_id, file=sys.stderr)
    else:
        system_id = None


    # ClientAuth...
    project = Project.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        project = Project.construct(cmd.organisation, cmd.group, cmd.location)
        project.save(Host)

    if cmd.delete:
        project.delete(Host)
        project = None

    if project:
        print(JSONify.dumps(project))

        if cmd.verbose:
            print("-")
            for channel in Project.CHANNELS:
                print(project.channel_path(channel, system_id), file=sys.stderr)
