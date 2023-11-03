import click
import logging
import requests
from .config import (
    DOMAIN, 
    LIST_SPIDERS_ROUTE, 
    LIST_CAMPAIGNS_ROUTE, 
    LIST_JOBS_ROUTE
)
from .decryptor import FileDecryptor
from .exceptions import PasswordError
from .launcher import Launcher
from .lister import Lister


logger = logging.getLogger('client')


class ExtensionEnum:
    JSON = "json"
    XML = "xml"
    HTML = "html"
    EXCEL = "xlsx"
    CSV = "csv"
    FEATHER = "feather"
    TXT = "txt"
    SQLITE = "sqlite"
    SQL = "dump"
    PARQUET = "parquet"
    GOOGLE_SHEETS = "xlsx"


class GroupEnum:
    SPIDERS = "spiders"
    CAMPAIGNS = "campaigns"
    JOBS = "jobs"


class WebWeaver:

    api_headers:dict = None
    # LAUNCH_URL = DOMAIN+LAUNCH_URL
    LIST_SPIDERS_URL = DOMAIN+LIST_SPIDERS_ROUTE
    LIST_CAMPAIGNS_URL = DOMAIN+LIST_CAMPAIGNS_ROUTE
    LIST_JOBS_URL = DOMAIN+LIST_JOBS_ROUTE


    def __init__(self):
        self.lister = Lister()
        self.launcher = Launcher()
        self.group = GroupEnum
        self.ext = ExtensionEnum
        self.ext_set = self.get_ext_set()


    def get_ext_set(self) -> set:
        """Returns a set of allowed file extensions."""
        return {value for key, value in vars(self.ext).items() if not key.startswith("__")}


    def ext_list(self) -> list:
        return list(self.ext_set)

    def print_ext_list(self, extension:str):
        click.echo(f"File extension '.{extension}' {click.style('invalid', fg='red')}.")
        click.echo("Acceptable file types:")
        for ext in self.ext_list():
            click.echo(f"  .{ext}")


    def launch(self, enum:str, id:int, ext:str=None):
        launch_headers = self.get_headers()
        if enum == self.group.CAMPAIGNS:
            self.launcher.launch_campaign(launch_headers, id)
        elif enum == self.group.SPIDERS:
            self.launcher.launch_spider(launch_headers, id)


    def list_data(self, enum:str, id:int=None, **kwargs):
        if enum == self.group.SPIDERS:
            res = requests.get(self.LIST_SPIDERS_URL, params={'spider_id':id})
            self.lister.list_spiders(res, id)

        elif enum == self.group.CAMPAIGNS:
            res = requests.get(self.LIST_CAMPAIGNS_URL, params={'campaign_id':id})
            self.lister.list_campaigns(res, id)

        elif enum == self.group.JOBS:
            if kwargs.get('last'):
                res = requests.get(self.LIST_JOBS_URL, {'last':True})
                self.lister.list_jobs(res.text, last=True)
            else:
                res = requests.get(self.LIST_JOBS_URL, {'job_id':id})
                self.lister.list_jobs(res.text, id)


    def get_headers(self) -> dict | None:
        """Retrieve the file headers from the encrypted vault that are 
        required to launch our spiders.
        """
        try:
            headers = FileDecryptor().decrypt()
        except PasswordError as e:
            headers = None
            logger.error(f"{e.__class__.__name__}: Incorrect password")
            logger.info("Aborting...")
            exit(0)
        else:
            logger.info("Password correct")
            logger.info("Fetching API headers from vault...")
        return headers