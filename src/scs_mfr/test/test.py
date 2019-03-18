"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from abc import abstractmethod


# --------------------------------------------------------------------------------------------------------------------

class Test(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, verbose):
        self.__verbose = verbose

        self._datum = None


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def conduct(self):
        pass


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def datum(self):
        return self._datum


    @property
    def verbose(self):
        return self.__verbose


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{datum:%s, verbose:%s}" % (self.datum, self.verbose)
