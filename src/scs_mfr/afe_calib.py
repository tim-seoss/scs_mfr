#!/usr/bin/env python3

"""
Created on 27 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The afe_calib utility is used to retrieve or install the calibration sheet for the Alphasense analogue front-end (AFE)
board installed on the host system.

Alphasense electrochemical sensors are calibrated in the factory when fitted to their AFE board. The calibration
values are provided in a structured document, either on paper or - for AFE boards provided by South Coast Science -
in electronic form. The afe_calib utility is used to retrieve this JSON document via a web API.

The afe_calib utility may also be used to set a "test" calibration sheet, for use in a manufacturing environment.

Note that the scs_dev/gasses_sampler process must be restarted for changes to take effect.

SYNOPSIS
afe_calib.py [{-a AFE_SERIAL_NUMBER | -s A4_SERIAL_NUMBER YYYY-MM-DD WE_SENS WE_X_SENS | -t}] [-v]

EXAMPLES
./afe_calib.py -v -s 212810465 2019-08-22 0.324 0

DOCUMENT EXAMPLE
{"serial_number": "00-000000", "type": "000-0000-00", "calibrated_on": "2019-08-22", "dispatched_on": null,
"pt1000_v20": 1.0, "sn1": {"serial_number": "212810465", "sensor_type": "NOGA4", "we_electronic_zero_mv": 300,
"we_sensor_zero_mv": 6, "we_total_zero_mv": 300, "ae_electronic_zero_mv": 300, "ae_sensor_zero_mv": 1,
"ae_total_zero_mv": 300, "we_sensitivity_na_ppb": null, "we_cross_sensitivity_no2_na_ppb": -0.3, "pcb_gain": -0.7,
"we_sensitivity_mv_ppb": 0.324, "we_cross_sensitivity_no2_mv_ppb": "n/a"}}

FILES
~/SCS/conf/afe_calib.json

SEE ALSO
scs_dev/gases_sampler
scs_mfr/afe_baseline

RESOURCES
https://www.alphasense-technology.co.uk/
"""

import json
import sys

from scs_core.data.json import JSONify

from scs_core.gas.afe_calib import AFECalib
from scs_core.gas.sensor import Sensor

from scs_core.sys.http_exception import HTTPException

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_afe_calib import CmdAFECalib

# TODO: use nA instead of mV

# TODO: add delete mode, change name to gas_calib

# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    calib = None
    calibrated_on = None
    we_sens_mv = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAFECalib()

    if cmd.verbose:
        print("afe_calib: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        if cmd.test:
            jdict = json.loads(AFECalib.TEST_LOAD)
            calib = AFECalib.construct_from_jdict(jdict)

        elif cmd.afe_serial_number:
            client = HTTPClient()
            client.connect(AFECalib.HOST)

            try:
                path = AFECalib.PATH + cmd.afe_serial_number
                jdict = json.loads(client.get(path, None, AFECalib.HEADER))
                calib = AFECalib.construct_from_jdict(jdict)

            except HTTPException as ex:
                print("afe_calib: %s" % ex, file=sys.stderr)
                exit(1)

            finally:
                client.close()

        else:
            sensor = Sensor.find(cmd.dsi_serial_number)

            if sensor is None:
                print("afe_calib: unrecognised serial number: %s" % cmd.dsi_serial_number, file=sys.stderr)
                exit(2)

            try:
                calibrated_on = cmd.dsi_calibration_date
            except (IndexError, ValueError):
                print("afe_calib: invalid date: %s" % cmd.dsi_calibration_date_str, file=sys.stderr)
                exit(2)

            try:
                we_sens_mv = float(cmd.dsi_we_sens_mv)
            except ValueError:
                print("afe_calib: invalid floating point value: %s" % cmd.dsi_we_sens_mv_str, file=sys.stderr)
                exit(2)

            jdict = json.loads(AFECalib.DSI_WRAPPER)
            calib = AFECalib.construct_from_jdict(jdict)

            calib.calibrated_on = calibrated_on

            sensor_calib = calib.sensor_calib(0)
            sensor_calib.serial_number = cmd.dsi_serial_number
            sensor_calib.sensor_type = sensor.sensor_type
            sensor_calib.we_sens_mv = we_sens_mv
            sensor_calib.we_no2_x_sens_mv = cmd.dsi_we_no2_x_sens_mv

        if calib is not None:
            calib.save(Host)

    calib = AFECalib.load(Host)

    if calib:
        print(JSONify.dumps(calib))
