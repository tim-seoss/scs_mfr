#!/usr/bin/env python3

"""
Created on 16 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

SCS workflow:
    1: ./afe_calib -s SERIAL_NUMBER
    2: ./afe_baseline.py -v -1 SN1_OFFSET -2 SN2_OFFSET -3 SN3_OFFSET -4 SN3_OFFSET

OpenSensors workflow:
  > 1: ./host_id.py
    2: ./system_id.py -s VENDOR_ID MODEL_ID MODEL_NAME CONFIG SYSTEM_SERIAL
    3: ./api_auth.py -s ORG_ID API_KEY
(   4: ./host_organisation.py -o ORG_ID -n NAME -w WEB -d DESCRIPTION -e EMAIL -v )
    5: ./host_client.py -s -u USER_ID -l LAT LNG POSTCODE -p
    6: ./host_project.py -s GROUP LOCATION_ID -p

command line example:
./host_id.py
"""

from scs_core.data.json import JSONify

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    serial_number = Host.serial_number()

    print(JSONify.dumps(serial_number))
