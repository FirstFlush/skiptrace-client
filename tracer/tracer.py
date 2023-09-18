import json
import logging
from prettytable import PrettyTable
import requests
from .config import DOMAIN, LAUNCH_URL, LIST_URL
from .decryptor import FileDecryptor
from .exceptions import PasswordError
import click

logger = logging.getLogger('client')


class Tracer:

    api_headers:dict = None

    def list_spiders(self, spider_name:str=None) -> PrettyTable:

        res = requests.get(DOMAIN+LIST_URL)
        spider_details = json.loads(res.text)
        table = PrettyTable(["Spider", "Active", "Domain", "Description"])
        for spider in spider_details:
            if spider_name:
                if spider["spider_name"].lower() == spider_name.lower():
                    table.add_row(self.styled_row(spider))
            else:
                table.add_row(self.styled_row(spider))
        
        return table
        
    def styled_row(self, spider:dict) -> list:
        """Style the row visually before adding it to the table."""
        spider_name = click.style(spider["spider_name"], bold=True, underline=True)
        domain = click.style(spider["domain"], fg="green", bold=True)
        description = click.style(spider["description"], fg="green")
        if spider["is_active"]:
            is_active = click.style(spider["is_active"], fg="cyan", bold=True)
        else:
            is_active = click.style(spider["is_active"], fg="red")
        row = [spider_name, is_active, domain, description]
        return row


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