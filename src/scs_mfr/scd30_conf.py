#!/usr/bin/env python3

"""
Created on 8 Sep 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The scd30_conf utility is used to specify whether or not a Sensirion SCD30 NDIR CO2 sensor is present, together with
its basic operating parameters.

Note that the scs_analysis/gases_sampler process must be restarted for changes to take effect.

SYNOPSIS
scd30_conf.py [{ [-i INTERVAL] [-t OFFSET] | -d }] [-v]

EXAMPLES
./scd30_conf.py -i 5 -t 0.0

DOCUMENT EXAMPLE
{"sample-interval": 5, "temp-offset": 0.0}

FILES
~/SCS/conf/scd30_conf.json

SEE ALSO
scs_dev/gases_sampler
scs_mfr/scd30_baseline
"""

import sys

from scs_core.data.json import JSONify

from scs_dfe.gas.scd30.scd30_conf import SCD30Conf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_scd30_conf import CmdSCD30Conf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdSCD30Conf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("scd30_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # scd30Conf...
    conf = SCD30Conf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        if conf is None and not cmd.is_complete():
            print("scd30_conf: No configuration is stored - you must therefore set both fields.", file=sys.stderr)
            cmd.print_help(sys.stderr)
            exit(2)

        sample_interval = cmd.sample_interval if cmd.sample_interval is not None else conf.sample_interval
        temperature_offset = cmd.temperature_offset if cmd.temperature_offset is not None else conf.temperature_offset

        conf = SCD30Conf(sample_interval, temperature_offset)
        conf.save(Host)

    elif cmd.delete and conf is not None:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
