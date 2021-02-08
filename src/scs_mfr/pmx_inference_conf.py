#!/usr/bin/env python3

"""
Created on 23 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The pmx_inference_conf utility is used to specify how Greengrass data interpretation models are to be accessed:

* UDS_PATH - the Unix domain socket for communication between the particulates sampler and the inference server
* INTERFACE - the format of the request
* SPECIES: RESOURCE_NAME - the model resource for each particle size

The particulates_sampler and Greengrass container must be restarted for changes to take effect.

SYNOPSIS
pmx_inference_conf.py [{ [-u UDS_PATH] [-i INTERFACE] | -d }] [-v]

EXAMPLES
./pmx_inference_conf.py -u pipes/lambda-pmx-model.uds -i s1 -v

DOCUMENT EXAMPLE
{"uds-path": "pipes/lambda-pmx-model.uds", "model-interface": "s1"}

FILES
~/SCS/conf/pmx_model_conf.json

SEE ALSO
scs_dev/particulates_sampler
"""

import sys

from scs_core.data.json import JSONify
from scs_core.model.pmx.pmx_model_conf import PMxModelConf

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

        conf = PMxModelConf(uds_path, model_interface)
        conf.save(Host)

    if cmd.delete and conf is not None:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
