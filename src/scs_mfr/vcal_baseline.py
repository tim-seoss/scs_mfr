#!/usr/bin/env python3

"""
Created on 15 Oct 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The baseline utility is used to adjust the zero offset of the reported vCal value. A positive offset value
cause the output to be higher.

In normal circumstances, the vCal offset should be set so that the minimum vCal value for the given gas on the given
device matches the minimum vCal value in the model compendium.

IMPORTANT NOTE: the vCal baseline does not change the vCal value as reported by the gases_sampler utility. Instead,
it is used by the gas exegesis system, as part of the preprocessing of data that is passed to the interpretation
model.

Each sensor is identified by the gas that it detects. For example, a nitrogen dioxide sensor is identified as NO2, and
an ozone sensor is identified as Ox.

Note that the greengrass processes must be restarted for changes to take effect.

SYNOPSIS
vcal_baseline.py [{ -b GAS  | -s GAS VALUE | -m GAS MINIMUM | -r GAS | -d }] [-v]

EXAMPLES
./vcal_baseline.py -m NO2 -5

DOCUMENT EXAMPLE
{"CO": {"calibrated-on": "2021-01-19T10:07:27Z", "offset": 2},
"NO2": {"calibrated-on": "2021-01-19T10:07:27Z", "offset": 16}}

FILES
~/SCS/conf/baseline.json

SEE ALSO
scs_dev/gases_sampler
scs_mfr/gas_inference_conf
"""

import sys

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.gas.sensor_baseline import SensorBaseline

from scs_core.model.catalogue.model_compendium_group import ModelCompendiumGroup
from scs_core.model.gas.gas_model_conf import GasModelConf
from scs_core.model.gas.vcal_baseline import VCalBaseline

from scs_core.sys.logging import Logging

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_vcal_baseline import CmdVCalBaseline


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    model = None
    primary = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdVCalBaseline()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    Logging.config('vcal_baseline', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # resources...

        baseline = VCalBaseline.load(Host, skeleton=True)

        if cmd.match:
            conf = GasModelConf.load(Host)

            if conf is None:
                logger.error("GasModelConf not available.")
                exit(1)

            logger.info(conf)

            group_name = conf.model_compendium_group
            group = ModelCompendiumGroup.retrieve(group_name)

            if conf is None:
                logger.error("ModelCompendiumGroup not available for '%s'." % group_name)
                exit(1)

            try:
                model = group.compendium(cmd.gas_name())
            except KeyError:
                logger.error("ModelCompendium not available for gas '%s'." % cmd.gas_name())
                exit(1)

            primary = model.primaries['.'.join((cmd.gas_name(), 'vCal'))]

            logger.info(primary)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        now = LocalizedDatetime.now().utc()

        # update...
        if cmd.update():
            old_offset = baseline.sensor_offset(cmd.gas_name())
            new_offset = int(round(primary.minimum - cmd.match_value())) if cmd.match else cmd.set_value()

            baseline.set_sensor_baseline(cmd.gas_name(), SensorBaseline(now, new_offset))
            baseline.save(Host)

            if cmd.verbose:
                logger.info("%s: was: %s now: %s" % (cmd.gas_name(), old_offset, new_offset))

        # baseline...
        if cmd.baseline:
            gas_name = cmd.gas_name()
            sensor_baseline = baseline.sensor_baseline(gas_name)

            if sensor_baseline is None:
                logger.error("%s is not included in the calibration document." % gas_name)
                exit(1)

            baseline = VCalBaseline({gas_name: sensor_baseline})

        # remove...
        if cmd.remove:
            baseline.remove_sensor_baseline(cmd.gas_name())
            baseline.save(Host)

        # delete...
        if cmd.delete:
            VCalBaseline.delete(Host)
            baseline = None

        # report...
        if baseline:
            print(JSONify.dumps(baseline))


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt:
        print(file=sys.stderr)
