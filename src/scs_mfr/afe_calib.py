#!/usr/bin/env python3

"""
Created on 27 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The afe_calib utility is used to retrieve or install the calibration sheet for the Alphasense analogue front-end (AFE)
board or single sensor installed on the host system.

Alphasense electrochemical sensors are calibrated in the factory when fitted to their AFE board, or individually.
The calibration values are provided in a structured document, either on paper or - for sensors provided by South Coast
Science - in electronic form. The afe_calib utility is used to retrieve this JSON document via a web API.

The afe_calib utility may also be used to set a "test" calibration sheet, for use in a manufacturing environment.

Note that the scs_dev/gasses_sampler process must be restarted for changes to take effect.

SYNOPSIS
afe_calib.py [{ -a SERIAL_NUMBER | -s SERIAL_NUMBER YYYY-MM-DD | -t }] [-v]

EXAMPLES
./afe_calib.py -s 212810465 2019-08-22

DOCUMENT EXAMPLE
{"serial_number": null, "type": "IEI", "calibrated_on": "2019-09-09", "dispatched_on": null, "pt1000_v20": null,
"sn1": {"serial_number": "212810464", "sensor_type": "NOGA4", "we_electronic_zero_mv": 300, "we_sensor_zero_mv": 0,
"we_total_zero_mv": 300, "ae_electronic_zero_mv": 300, "ae_sensor_zero_mv": 0, "ae_total_zero_mv": 300,
"we_sensitivity_na_ppb": -0.445, "we_cross_sensitivity_no2_na_ppb": "n/a", "pcb_gain": -0.7,
"we_sensitivity_mv_ppb": 0.325, "we_cross_sensitivity_no2_mv_ppb": 0.324}}

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
from scs_core.gas.sensor_calib import SensorCalib

from scs_core.sys.http_exception import HTTPException

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_afe_calib import CmdAFECalib


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
            client.connect(AFECalib.ALPHASENSE_HOST)

            try:
                path = AFECalib.ALPHASENSE_PATH + cmd.afe_serial_number
                jdict = json.loads(client.get(path, None, AFECalib.ALPHASENSE_HEADER))
                calib = AFECalib.construct_from_jdict(jdict)

            except HTTPException as ex:
                print("afe_calib: %s" % ex, file=sys.stderr)
                exit(1)

            finally:
                client.close()

        else:
            client = HTTPClient()
            client.connect(SensorCalib.ALPHASENSE_HOST)

            try:
                path = SensorCalib.ALPHASENSE_PATH + cmd.sensor_serial_number
                jstr = client.get(path, None, SensorCalib.ALPHASENSE_HEADER)

                sensor_calib = SensorCalib.construct_from_jdict(json.loads(jstr))
                sensor_calib.set_defaults()
                sensor_calib.set_sens_mv_from_sens_na()

                calib = AFECalib.construct_for_sensor(cmd.sensor_calibration_date, sensor_calib)

            except HTTPException as ex:
                print("afe_calib: %s" % ex, file=sys.stderr)
                exit(1)

            finally:
                client.close()

        if calib is not None:
            calib.save(Host)

    calib = AFECalib.load(Host)

    if calib:
        print(JSONify.dumps(calib))
