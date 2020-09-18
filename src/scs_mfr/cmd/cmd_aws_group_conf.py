import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdAWSGroupConfig(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog { [-r ROOT_PATH] | "
                                                    "-d } [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--root", "-r", type="string", nargs=1, action="store", dest="root_path",
                                 help="set filesystem logging directory")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the logger configuration")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()

    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.set() and self.delete:
            return False

        return True

    def is_complete(self):
        if self.root_path is None or self.delete is None:
            return False

        return True

    def set(self):
        if self.root_path is not None:
            return True

        return False

    # ----------------------------------------------------------------------------------------------------------------

    @property
    def root_path(self):
        return self.__opts.root_path

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
        return "CmdCSVLoggerConf:{root_path:%s, delete:%s, verbose:%s}" % \
               (self.root_path, self.delete, self.verbose)
