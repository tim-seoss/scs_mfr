"""
Created on 17 May 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_core.comms.mqtt_conf import MQTTConf


# --------------------------------------------------------------------------------------------------------------------

class CmdMQTTConf(object):
    """
    unix command line handler
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        self.__parser = optparse.OptionParser(usage="%prog { [-p INHIBIT_PUBLISHING] [-q QUEUE_SIZE] [-f REPORT_FILE] "
                                                    "| -d } [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--pub", "-p", type="int", nargs=1, action="store", dest="inhibit_publishing",
                                 help="inhibit publishing (1) or enable (0)")

        self.__parser.add_option("--queue_size", "-q", type="int", nargs=1, action="store", dest="queue_size",
                                 help="queue size (default is %s)" % MQTTConf.DEFAULT_QUEUE_SIZE)

        self.__parser.add_option("--report-file", "-f", type="string", nargs=1, action="store", dest="report_file",
                                 help="file to store latest queue length value")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="revert to the default MQTT configuration")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.set and self.delete:
            return False

        return True


    def set(self):
        return self.inhibit_publishing is not None or self.queue_size is not None or self.report_file is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def inhibit_publishing(self):
        return self.__opts.inhibit_publishing


    @property
    def queue_size(self):
        return self.__opts.queue_size


    @property
    def report_file(self):
        return self.__opts.report_file


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
        return "CmdMQTTConf:{inhibit_publishing:%s, queue_size:%s, report_file:%s, delete:%s, verbose:%s}" % \
               (self.inhibit_publishing, self.queue_size, self.report_file, self.delete, self.verbose)
