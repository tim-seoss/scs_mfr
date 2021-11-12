"""
Created on 21 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""

import optparse

from scs_core.aws.greengrass.aws_group_configuration import AWSGroupConfiguration


# --------------------------------------------------------------------------------------------------------------------

class CmdAWSGroupSetup(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        templates = ' | '.join(AWSGroupConfiguration.templates())

        self.__parser = optparse.OptionParser(usage="%prog [-s TEMPLATE [-a AWS_GROUP_NAME] [-f]] [-k] "
                                                    "[-i INDENT] [-v]", version="%prog 1.0")

        # configuration...
        self.__parser.add_option("--set", "-s", type="string", action="store", dest="set",
                                 help="set the group configuration with template { %s }" % templates)

        self.__parser.add_option("--aws-group-name", "-a", type="string", action="store", dest="aws_group_name",
                                 help="override the name of the AWS group to configure")

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
        if self.set is None and (self.aws_group_name is not None or self.force):
            return False

        if self.set is not None and self.set not in AWSGroupConfiguration.templates():
            return False

        if self.set is not None and self.stdin and not self.force:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def set(self):
        return self.__opts.set


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
        return "CmdAWSGroupSetup:{set:%s, aws_group_name:%s, force:%s, stdin:%s indent:%s verbose:%s}" % \
               (self.set, self.aws_group_name, self.force, self.stdin, self.indent, self.verbose)
