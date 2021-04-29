"""
Created on 08 Feb 2021

@author: Jade Page (jade.page@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdAWSGroupCloner(object):
    """unix command line handler"""

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog { -s SOURCE-GROUP-NAME } [-d DEST-GROUP-NAME] [-g] [-p] "
                                                    "[-v] [-i INDENT]", version="%prog 1.0")

        # compulsory...
        self.__parser.add_option("--source-group-name", "-s", action="store", dest="group_name",
                                 help="the group for which to base the deployments on")

        self.__parser.add_option("--dest-group-name", "-d", action="store", dest="dest",
                                 help="deploy to names in the list")

        # options...
        self.__parser.add_option("--gasses", "-g", action="store_true", dest="gas",
                                 help="Add the gasses ML to this group ")

        self.__parser.add_option("--particulates", "-p", action="store_true", dest="parts",
                                 help="Add the particulates ML to this group ")

        # reporting flags...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__parser.add_option("--indent", "-i", type="int", nargs=1, action="store", dest="indent",
                                 help="indent report by INDENT")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if not self.group_name:
            return False

        if not self.dest:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def group_name(self):
        return self.__opts.group_name

    @property
    def dest(self):
        return self.__opts.dest

    @property
    def gas(self):
        return self.__opts.gas

    @property
    def parts(self):
        return self.__opts.parts


    @property
    def indent(self):
        return self.__opts.indent

    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdAWSGroupCloner:{ group_name:%s,  dest:%s, gas:%s, parts:%s, indent:%s, verbose:%s}" % \
               (self.group_name, self.dest, self.gas, self.parts, self.indent, self.verbose)
