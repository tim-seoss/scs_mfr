"""
Created on 18 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"username": "southcoastscience-dev", "client-id": "5406", "client-password": "jtxSrK2e"}
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdOSIOClientAuth(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-s USERNAME CLIENT_ID CLIENT_PASSWORD] [-v]",
                                              version="%prog 1.0")

        # optional...
        self.__parser.add_option("--set", "-s", type="string", nargs=3, action="store", dest="username_client_password",
                                 help="username, client ID and password")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def set(self):
        return self.__opts.username_client_password is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def username(self):
        return self.__opts.username_client_password[0] if self.__opts.username_client_password else None


    @property
    def client_id(self):
        return self.__opts.username_client_password[1] if self.__opts.username_client_password else None


    @property
    def client_password(self):
        return self.__opts.username_client_password[2] if self.__opts.username_client_password else None


    @property
    def verbose(self):
        return self.__opts.verbose


    @property
    def args(self):
        return self.__args


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CmdOSIOClientAuth:{username:%s, client_id:%s, client_password:%s, verbose:%s, args:%s}" % \
               (self.username, self.client_id, self.client_password, self.verbose, self.args)
