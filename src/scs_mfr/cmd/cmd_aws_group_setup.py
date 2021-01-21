"""
Created on 21 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)
Based on other cmd handlers by Bruno Beloff
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdAWSGroupSetup(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-s [-m] [-a AWS_GROUP_NAME] [-f]] [-k] [-i INDENT] [-v]",
                                              version="%prog 1.0")

        # configuration...
        self.__parser.add_option("--set", "-s", action="store_true", dest="set", default=False,
                                 help="set the group configuration")

        self.__parser.add_option("--machine-learning", "-m", action="store_true", dest="use_ml", default=False,
                                 help="enable machine learning resources for this group")

        self.__parser.add_option("--aws-group-name", "-a", type="string", action="store", dest="aws_group_name",
                                 help="override the name of the AWS group to configure ")

        self.__parser.add_option("--force", "-f", action="store_true", dest="force", default=False,
                                 help="force overwrite of existing configuration")

        # input...
        self.__parser.add_option("--stdin-key", "-k", action="store_true", dest="stdin", default=False,
                                 help="read key from stdin (--force mode only)")

        # output...
        self.__parser.add_option("--indent", "-i", action="store", dest="indent", type=int,
                                 help="pretty-print the output with INDENT")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if not self.set and (self.use_ml or self.aws_group_name or self.force):
            return False

        if self.stdin and self.set and not self.force:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def set(self):
        return self.__opts.set


    @property
    def use_ml(self):
        return self.__opts.use_ml


    @property
    def aws_group_name(self):
        return self.__opts.aws_group_name


    @property
    def force(self):
        return self.__opts.force


    @property
    def stdin(self):
        return self.__opts.stdin


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
        return "CmdAWSGroupSetup:{set:%s, use_ml:%s, aws_group_name:%s, force:%s, stdin:%s indent:%s verbose:%s}" % \
               (self.set, self.use_ml, self.aws_group_name, self.force, self.stdin, self.indent, self.verbose)
