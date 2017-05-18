#!/usr/bin/env python3

"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_core.data.json import JSONify
from scs_core.gas.pt1000_calib import Pt1000Calib
from scs_core.sys.exception_report import ExceptionReport

from scs_dfe.climate.sht_conf import SHTConf
from scs_dfe.gas.afe import AFE
from scs_dfe.gas.pt1000 import Pt1000

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_pt1000_calib import CmdPt1000Calib


# --------------------------------------------------------------------------------------------------------------------

# TODO: implement RTC init / set functions
