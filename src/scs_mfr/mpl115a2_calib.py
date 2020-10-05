#!/usr/bin/env python3

"""
Created on 20 Jun 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The mpl115a2_calib utility is used to calibrate the temperature sensor in the MPL115A2 digital barometer. The utility
operates by measuring the temperature using a Sensirion SHT sensor, measuring the temperature ADC count of the MPL115A2
sensor, and back-calculating the offset.

If calibration has been performed, the pressure_sampler utility reports temperature in addition to actual pressure
("pA"). If the host device altitude has also been set, the pressure_sampler additionally reports equivalent pressure
at sea level ("p0").

The pressure_sampler sampler processes must be restarted for changes to take effect.

SYNOPSIS
mpl115a2_calib.py [{ -s | -d }] [-v]

EXAMPLES
./mpl115a2_calib.py -s

FILES
~/SCS/conf/mpl115a2_calib.json

DOCUMENT EXAMPLE
{"calibrated-on": "2018-06-20T10:25:39.045+00:00", "c25": 511}

SEE ALSO
scs_dev/pressure_sampler
scs_mfr/mpl115a2_conf

  File "/home/scs/SCS/scs_host_bbe_southern/src/scs_host/bus/i2c.py", line 92, in read_cmd
    iter(cmd)
TypeError: 'int' object is not iterable

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "./mpl115a2_calib.py", line 90, in <module>
    barometer.init()
  File "/home/scs/SCS/scs_dfe_eng/src/scs_dfe/climate/mpl115a2.py", line 86, in init
    self.__a0 = self.__REG_A0.read()
  File "/home/scs/SCS/scs_dfe_eng/src/scs_dfe/climate/mpl115a2_reg.py", line 58, in read
    raw_value = self.__read_raw()
  File "/home/scs/SCS/scs_dfe_eng/src/scs_dfe/climate/mpl115a2_reg.py", line 72, in __read_raw
    values = I2C.read_cmd(self.__reg_addr, 2)
  File "/home/scs/SCS/scs_host_bbe_southern/src/scs_host/bus/i2c.py", line 96, in read_cmd
    cls.write(cmd)
  File "/home/scs/SCS/scs_host_bbe_southern/src/scs_host/bus/i2c.py", line 121, in write
    I2C.__FW.write(bytearray(values))
OSError: [Errno 121] Remote I/O error

"""

import sys

from scs_core.data.json import JSONify

from scs_dfe.climate.mpl115a2 import MPL115A2
from scs_core.climate.mpl115a2_calib import MPL115A2Calib
from scs_dfe.climate.sht_conf import SHTConf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_mpl115a2_calib import CmdMPL115A2Calib


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    try:
        I2C.open(Host.I2C_SENSORS)

        # ------------------------------------------------------------------------------------------------------------
        # cmd...

        cmd = CmdMPL115A2Calib()

        if not cmd.is_valid():
            cmd.print_help(sys.stderr)
            exit(2)

        if cmd.verbose:
            print("mpl115a2_calib: %s" % cmd, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # SHT...
        sht_conf = SHTConf.load(Host)
        sht = sht_conf.int_sht()

        # MPL115A2Calib...
        calib = MPL115A2Calib.load(Host)

        c25 = MPL115A2Calib.DEFAULT_C25 if calib is None else calib.c25

        # MPL115A2...
        barometer = MPL115A2(c25)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        barometer.init()

        if cmd.set:
            # SHT...
            sht_datum = sht.sample()

            if cmd.verbose:
                print(sht_datum, file=sys.stderr)

            # MPL115A2 initial...
            datum = barometer.sample()

            # MPL115A2 correction...
            c25 = datum.c25(sht_datum.temp)

            calib = MPL115A2Calib(None, c25)
            calib.save(Host)

            # calibrated...
            calib = MPL115A2Calib.load(Host)

        elif cmd.delete and calib is not None:
            calib.delete(Host)
            calib = None

        if calib:
            print(JSONify.dumps(calib))

        if cmd.verbose:
            barometer = MPL115A2.construct(calib)
            barometer.init()

            datum = barometer.sample()

            print(datum, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    finally:
        I2C.close()
