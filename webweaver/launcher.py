import requests
from .config import DOMAIN, LAUNCH_CAMPAIGN_ROUTE, LAUNCH_SPIDER_ROUTE

class Launcher:
    
    LAUNCH_CAMPAIGN_URL = DOMAIN+LAUNCH_CAMPAIGN_ROUTE
    LAUNCH_SPIDER_URL = DOMAIN+LAUNCH_SPIDER_ROUTE
    
    def launch_spider(self, launch_headers:dict, spider_id:int):
        """Launches a spider"""
        res = requests.post(
            self.LAUNCH_SPIDER_URL,
            headers=launch_headers,
            json={'id':spider_id}
        )
        print(res.status_code)


    def launch_campaign(self, launch_headers:dict, campaign_id:int):
        """Launches a campaign"""
        res = requests.post(
            self.LAUNCH_CAMPAIGN_URL,
            headers=launch_headers,
            json={'id':campaign_id}
        )
        print(res)
        print(res.status_code)
