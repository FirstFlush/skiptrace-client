#!/usr/bin/env python3
import requests
from webweaver.config import DOMAIN, CREATE_SPIDER_URL


class CreateSpider:

    def __init__(self):
        self.spider_name = None
        self.spider_type = None
        self.domain = None
        self.is_search_string = None
        self.description = None

    def _fail(self, msg:str="Bruh..."):
        """Wtf?"""
        print(msg)
        exit(1)

    def create_scraper(self):
        """Creates a SpiderAsset DB object and generates all the module files
        required to start scraping.
        """
        self._create_spider_details()
        print(f"\nSpider Name:\t{self.spider_name}\nDirectory:\t{self.spider_name.lower()}/\nSpider Type:\t{self.spider_type}\nStarting Url:\t{self.domain}\nSearch String:\t{self.is_search_string}\nDescription:\t{self.description}\n")
        confirm = input("Confirm details? (y/n): ").lower()
        if confirm != 'y':
            self._fail()

        status_code = self._send_asset_details()
        if status_code != 200:
            self._fail("Spider rejected. lol")


        print(f"\nSpider \033[1m{self.spider_name}\033[0m successfully created.\nHappy scraping!\n")
        exit(0)


    def _send_asset_details(self) -> int:
        """Sends the SpiderAsset details to the app's route for creating 
        new SpiderAsset objects, then returns the status code.
        """
        data = {
            'spider_asset': {
                'spider_name': self.spider_name,
                'domain': self.domain,
                'description': self.description,
                'is_active': True,
                'is_search_string': self.is_search_string
            },
            'spider_module': {
                'spider_type': self.spider_type,
            },
        }
        response = requests.post(f"{DOMAIN+CREATE_SPIDER_URL}", json=data)
        return response.status_code


    def _create_spider_details(self):
        """Creates a dictionary of all details required for a new SpiderAsset model object.
        Does not create the model object until after we have verified 
        """
        self.spider_name = input("Spider Name: ")
        spider_type_choice = input("Async or Playwright spider? (a/p): ")
        match spider_type_choice.lower():
            case "a":
                self.spider_type = "AsyncSpider"
            case "p":
                self.spider_type = "PlaywrightSpider"
            case _:
                self._fail()
        self.domain = input("Website domain: ")
        is_search_string = input("Is a search-string required to scrape (y/n): ")
        match is_search_string.lower():
            case "y":
                self.is_search_string = True
            case "n":
                self.is_search_string = False
            case _:
                self._fail()
        self.description = input("Description: ")
        if self.spider_name[-6:] == "Spider":
            self.spider_name = self.spider_name[:-6]

        return


if __name__ == "__main__":
    CreateSpider().create_scraper()