#!/usr/bin/env python3

"""
Created on 23 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The pmx_inference_conf utility is used to

The gases_sampler must be restarted for changes to take effect.

SYNOPSIS
pmx_inference_conf.py [{ [-u UDS_PATH] [-i INTERFACE] [-s SPECIES RESOURCE_NAME] | [-r SPECIES] | -d }] [-v]

EXAMPLES
(scs-venv) scs@scs-bbe-003:~/SCS/scs_mfr/src/scs_mfr$ ./pmx_inference_conf.py -u pipes/lambda-model-pmx-s1.uds -i s1 \
-s pm1 /trained-models/pm1-s1-2020h1/xgboost-model -v

DOCUMENT EXAMPLE
{"uds-path": "pipes/lambda-model-pmx-s1.uds", "model-interface": "s1",
"resource-names": {"pm1": "/trained-models/pm1-s1-2020h1/xgboost-model",
"pm2p5": "/trained-models/pm2p5-s1-2020h1/xgboost-model",
"pm10": "/trained-models/pm10-s1-2020h1/xgboost-model"}}

FILES
~/SCS/conf/pmx_model_conf.json

SEE ALSO
scs_dev/particulates_sampler
"""

import sys

from scs_core.data.json import JSONify
from scs_core.model.particulates.pmx_model_conf import PMxModelConf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_inference_conf import CmdInferenceConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdInferenceConf(PMxModelConf.interfaces())

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("pmx_inference_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # PMxModelConf...
    conf = PMxModelConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        if conf is None and not cmd.is_complete():
            print("pmx_inference_conf: No configuration is stored - you must therefore set all fields.",
                  file=sys.stderr)
            cmd.print_help(sys.stderr)
            exit(2)

        uds_path = cmd.uds_path if cmd.uds_path else conf.uds_path
        model_interface = cmd.model_interface if cmd.model_interface else conf.model_interface
        resource_names = {} if conf is None else conf.resource_names

        conf = PMxModelConf(uds_path, model_interface, resource_names)
        conf.save(Host)

    if cmd.set_species:
        conf.set_resource_name(cmd.set_species, cmd.set_filename)
        conf.save(Host)

    if cmd.remove_species:
        conf.delete_resource_name(cmd.remove_species)
        conf.save(Host)

    if cmd.delete and conf is not None:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
