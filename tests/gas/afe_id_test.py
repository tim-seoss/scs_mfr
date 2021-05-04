#!/usr/bin/env python3

"""
Created on 2 Mar 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from scs_core.data.json import JSONify
from scs_core.gas.afe_id import AFEId

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------
# run...

afe_id1 = AFEId.load(Host)
print(afe_id1)
print("-")

jstr = JSONify.dumps(afe_id1)
print(jstr)
print("-")

afe_id2 = AFEId.construct_from_jdict(json.loads(jstr))
print(afe_id2)
print("-")

print(afe_id2 == afe_id1)
