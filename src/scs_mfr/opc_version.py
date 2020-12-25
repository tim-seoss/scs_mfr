#!/usr/bin/env python3

"""
Created on 4 Sep 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The opc_version utility reports either the firmware version or serial number of an attached optical particle counter
(OPC). The reported string is written to stdout.

The opc_version utility exits with 1 if no version string could be read, and exits with 0 if a string was read. The
command can therefore be used to test for the presence / operability of an OPC.

SYNOPSIS
opc_version.py { -w | -s } [-n NAME] [-v]

EXAMPLES
./opc_version.py -w -v

DOCUMENT EXAMPLE - OUTPUT
"OPC-N2 FirmwareVer=OPC-018.2..............................BD"

SEE ALSO
scs_dev/opc_cleaner
scs_dev/particulates_sampler

scs_mfr/opc_conf
scs_mfr/opc_firmware_conf
"""

import sys

from scs_core.data.json import JSONify

from scs_dfe.interface.interface_conf import InterfaceConf
from scs_dfe.particulate.opc_conf import OPCConf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_opc_version import CmdOPCVersion


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    opc = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdOPCVersion()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("opc_version: %s" % cmd, file=sys.stderr)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # OPCConf...
        opc_conf = OPCConf.load(Host, name=cmd.name)

        if opc_conf is None:
            print("opc_version: OPCConf not available.", file=sys.stderr)
            exit(1)

        # I2C...
        if opc_conf.uses_spi():
            I2C.Utilities.open()
        else:
            I2C.Sensors.open_for_bus(opc_conf.bus)

        # Interface...
        interface_conf = InterfaceConf.load(Host)

        if interface_conf is None:
            print("opc_version: InterfaceConf not available.", file=sys.stderr)
            exit(1)

        interface = interface_conf.interface()

        if interface is None:
            print("opc_power: Interface not available.", file=sys.stderr)
            exit(1)

        if cmd.verbose and interface:
            print("opc_version: %s" % interface, file=sys.stderr)

        # OPC...
        opc = opc_conf.opc(interface, Host)

        if cmd.verbose:
            print("opc_version: %s" % opc, file=sys.stderr)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        opc.power_on()

        report = opc.firmware() if cmd.firmware else opc.serial_no()

        if not report:
            print("opc_version: OPC not available", file=sys.stderr)
            exit(1)

        print(JSONify.dumps(report))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        pass

    finally:
        if opc:
            opc.power_off()

        I2C.Sensors.close()
        I2C.Utilities.close()
