#!/usr/bin/env python3

"""
Created on 29 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Part 1 of 3: Configuration:

    1: ./dfe_conf.py -v -s -p PT1000_ADDR
    2: ./sht_conf.py -v -i INT_ADDR -e EXT_ADDR
    3: ./ndir_conf.py -v -m MODEL
    4: ./opc_conf.py -v -m MODEL -s SAMPLE_PERIOD -p { 0 | 1 }
    5: ./psu_conf.py -v -m MODEL
    6: ./gps_conf.py -v -m MODEL
  > 7: ./schedule.py -v [{-s NAME INTERVAL COUNT | -c NAME }]

Creates or deletes Schedule document.

document example:
{"scs-climate": {"interval": 60.0, "tally": 1}, "scs-gases": {"interval": 10.0, "tally": 1},
"scs-particulates": {"interval": 10.0, "tally": 1}, "scs-status": {"interval": 60.0, "tally": 1}}

command line example:
./schedule.py -s scs-climate 10.0 1
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
        exit(2)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    schedule = Schedule.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        item = ScheduleItem(cmd.name, cmd.interval, cmd.count)

        # if not item.is_valid():
        #     print("Item is not valid: %s" % item)
        #     exit(1)

        schedule.set(item)
        schedule.save(Host)

    if cmd.clear():
        schedule.clear(cmd.name)
        schedule.save(Host)

    print(JSONify.dumps(schedule))
