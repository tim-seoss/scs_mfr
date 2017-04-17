#!/usr/bin/env python3

"""
Created on 24 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./gpo.py P9_12 0 -v
"""

import sys
import time

from scs_core.data.json import JSONify
from scs_core.sys.exception_report import ExceptionReport

from scs_host.sys.host_gpo import HostGPO

from scs_mfr.cmd.cmd_gpo import CmdGPO


# TODO: handle Raspberry Pi case for GPIO

# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    cmd = None
    sampler = None

    try:
        # ------------------------------------------------------------------------------------------------------------
        # cmd...

        cmd = CmdGPO()

        if not cmd.is_valid():
            cmd.print_help(sys.stderr)
            exit()

        if cmd.verbose:
            print(cmd, file=sys.stderr)


        # ------------------------------------------------------------------------------------------------------------
        # resources...

        state = HostGPO.HIGH if cmd.level else HostGPO.LOW

        gpo = HostGPO(cmd.pin, state)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        if cmd.wait:
            time.sleep(cmd.wait)
        else:
            while True:
                time.sleep(0.1)

        print(gpo, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt as ex:
        if cmd.verbose:
            print("gpo: KeyboardInterrupt", file=sys.stderr)

    except Exception as ex:
        print(JSONify.dumps(ExceptionReport.construct(ex)), file=sys.stderr)

    finally:
        HostGPO.cleanup()
