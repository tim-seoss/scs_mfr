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
afe_calib.py [{-s AFE_SERIAL_NUMBER | -t}] [-v]

EXAMPLES
./afe_calib -s 24-000004

DOCUMENT EXAMPLE
{"serial_number": "24-000004", "type": "810-0020-04", "calibrated_on": "2016-11-01", "dispatched_on": null,
"pt1000_v20": 1.0,
"sn1": {"serial_number": "132910128", "sensor_type": "CO A4", "we_electronic_zero_mv": 280, "we_sensor_zero_mv": 71,
"we_total_zero_mv": 351, "ae_electronic_zero_mv": 273, "ae_sensor_zero_mv": -8, "ae_total_zero_mv": 265,
 "we_sensitivity_na_ppb": 0.34, "we_cross_sensitivity_no2_na_ppb": "n/a", "pcb_gain": 0.8,
 "we_sensitivity_mv_ppb": 0.272, "we_cross_sensitivity_no2_mv_ppb": "n/a"},
 "sn2": {"serial_number": "134060008", "sensor_type": "SO2A4", "we_electronic_zero_mv": 271, "we_sensor_zero_mv": -2,
 "we_total_zero_mv": 269, "ae_electronic_zero_mv": 272, "ae_sensor_zero_mv": 2, "ae_total_zero_mv": 274,
 "we_sensitivity_na_ppb": 0.459, "we_cross_sensitivity_no2_na_ppb": "n/a", "pcb_gain": 0.8,
 "we_sensitivity_mv_ppb": 0.367, "we_cross_sensitivity_no2_mv_ppb": "n/a"},
 "sn3": {"serial_number": "133910025", "sensor_type": "H2SA4", "we_electronic_zero_mv": 277, "we_sensor_zero_mv": 13,
 "we_total_zero_mv": 290, "ae_electronic_zero_mv": 280, "ae_sensor_zero_mv": -10, "ae_total_zero_mv": 270,
 "we_sensitivity_na_ppb": 1.694, "we_cross_sensitivity_no2_na_ppb": "n/a", "pcb_gain": 0.8,
 "we_sensitivity_mv_ppb": 1.355, "we_cross_sensitivity_no2_mv_ppb": "n/a"},
 "sn4": {"serial_number": "143950150", "sensor_type": "PIDNH", "pid_zero_mv": null, "pid_sensitivity_mv_ppm": null}}

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

from scs_core.sys.http_exception import HTTPException

from scs_host.client.http_client import HTTPClient

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_afe_calib import CmdAFECalib


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    jstr = None

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
            jstr = AFECalib.TEST_JSON

        else:
            client = HTTPClient()
            client.connect(AFECalib.HOST)

            try:
                path = AFECalib.PATH + cmd.serial_number
                jstr = client.get(path, None, AFECalib.HEADER)

            except HTTPException as ex:
                print("afe_calib: %s" % ex, file=sys.stderr)
                exit(1)

            finally:
                client.close()

        jdict = json.loads(jstr)

        calib = AFECalib.construct_from_jdict(jdict)

        if calib is not None:
            calib.save(Host)

    calib = AFECalib.load(Host)

    if calib:
        print(JSONify.dumps(calib))
