#!/usr/bin/env python3

"""
Created on 27 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

workflow:
> 1: ./afe_calib -s SERIAL_NUMBER
  2: ./system_id.py -s VENDOR_ID MODEL_ID MODEL_NAME CONFIG SYSTEM_SERIAL
  3: ./api_auth.py -s ORG_ID API_KEY
  4: ./host_device.py -s -u USER_ID -l LAT LNG POSTCODE -p
  5: ./host_project.py -s GROUP LOCATION_ID -p

Creates AFECalib document.

command line example:
./afe_calib.py -v -s 15-000064
"""

import json
import sys

from collections import OrderedDict

from scs_core.data.json import JSONify
from scs_core.sys.exception_report import ExceptionReport

from scs_dfe.gas.afe_calib import AFECalib

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_afe_calib import CmdAFECalib


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAFECalib()

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        client = HTTPClient()
        client.connect(AFECalib.HOST)

        try:
            path = AFECalib.PATH + cmd.serial_number
            response = client.get(path, None, AFECalib.HEADER)
            jdict = json.loads(response, object_pairs_hook=OrderedDict)

            calib = AFECalib.construct_from_jdict(jdict)

            if calib is not None:
                calib.save(Host)

        except RuntimeError as ex:
            if cmd.verbose:
                report = ExceptionReport.construct(ex)
                print(JSONify.dumps(report.summary), file=sys.stderr)

            calib = None

        finally:
            client.close()

    calib = AFECalib.load_from_host(Host)

    print(JSONify.dumps(calib))
