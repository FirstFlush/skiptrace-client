import json
import logging
from prettytable import PrettyTable
import requests
from .config import DOMAIN, LAUNCH_URL, LIST_URL
from .decryptor import FileDecryptor
from .exceptions import PasswordError


logger = logging.getLogger('client')


class Tracer:

    api_headers:dict = None

    def list(self, spider_name:str=None) -> PrettyTable:

        res = requests.get(DOMAIN+LIST_URL)
        spider_details = json.loads(res.text)
        table = PrettyTable(["Spider", "Active", "Description"])
        for spider in spider_details:
            if spider_name:
                if spider["spider_name"].lower() == spider_name.lower():
                    table.add_row([spider["spider_name"], spider["is_active"], spider["description"]])
            else:
                table.add_row([spider["spider_name"], spider["is_active"], spider["description"]])
        
        return table
        


    def launch_all(self, api_headers:dict):
        """Launch all spiders"""
        logger.info("Launching all spiders...")
        headers = api_headers
        res = requests.post(DOMAIN+LAUNCH_URL, headers=headers)
        logger.info("Scraping complete")

        print(res.status_code)



    def launch_one(self, api_headers:dict, spider_name:str):
        """Launches a single spider"""
        logger.info(f"Launching spider: {spider_name}")


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