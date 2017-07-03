#!/usr/bin/env python3

"""
Created on 29 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

calibration workflow:
    1: ./rtc.py -i -s -v
    2: ./pt1000_calib.py -s -v
    3: ./afe_calib -s AFE_SERIAL_NUMBER
    4: ./afe_baseline.py -v -1 SN1_OFFSET -2 SN2_OFFSET -3 SN3_OFFSET -4 SN3_OFFSET
  > 5: ./schedule.py [{-s NAME INTERVAL COUNT | -c NAME }] [-v]

Creates Schedule document.

document example:
{"particulates": {"sampling-interval": 5.0, "sample-count": 2}, "gases": {"sampling-interval": 10.0, "sample-count": 1}}

command line example:
./schedule.py -s gases 10.0 1
"""

import sys

from scs_core.data.json import JSONify
from scs_core.sync.schedule import Schedule
from scs_core.sync.schedule import ScheduleItem

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_schedule import CmdSchedule


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdSchedule()

    if cmd.verbose:
        print(cmd, file=sys.stderr)
        sys.stderr.flush()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    schedule = Schedule.load_from_host(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        item = ScheduleItem(cmd.name, cmd.interval, cmd.count)
        schedule.set(item)
        schedule.save(Host)

    if cmd.clear():
        schedule.clear(cmd.name)
        schedule.save(Host)

    print(JSONify.dumps(schedule))
