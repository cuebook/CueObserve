import json
import logging


logger = logging.getLogger(__name__)


class Redshift:
    """
    Class to support functionalities of Redshift connection
    """

    @staticmethod
    def checkConnection():
        """
        Connection for Redshift database
        """
        res = True
        return res