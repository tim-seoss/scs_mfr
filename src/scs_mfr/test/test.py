"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from abc import ABC, abstractmethod


# --------------------------------------------------------------------------------------------------------------------

class Test(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, interface, verbose):
        self.__interface = interface
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
    def interface(self):
        return self.__interface


    @property
    def verbose(self):
        return self.__verbose


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{datum:%s, interface:%s, verbose:%s}" % \
               (self.datum, self.__interface, self.verbose)
