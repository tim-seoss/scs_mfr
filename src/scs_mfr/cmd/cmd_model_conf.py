"""
Created on 22 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_core.aws.greengrass.aws_group_configuration import AWSGroupConfiguration
from scs_core.model.gas.gas_model_conf import GasModelConf


# --------------------------------------------------------------------------------------------------------------------

class CmdModelConf(object):
    """
    unix command line handler
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        interface_names = ' | '.join(GasModelConf.interfaces())
        group_names = ' | '.join(AWSGroupConfiguration.templates())

        self.__parser = optparse.OptionParser(usage="%prog [{ -l | [-u UDS_PATH] [-i INTERFACE] [-g GROUP] | -d }] "
                                                    "[-v]", version="%prog 1.0")

        # functions...
        self.__parser.add_option("--list", "-l", action="store_true", dest="list", default=False,
                                 help="list the available model compendium groups")

        self.__parser.add_option("--uds-path", "-u", type="string", nargs=1, action="store", dest="uds_path",
                                 help="set the UDS path (relative to ~/SCS)")

        self.__parser.add_option("--interface", "-i", type="string", nargs=1, action="store", dest="model_interface",
                                 help="set the interface code { %s }" % interface_names)

        self.__parser.add_option("--group", "-g", type="string", nargs=1, action="store", dest="model_compendium_group",
                                 help="set the model compendium group { %s }" % group_names)

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the inference configuration")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        count = 0

        if self.list:
            count += 1

        if self.set():
            count += 1

        if self.delete:
            count += 1

        if count > 1:
            return False

        if self.model_interface and self.model_interface not in GasModelConf.interfaces():
            return False

        return True


    def is_complete(self):
        if self.uds_path is None or self.model_interface is None:
            return False

        return True


    def set(self):
        return self.uds_path is not None or self.model_interface is not None or self.model_compendium_group is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def list(self):
        return self.__opts.list


    @property
    def uds_path(self):
        return self.__opts.uds_path


    @property
    def model_interface(self):
        return self.__opts.model_interface


    @property
    def model_compendium_group(self):
        return self.__opts.model_compendium_group


    @property
    def delete(self):
        return self.__opts.delete


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdModelConf:{list:%s, uds_path:%s, model_interface:%s, model_compendium_group:%s, delete:%s, " \
               "verbose:%s}" % \
               (self.list, self.uds_path, self.model_interface, self.model_compendium_group, self.delete,
                self.verbose)
