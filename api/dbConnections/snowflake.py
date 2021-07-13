import json
import logging


logger = logging.getLogger(__name__)


class Snowflake:
    """
    Class to support functionalities of Snowflake connection
    """

    @staticmethod
    def checkConnection():
        """
        Connection for Snowflake database
        """
        res = True
        return res