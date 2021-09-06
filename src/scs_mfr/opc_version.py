#!/usr/bin/env python3

"""
Created on 4 Sep 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The opc_version utility is used to interrogate, update or delete the firmware version and serial number of an
attached optical particle counter (OPC).

The report is updated automatically each time the particulates_sampler command is run. The report is persisted in the
host's filesystem, enabling it to be read by the configuration utility.

Note that, although support is provided for multiple named version reports, the configuration utility will only access
unnamed (solitary) version reports.

SYNOPSIS
opc_version.py [-n NAME] [{ -s | -d }] [-v]

EXAMPLES
./opc_version.py -vs

DOCUMENT EXAMPLE
{"serial": "177336702", "firmware": "OPC-N3 Iss1.1 FirmwareVer=1.17a...........................BS"}

FILES
~/SCS/conf/opc_version.json

SEE ALSO
scs_dev/opc_cleaner
scs_dev/particulates_sampler

scs_mfr/opc_conf
scs_mfr/opc_firmware_conf
"""

import sys

from scs_core.data.json import JSONify
from scs_core.particulate.opc_version import OPCVersion

from scs_dfe.interface.interface_conf import InterfaceConf
from scs_dfe.particulate.opc_conf import OPCConf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_opc_version import CmdOPCVersion


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    opc = None
    report = None

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

        if cmd.set:
            # OPC...
            opc = opc_conf.opc(interface, Host)

            if not opc:
                print("opc_version: OPC not available", file=sys.stderr)
                exit(1)

            if cmd.verbose:
                print("opc_version: %s" % opc, file=sys.stderr)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        if cmd.set:
            opc.power_on()

            report = OPCVersion(opc.serial_no(), opc.firmware(), name=cmd.name)
            report.save(Host)

        elif cmd.delete:
            OPCVersion.delete(Host, name=cmd.name)

        else:
            report = OPCVersion.load(Host, name=cmd.name)

        if report:
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
