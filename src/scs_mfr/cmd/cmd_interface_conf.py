"""
Created on 27 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_dfe.interface.interface_conf import InterfaceConf


# --------------------------------------------------------------------------------------------------------------------

class CmdInterfaceConf(object):
    """
    unix command line handler
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        self.__parser = optparse.OptionParser(usage="%prog [{ [-m MODEL] [-i INFERENCE_UDS] | -d }] [-v]",
                                              version="%prog 1.0")

        models = ' | '.join(InterfaceConf.models())

        # optional...
        self.__parser.add_option("--model", "-m", type="string", nargs=1, action="store", dest="model",
                                 help="interface model { %s }" % models)

        self.__parser.add_option("--inference", "-i", type="string", nargs=1, action="store", dest="inference",
                                 help="set inference server UDS")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the interface configuration")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.set() and self.delete:
            return False

        if self.set() and self.model not in InterfaceConf.models():
            return False

        return True


    def set(self):
        return self.model is not None or self.inference is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return self.__opts.model


    @property
    def inference(self):
        return self.__opts.inference


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
        return "CmdInterfaceConf:{source:%s, inference:%s, delete:%s, verbose:%s}" % \
               (self.__opts.source, self.inference, self.delete, self.verbose)
