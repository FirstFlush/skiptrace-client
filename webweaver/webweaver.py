import json
import logging
from prettytable import PrettyTable
import requests
from .config import DOMAIN, LAUNCH_URL, LIST_URL
from .decryptor import FileDecryptor
from .exceptions import PasswordError
from .launcher import Launcher
from .lister import Lister

import click

logger = logging.getLogger('client')




class WebWeaver:

    api_headers:dict = None
    LAUNCH_URL = DOMAIN+LAUNCH_URL
    LIST_URL = DOMAIN+LIST_URL
    SPIDERS = "spiders"
    CAMPAIGNS = "campaigns"
    JOBS = "jobs"


    def __init__(self):
        self.lister = Lister()
        self.launcher = Launcher()


    def list_data(self, data_type:str, id:int=None):
        if data_type == self.SPIDERS:
            res = requests.get(DOMAIN+LIST_URL, params={'spider_id':id})
            self.lister.list_spiders(res, id)

        # elif data_type == self.CAMPAIGNS:
        #     res = requests.get(DOMAIN+LIST_URL, params=)



    def get_headers(self) -> dict | None:
        """Retrieve the file headers from the encrypted vault that are 
        required to launch our spiders.
        """
        try:
            headers = FileDecryptor().decrypt()
        except PasswordError:
            headers = None
            logger.error("Incorrect password")
            logger.error("Aborting...")
        else:
            logger.info("Password correct")
            logger.info("Fetching API headers from vault...")
        return headers