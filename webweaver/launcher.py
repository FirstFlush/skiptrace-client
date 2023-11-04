import requests
from .config import DOMAIN, LAUNCH_CAMPAIGN_ROUTE, LAUNCH_SPIDER_ROUTE

class Launcher:
    
    LAUNCH_CAMPAIGN_URL = DOMAIN+LAUNCH_CAMPAIGN_ROUTE
    LAUNCH_SPIDER_URL = DOMAIN+LAUNCH_SPIDER_ROUTE
    
    def launch_spider(self, launch_headers:dict, spider_id:int, file_format:str=None):
        """Launches a spider"""
        json_data = {
            'id':spider_id,
            'file_format': file_format,
        }
        res = requests.post(
            self.LAUNCH_SPIDER_URL,
            headers=launch_headers,
            json=json_data
        )
        print(res.status_code)


    def launch_campaign(self, launch_headers:dict, campaign_id:int, file_format:str):
        """Launches a campaign"""
        json_data = {
            'id': campaign_id,
            'file_format': file_format,
        }
        res = requests.post(
            self.LAUNCH_CAMPAIGN_URL,
            headers=launch_headers,
            json=json_data
        )
        print(res)
        print(res.status_code)
