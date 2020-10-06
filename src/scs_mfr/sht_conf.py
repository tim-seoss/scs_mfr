#!/usr/bin/env python3

"""
Created on 13 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The sht_conf utility is used to specify the I2C address(es) of Sensirion SHT temperature and relative humidity sensors
deployed in South Coast Science equipment.

Two different Sensirion SHT sensor configurations are generally used:

* SHT in A4 pot (internal) - I2C address: 0x44 - the sensor is enclosed in a package that mimics the electrochemical
sensor environment. This sensor is used to perform temperature and humidity compensations in data interpretation.

* Free-to-air SHT (external) - I2C address: 0x45 - the sensor is directly exposed to the air. This arrangement provides
a more responsive and accurate measurement of the ambient conditions.

For devices with only one sensor type present, the internal and external address should be set to the same value.

Note that the scs_dev sampler processes must be restarted for changes to take effect.

SYNOPSIS
sht_conf.py [{ [-i INT_ADDR] [-e EXT_ADDR] | -d }] [-v]

EXAMPLES
./sht_conf.py -v -i 0x44 -e 0x45

DOCUMENT EXAMPLE
{"int": "0x44", "ext": "0x45"}

FILES
~/SCS/conf/sht_conf.json

SEE ALSO
scs_dev/climate_sampler
scs_dev/gases_sampler
"""

import sys

from scs_core.data.json import JSONify

from scs_dfe.climate.sht_conf import SHTConf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_sht_conf import CmdSHTConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdSHTConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("sht_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # SHTConf...
    conf = SHTConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # validate...

    if conf is None and cmd.set() and not cmd.is_complete():
        print("sht_conf: No configuration is stored - you must therefore set both I2C addresses.", file=sys.stderr)
        cmd.print_help(sys.stderr)
        exit(2)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        if conf is None and not cmd.is_complete():
            cmd.print_help(sys.stderr)
            exit(1)

        int_addr = cmd.int_addr if cmd.int_addr is not None else conf.int_addr
        ext_addr = cmd.ext_addr if cmd.ext_addr is not None else conf.ext_addr

        conf = SHTConf(int_addr, ext_addr)
        conf.save(Host)

    elif cmd.delete and conf is not None:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
