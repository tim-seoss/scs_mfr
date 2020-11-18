#!/usr/bin/env python3

"""
Created on 20 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The interface_conf utility is used to specify whether a South Coast Science sensor interface board is present on the
host system and, if so, which type it is.

Types are:

* DFE - uses the Alphasense analogue front-end board (default)
* ISI - uses the South Coast Science integrated electrochem interface

If a DFE is selected, the use of the analogue-digital converter for the Pt1000 temperature sensor should be specified.
Options are:

* DFE - Pt1000 not used
* DFE/0x68 - Pt1000 used, ADC I2C address is 0x68
* DFE/0x69 - Pt1000 used, ADC I2C address is 0x69
* PZHBt1 - Pi Zero header breakout (type 1)
* PZHBt2 - Pi Zero header breakout (type 2)

The scs_dev sampler processes must be restarted for changes to take effect.

SYNOPSIS
interface_conf.py [{ [-m MODEL] [-i INFERENCE_UDS] | -d }] [-v]

EXAMPLES
./interface_conf.py -m DFE - i /home/scs/SCS/pipes/lambda-model-gas-s1.uds

DOCUMENT EXAMPLE
{"model": "DFE", "inf": "/home/scs/SCS/pipes/lambda-model-gas-s1.uds"}

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


# TODO: add a field identifying the model of DSI

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
    conf = InterfaceConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        model = cmd.model if cmd.model else conf.model
        inference = cmd.inference if cmd.inference else conf.inference

        conf = InterfaceConf(model, inference)
        conf.save(Host)

    elif cmd.delete and conf is not None:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
