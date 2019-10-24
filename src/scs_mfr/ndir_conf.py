#!/usr/bin/env python3

"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The ndir_conf utility is used to specify whether a South Coast Science SPI interface NDIR CO2 sensor board is present
and if so, which model is provided.

The specification also includes the number of number of NDIR readings to be averaged. The NDIR monitor sub-process
maintains a rolling average with a base sampling rate of one second. Thus, setting the tally to 10 results in an
independent reading every 10 seconds.

Sampling is performed by the scs_dev/gasses_sampler utility if an ndir_conf.json document is present. If the document
is not present, the NDIR sensor board is ignored.

Note that the scs_analysis/gasses_sampler process must be restarted for changes to take effect.

SYNOPSIS
ndir_conf.py [{ [-m MODEL] [-t AVERAGING_TALLY] | -d }] [-v]

EXAMPLES
./ndir_conf.py -m NDIRv1 -t 10

DOCUMENT EXAMPLE
{"model": "NDIRv1", "tally": 10}

FILES
~/SCS/conf/ndir_conf.json

SEE ALSO
scs_dev/gases_sampler
"""

import sys

from scs_core.data.json import JSONify

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_ndir_conf import CmdNDIRConf

from scs_ndir.gas.ndir.ndir_conf import NDIRConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdNDIRConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("ndir_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # NDIRConf...
    conf = NDIRConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        if conf is None and not cmd.is_complete():
            print("ndir_conf: No configuration is stored. You must therefore set all fields.", file=sys.stderr)
            cmd.print_help(sys.stderr)
            exit(1)

        model = cmd.model if cmd.model else conf.model
        tally = cmd.tally if cmd.tally else conf.tally
        raw = cmd.raw if cmd.raw is not None else conf.raw

        conf = NDIRConf(model, tally, raw)
        conf.save(Host)

    elif cmd.delete and conf is not None:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
