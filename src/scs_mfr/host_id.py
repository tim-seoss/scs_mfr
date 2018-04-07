#!/usr/bin/env python3

"""
Created on 16 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The host_id utility reports the serial number of the host system processor board. The meaning of "serial number" is
implemented differently on each platform:

* Raspberry Pi: /proc/cpuinfo

* BeagleBone: hexdump -e '8/1 \"%c\"' /sys/bus/i2c/devices/0-0050/eeprom -s 16 -n 12

The host_id utility should be made available to the scs_dev/control_receiver in order that the host serial number
can be verified by a remote management system.

SYNOPSIS
host_id.py

EXAMPLES
./host_id.py

DOCUMENT EXAMPLE
"0000000040d4d158"

BUGS
On Raspberry Pi, the host ID appears to be derived from the MAC address of the active interface, and is therefore
unreliable on multi-homed hosts.
"""


from scs_core.data.json import JSONify

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    serial_number = Host.serial_number()

    print(JSONify.dumps(serial_number))
