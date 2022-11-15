#!/usr/bin/env python3

"""
Created on 20 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The interface_conf utility is used to specify whether a South Coast Science sensor interface is present on the
host system and, if so, which type it is. A distinction is made between the sensor interface (which controls power
and access to all sensors) and the gas interface, which controls access to electrochemical and VOC A4 sensors.

Sensor interface types are:

* DFE - the digital front-end board for Praxis/Urban
* OPCubeT1 - the man processor board for Praxis/Cube
* PZHBtN - the header breakout board for Praxis/Handheld

Gas interface types are:

* AFE - Alphasense analogue front-end board
* ISI - South Coast Science integrated single interface

If an AFE is selected, the use of the analogue-digital converter for the Pt1000 temperature sensor should be specified.

The scs_dev sampler processes must be restarted for changes to take effect.

SYNOPSIS
interface_conf.py [{ -m MODEL | -d }] [-v]

EXAMPLES
./interface_conf.py -m DFE

DOCUMENT EXAMPLE
{"model": "DFE"}

FILES
~/SCS/conf/interface_conf.json

SEE ALSO
scs_dev/gases_sampler
scs_mfr/pt1000_calib
"""

import sys

from scs_core.data.json import JSONify

from scs_dfe.interface.interface_conf import InterfaceConf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_interface_conf import CmdInterfaceConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdInterfaceConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("interface_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # InterfaceConf...
    conf = InterfaceConf.load(Host, skeleton=True)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        model = cmd.model if cmd.model else conf.model

        conf = InterfaceConf(model)
        conf.save(Host)

    elif cmd.delete and conf is not None:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
