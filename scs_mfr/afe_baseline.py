#!/usr/bin/env python3

"""
Created on 1 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

SCS workflow:
    1: ./afe_calib -s SERIAL_NUMBER
  > 2: ./afe_baseline.py -v -1 SN1_OFFSET -2 SN2_OFFSET -3 SN3_OFFSET -4 SN3_OFFSET

OpenSensors workflow:
    1: ./host_id.py
    2: ./system_id.py -s VENDOR_ID MODEL_ID MODEL_NAME CONFIG SYSTEM_SERIAL
    3: ./api_auth.py -s ORG_ID API_KEY
(   4: ./host_organisation.py -o ORG_ID -n NAME -w WEB -d DESCRIPTION -e EMAIL -v )
    5: ./host_client.py -s -u USER_ID -l LAT LNG POSTCODE -p
    6: ./host_project.py -s GROUP LOCATION_ID -p

Creates AFECalib document.

command line example:
./afe_baseline.py -v -1 SN1_OFFSET -2 SN2_OFFSET -3 SN3_OFFSET -4 SN3_OFFSET
"""

import datetime
import sys

from scs_core.data.json import JSONify
from scs_core.gas.afe_baseline import AFEBaseline
from scs_core.gas.sensor_baseline import SensorBaseline
from scs_host.sys.host import Host
from scs_mfr.cmd.cmd_afe_baseline import CmdAFEBaseline


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAFEBaseline()

    if cmd.verbose:
        print(cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    now = datetime.datetime.now()

    baseline = AFEBaseline.load_from_host(Host)

    if cmd.set():
        for i, offset in cmd.offsets.items():
            if offset is not None:
                baseline.set_sensor_baseline(i, SensorBaseline(now.date(), offset))

        baseline.save(Host)

    print(JSONify.dumps(baseline))
