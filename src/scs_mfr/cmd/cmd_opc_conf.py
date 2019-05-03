"""
Created on 13 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_dfe.particulate.opc_conf import OPCConf


# --------------------------------------------------------------------------------------------------------------------

class CmdOPCConf(object):
    """
    unix command line handler
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        self.__parser = optparse.OptionParser(usage="%prog [{ [-m MODEL] [-s SAMPLE_PERIOD] [-p { 0 | 1 }] "
                                                    "[-b SPI_BUS] [-c SPI_DEVICE] | -d }] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--model", "-m", type="string", nargs=1, action="store", dest="model",
                                 help="set MODEL (N2, N3, R1 or S30)")

        self.__parser.add_option("--sample-period", "-s", type="int", nargs=1, action="store", dest="sample_period",
                                 help="set SAMPLE_PERIOD")

        self.__parser.add_option("--power-saving", "-p", type="int", nargs=1, action="store", dest="power_saving",
                                 help="set power saving mode")

        self.__parser.add_option("--spi-bus", "-b", type="int", nargs=1, action="store", dest="spi_bus",
                                 help="override host SPI bus")

        self.__parser.add_option("--spi-device", "-c", type="int", nargs=1, action="store", dest="spi_device",
                                 help="override host SPI chip select")


        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete",
                                 help="delete the OPC configuration")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.set() and self.delete:
            return False

        if self.model and not OPCConf.is_valid_model(self.model):
            return False

        if self.__opts.power_saving is None or self.__opts.power_saving == 0 or self.__opts.power_saving == 1:
            return True

        return False


    def is_complete(self):
        if self.model is None or self.sample_period is None or self.power_saving is None:
            return False

        return True


    def set(self):
        return self.model is not None or self.sample_period is not None or self.power_saving is not None \
               or self.spi_bus is not None or self.spi_device is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return self.__opts.model


    @property
    def sample_period(self):
        return self.__opts.sample_period


    @property
    def power_saving(self):
        return None if self.__opts.power_saving is None else bool(self.__opts.power_saving)


    @property
    def delete(self):
        return self.__opts.delete


    @property
    def spi_bus(self):
        return self.__opts.spi_bus


    @property
    def spi_device(self):
        return self.__opts.spi_device


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdOPCConf:{model:%s, sample_period:%s, ext_addr:%s, spi_bus:%s, spi_device:%s, " \
               "delete:%s, verbose:%s}" % \
               (self.model, self.sample_period, self.power_saving, self.spi_bus, self.spi_device,
                self.delete, self.verbose)
