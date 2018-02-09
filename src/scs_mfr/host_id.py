#!/usr/bin/env python3

"""
Created on 16 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

WARNING: for Raspberry Pi, the host ID appears to be derived from the MAC address of the active interface.

Part 3 of 3: Deployment:

  > 1: ./host_id.py
    2: ./system_id.py -d VENDOR_ID -m MODEL_ID -n MODEL_NAME -c CONFIG -s SYSTEM_SERIAL_NUMBER -v
    3: ./osio_api_auth.py -s ORG_ID API_KEY
    4: ./osio_client_auth.py -u USER_ID -l LAT LNG POSTCODE
    5: ./osio_host_project.py -v -s GROUP LOCATION_ID
    6: ./timezone.py -v -s ZONE

command line example:
./host_id.py
"""

from scs_core.data.json import JSONify

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    serial_number = Host.serial_number()

    print(JSONify.dumps(serial_number))
