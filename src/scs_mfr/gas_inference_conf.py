#!/usr/bin/env python3

"""
Created on 22 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The gas_inference_conf utility is used to specify how Greengrass data interpretation models are to be accessed:

* UDS_PATH - the Unix domain socket for communication between the gas sampler and the inference server
* INTERFACE - the format of the request
* GROUP - the performance parameters of the model(s) to be used

The gases_sampler and Greengrass container must be restarted for changes to take effect.

SYNOPSIS
gas_inference_conf.py [{ -l | [-u UDS_PATH] [-i INTERFACE] [-g GROUP] | -d }] [-v]

EXAMPLES
./gas_inference_conf.py -u pipes/lambda-gas-model.uds -i vB -v

DOCUMENT EXAMPLE
{"uds-path": "pipes/lambda-gas-model.uds", "model-interface": "vE", "model-compendium-group": "OE.g1"}

FILES
~/SCS/conf/gas_model_conf.json

SEE ALSO
scs_dev/gases_sampler
"""

import sys

from scs_core.data.json import JSONify
from scs_core.model.catalogue.model_compendium_group import ModelCompendiumGroup
from scs_core.model.gas.gas_model_conf import GasModelConf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_inference_conf import CmdInferenceConf


# TODO: rename as gas_model_conf.py?
# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdInferenceConf(GasModelConf.interfaces())

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("gas_inference_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # GasModelConf...
    conf = GasModelConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.list:
        print(JSONify.dumps(ModelCompendiumGroup.list()))

    elif cmd.set():
        if conf is None and not cmd.is_complete():
            print("gas_inference_conf: No configuration is stored - you must therefore set the UDS path and "
                  "the interface.", file=sys.stderr)
            cmd.print_help(sys.stderr)
            exit(2)

        if cmd.model_compendium_group is not None and \
                cmd.model_compendium_group not in ModelCompendiumGroup.list():
            print("gas_inference_conf: group '%s' cannot be found." % cmd.model_compendium_group, file=sys.stderr)
            exit(2)

        uds_path = cmd.uds_path if cmd.uds_path else conf.uds_path
        model_interface = cmd.model_interface if cmd.model_interface else conf.model_interface
        model_compendium_group = cmd.model_compendium_group if cmd.model_compendium_group else \
            conf.model_compendium_group

        conf = GasModelConf(uds_path, model_interface, model_compendium_group)
        conf.save(Host)

    elif cmd.delete and conf is not None:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
