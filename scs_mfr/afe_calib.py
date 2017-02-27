#!/usr/bin/env python3

"""
Created on 27 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Creates AFECalib document.

command line example:
./scs_mfr/afe_calib.py -v
"""

import json
import sys

from collections import OrderedDict

from scs_core.data.json import JSONify

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
        client.connect("www.alphasense-technology.co.uk")

        try:
            response = client.get("/api/v1/boards/" + cmd.serial_number, None, {"Accept": "application/json"})
            jdict = json.loads(response, object_pairs_hook=OrderedDict)
            print("jdict:[%s]" % jdict)
            print("-")

            calib = AFECalib.construct_from_jdict(jdict)
            calib.save(Host)

        except RuntimeError:
            calib = None

        finally:
            client.close()

    else:
        calib = AFECalib.load_from_host(Host)

    print(JSONify.dumps(calib))
