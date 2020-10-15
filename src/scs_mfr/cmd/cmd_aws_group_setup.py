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
        self.__parser = optparse.OptionParser(usage="%prog { -c | -s } [-m] [-a AWS_GROUP_NAME] [-v]",
                                              version="%prog 1.0")

        # optional...
        self.__parser.add_option("--current", "-c", action="store_true", dest="show_current", default=False,
                                 help="view the current group configuration")

        self.__parser.add_option("--set", "-s", action="store_true", dest="set", default=False,
                                 help="set the group configuration")

        self.__parser.add_option("--machine-learning", "-m", action="store_true", dest="use_ml", default=False,
                                 help="enable machine learning resources for this group")

        self.__parser.add_option("--aws-group-name", "-a", type="string", action="store", dest="aws_group_name",
                                 help="override the name of the AWS group to configure ")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()

    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if bool(self.show_current) == bool(self.set):
            return False
        return True

    # ----------------------------------------------------------------------------------------------------------------

    @property
    def show_current(self):
        return self.__opts.show_current

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
    def verbose(self):
        return self.__opts.verbose

    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)

    def __str__(self, *args, **kwargs):
        return "CmdAWSGroupSetup:{current:%s, set:%s, machine-learning:%s, aws-group-name:%s, verbose:%s}" % \
               (self.show_current, self.set, self.use_ml, self.aws_group_name, self.verbose)
