#!/usr/bin/env python3

"""
Created on 24 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./gpi.py P9_12 -w 0 -v
"""

import sys

from scs_core.data.json import JSONify
from scs_core.sys.exception_report import ExceptionReport

from scs_host.sys.host_gpi import HostGPI

from scs_mfr.cmd.cmd_gpi import CmdGPI


# TODO: handle Raspberry Pi case for GPIO

# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    cmd = None
    sampler = None

    try:
        # ------------------------------------------------------------------------------------------------------------
        # cmd...

        cmd = CmdGPI()

        if not cmd.is_valid():
            cmd.print_help(sys.stderr)
            exit()

        if cmd.verbose:
            print(cmd, file=sys.stderr)


        # ------------------------------------------------------------------------------------------------------------
        # resources...

        gpi = HostGPI(cmd.pin)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        if cmd.wait is not None:
            edge = HostGPI.RISING if cmd.wait else HostGPI.FALLING
            gpi.wait(edge)

        print(gpi, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt as ex:
        if cmd.verbose:
            print("gpi: KeyboardInterrupt", file=sys.stderr)

    except Exception as ex:
        print(JSONify.dumps(ExceptionReport.construct(ex)), file=sys.stderr)

    finally:
        HostGPI.cleanup()
