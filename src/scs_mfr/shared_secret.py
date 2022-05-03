#!/usr/bin/env python3

"""
Created on 2 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The shared_secret utility generates a digest key used by the scs_analysis/mqtt_control and scs_dev/control_receiver
utilities. The key is typically generated when a device is manufactured, and securely stored on a remote device
management system.

SYNOPSIS
shared_secret.py [{ -g | -d }] [-v]

EXAMPLES
./shared_secret.py -g

DOCUMENT EXAMPLE
{"key": "sxBhncFybpbMwZUa"}

FILES
~/SCS/conf/shared_secret.conf

SEE ALSO
scs_dev/control_receiver
"""

import sys

from scs_core.data.json import JSONify

from scs_core.sys.shared_secret import SharedSecret

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_shared_secret import CmdSharedSecret


# TODO: update cognito device identity if shared secret changes
# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdSharedSecret()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("shared_secret: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # SHTConf...
    secret = SharedSecret.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.generate:
        secret = SharedSecret(SharedSecret.generate())
        secret.save(Host)

    if cmd.delete and secret is not None:
        secret.delete(Host)
        secret = None

    if secret:
        print(JSONify.dumps(secret))
