#!/usr/bin/env python3

"""
Created on 13 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The opc_conf utility is used to specify whether an Alphasense optical particle counter (OPC) is present and if so,
which model is attached. An option is also available to override the host's default SPI bus and SPI chip select
lines for the OPC.

The specification also includes the number of seconds between readings by the OPC monitor sub-process. The maximum
time between readings is 10 seconds, the minimum five. A 10 second period provides the highest precision, but sampling
at this rate may be subject to clipping in extremely polluted environments.

Sampling is performed by the scs_dev/particulates_sampler utility. If an opc_conf.json document is not present, the
scs_dev/particulates_sampler utility terminates.

Note that the scs_dev/particulates_sampler process must be restarted for changes to take effect.

The OPC-N2, OPC-N3 and OPC-R1 models are supported.

SYNOPSIS
opc_conf.py [{ [-m MODEL] [-s SAMPLE_PERIOD] [-p { 0 | 1 }] [-b SPI_BUS] [-c SPI_DEVICE] | -d }] [-v]

EXAMPLES
./opc_conf.py -b 0 -c 0 -m R1

DOCUMENT EXAMPLE
{"model": "R1", "sample-period": 10, "power-saving": false, "spi-bus": null, "spi-device": null}

FILES
~/SCS/conf/opc_conf.json

SEE ALSO
scs_dev/particulates_sampler
scs_mfr/opc_cleaning_interval

BUGS
The specification allows for a power saving mode - which enables the OPC to shut down between readings - but
this is not currently implemented.
"""

import sys

from scs_core.data.json import JSONify

from scs_dfe.particulate.opc_conf import OPCConf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_opc_conf import CmdOPCConf


# TODO: check sample period against Schedule

# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdOPCConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("opc_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # OPCConf...
    conf = OPCConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        if conf is None and not cmd.is_complete():
            print("opc_conf: No configuration is stored. You must therefore set model, period and power fields.",
                  file=sys.stderr)
            cmd.print_help(sys.stderr)
            exit(1)

        model = cmd.model if cmd.model else conf.model
        sample_period = cmd.sample_period if cmd.sample_period else conf.sample_period
        power_saving = cmd.power_saving if cmd.power_saving is not None else conf.power_saving

        spi_bus = conf.spi_bus if cmd.spi_bus is None else cmd.spi_bus
        spi_device = conf.spi_device if cmd.spi_device is None else cmd.spi_device

        conf = OPCConf(model, sample_period, power_saving, spi_bus, spi_device)
        conf.save(Host)

    elif cmd.delete:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
