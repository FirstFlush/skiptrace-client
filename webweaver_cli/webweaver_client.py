import click
import json
import logging
import requests
from .config import (
    DOMAIN, 
    LIST_PARAMS_ROUTE,
    LIST_SPIDERS_ROUTE, 
    LIST_CAMPAIGNS_ROUTE, 
    LIST_JOBS_ROUTE,
    SAVE_JOB_TO_FILE_ROUTE
)
from .create_spider import create_spider_script
from .decryptor import FileDecryptor
from .exceptions import PasswordError
from .launcher import Launcher
from .lister import Lister


logger = logging.getLogger('client')


class FileFormat:
    JSON = "json"
    XML = "xml"
    HTML = "html"
    EXCEL = "excel"
    CSV = "csv"
    FEATHER = "feather"
    TXT = "txt"
    SQLITE = "sqlite"
    SQL = "dump"
    PARQUET = "parquet"
    GOOGLE_SHEETS = "gsheets"




class GroupEnum:
    SPIDERS = "spiders"
    CAMPAIGNS = "campaigns"
    JOBS = "jobs"


class WebWeaverClient:

    api_headers:dict[str, str] = None
    LIST_PARAMS_URL = DOMAIN+LIST_PARAMS_ROUTE
    LIST_SPIDERS_URL = DOMAIN+LIST_SPIDERS_ROUTE
    LIST_CAMPAIGNS_URL = DOMAIN+LIST_CAMPAIGNS_ROUTE
    LIST_JOBS_URL = DOMAIN+LIST_JOBS_ROUTE
    SAVE_JOBS_URL = DOMAIN+SAVE_JOB_TO_FILE_ROUTE

    def __init__(self):
        self.lister = Lister()
        self.launcher = Launcher()
        self.group = GroupEnum
        self.file_formats = FileFormat
        self.file_format_set = self._create_file_format_set()


    
    def create_spider(self):
        create_spider_script()



    def save_job_to_file(self, id:int, file_format:str):
        """Ensure the file is in the file_format_set and 
        then send the data to the server's save route.
        """
        while file_format not in self.file_format_set:
            file_format = self.print_file_format_list(file_format)
            file_format = input('\nFile format: ')
        json_data = {
            'id':id,
            'file_format':file_format
        }
        requests.post(self.SAVE_JOBS_URL, json=json_data)


    def _create_file_format_set(self) -> set:
        """Creates a set of allowed file types from the FileFormat class."""
        return {value for key, value in vars(self.file_formats).items() if not key.startswith("__")}


    def file_format_list(self) -> list:
        return sorted(list(self.file_format_set))


    def print_file_format_list(self, user_file_type:str=None):
        """Prints the possible file type formatting options.
        Prints an error message if user-submitted file type is invalid.
        """
        if user_file_type != None:
            click.echo(f"File extension '.{user_file_type}' {click.style('invalid', fg='red')}.")
            click.echo()
        click.echo("Acceptable file types:")
        for file_type in self.file_format_list():
            click.echo(f"    -{click.style(file_type, fg='green')}")


    def launch(self, group_enum:str, id:int, file_format:str=None, scrape_job:int=None):
        if group_enum == self.group.CAMPAIGNS:
            launch_headers = self.get_headers()
            self.lister.title("Launch Campaign id: ", id)
            self.launcher.launch_campaign(launch_headers, id, file_format)

        elif group_enum == self.group.SPIDERS:
            launch_data = {
                'id': id,
                'file_format': file_format,
                'params': [],
                'scrape_job_id': scrape_job,
            }
            params_data = self._get_spider_params(id)
            self.lister.title("Launch Spider id: ", id)
            for param in params_data['params']:
                self.lister.pretty_print(param)
                param_value = click.prompt(click.style('\n>> Enter parameter value: '))
                d = {}
                d['param_name'] = param['param_name']
                d['param_value'] = param_value
                launch_data['params'].append(d)
            print(launch_data)

            launch_headers = self.get_headers()
            self.launcher.launch_spider(launch_headers, launch_data)


    def _get_spider_params(self, spider_id:int) -> dict[str, list[dict[str, str]]]:
        res_params = requests.get(self.LIST_PARAMS_URL, params={'id':spider_id})
        return json.loads(res_params.text)


    def list_data(self, enum:str, id:int=None, **kwargs):
        match enum:
            case self.group.SPIDERS:
                res = requests.get(self.LIST_SPIDERS_URL, params={'spider_id':id})
                self.lister.list_spiders(res, id)

            case self.group.CAMPAIGNS:
                res = requests.get(self.LIST_CAMPAIGNS_URL, params={'campaign_id':id})
                self.lister.list_campaigns(res, id)

            case self.group.JOBS:
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