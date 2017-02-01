#!/usr/bin/env python3

"""
Created on 2 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from datetime import date

from scs_core.data.json import JSONify

from scs_dfe.gas.a4_calib import A4Calib
from scs_dfe.gas.afe import AFE
from scs_dfe.gas.afe_calib import AFECalib
from scs_dfe.gas.afe_conf import AFEConf
from scs_dfe.gas.pt1000 import Pt1000
from scs_dfe.gas.pt1000_calib import Pt1000Calib
from scs_dfe.gas.sensor import Sensor

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

try:
    I2C.open(Host.I2C_SENSORS)

    afe_type = "810-0023-XX"


    # ----------------------------------------------------------------------------------------------------------------
    # AFEConf...

    sensor_types = [Sensor.NO2_A43F, Sensor.OX_A431, Sensor.NO_A4, Sensor.CO_A4]

    afe_conf = AFEConf(afe_type, sensor_types)
    print(afe_conf)
    print("-")

    afe_conf.save(Host)

    afe_conf = AFEConf.load(Host)
    print(JSONify.dumps(afe_conf))
    print("=")


    # ----------------------------------------------------------------------------------------------------------------
    # Pt1000Calib...

    pt1000_calib = Pt1000Calib(date.today(), 0.295)
    print(pt1000_calib)
    print("-")


    # ----------------------------------------------------------------------------------------------------------------
    # AFECalib...

    no2_calib = A4Calib("212060317", "NO2A4", 278, 2, 280, 276, 0, 276, 0.184)
    print(no2_calib)
    print("-")

    ox_calib = A4Calib("214060231", "OXA4", 394, 5, 399, 385, 1, 386, 0.378, 0.261)
    print(ox_calib)
    print("-")

    no_calib = A4Calib("130180054", "NOA4", 282, 26, 308, 287, 24, 311, 0.369)
    print(no_calib)
    print("-")

    co_calib = A4Calib("132950203", "COA4", 292, 56, 344, 265, -9, 254, 0.239)
    print(co_calib)
    print("-")

    sensor_calibs = [no2_calib, ox_calib, no_calib, co_calib]

    afe_calib = AFECalib("26-000032", afe_type, date.today(), date.today(), pt1000_calib, sensor_calibs)
    print(afe_calib)
    print("-")

    afe_calib.save(Host)

    afe_calib = AFECalib.load(Host)
    print(JSONify.dumps(afe_calib))
    print("=")


    # ----------------------------------------------------------------------------------------------------------------
    # AFE...

    pt1000 = Pt1000(pt1000_calib)
    sensors = afe_conf.sensors()

    afe = AFE(pt1000, sensors)


    # ----------------------------------------------------------------------------------------------------------------
    # Pt1000Calib...

    pt1000_datum = afe.sample_temp()
    v20 = pt1000_datum.v20(20.0)            # TODO: use the SHT temperature as the reference

    pt1000_calib = Pt1000Calib(date.today(), v20)
    print(pt1000_calib)
    print("-")

    pt1000_calib.save(Host)

    pt1000_calib = Pt1000Calib.load(Host)
    print(JSONify.dumps(pt1000_calib))
    print("=")


finally:
    I2C.close()
