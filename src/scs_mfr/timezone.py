#!/usr/bin/env python3

"""
Created on 12 Aug 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Part 2 of 3: Calibration:

(   1: ./rtc.py -i -s -v )
    2: ./afe_calib -s AFE_SERIAL_NUMBER
    3: ./pt1000_calib.py -s -v
    4: ./afe_baseline.py -v -1 SN1_OFFSET -2 SN2_OFFSET -3 SN3_OFFSET -4 SN3_OFFSET
  > 5: ./timezone.py -v -s ZONE

Creates TimezoneConf document.

document example:
{"set-on": "2017-08-12T11:20:28.740+00:00", "name": "Europe/London"}

command line example:
./timezone.py -s Europe/London -v
"""

import sys

from scs_core.data.json import JSONify
from scs_core.data.localized_datetime import LocalizedDatetime

from scs_core.location.timezone import Timezone
from scs_core.location.timezone_conf import TimezoneConf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_timezone import CmdTimezone


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdTimezone()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print(cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    conf = TimezoneConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    now = LocalizedDatetime.now()

    if cmd.list:
        for zone in Timezone.zones():
            print(zone, file=sys.stderr)
        exit(0)

    elif cmd.set():
        if not Timezone.is_valid(cmd.zone):
            print("timezone: zone is not accepted: %s" % cmd.zone, file=sys.stderr)
            exit(1)

        if cmd.zone != conf.name:
            conf = TimezoneConf(now, cmd.zone)
            conf.save(Host)

    elif cmd.link:
        if not conf.uses_system_name() or conf.set_on is None:
            conf = TimezoneConf(now, None)
            conf.save(Host)

    print(JSONify.dumps(conf))

    if cmd.verbose:
        print(JSONify.dumps(conf.timezone()), file=sys.stderr)

