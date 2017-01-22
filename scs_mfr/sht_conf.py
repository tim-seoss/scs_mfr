#!/usr/bin/env python3

"""
Created on 13 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./scs_manufacture/sht_conf.py -v -i 0x44
"""

import sys

from scs_core.data.json import JSONify
from scs_core.sys.exception_report import ExceptionReport

from scs_dfe.climate.sht_conf import SHTConf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_sht_conf import CmdSHTConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    sampler = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdSHTConf()

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    try:
        conf = SHTConf(cmd.int_addr, cmd.ext_addr)

        if cmd.verbose:
            print(conf, file=sys.stderr)

        conf.save(Host)

    except Exception as ex:
        print(JSONify.dumps(ExceptionReport.construct(ex)), file=sys.stderr)
