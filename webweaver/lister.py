from datetime import datetime
import click
import json
from prettytable import PrettyTable
from requests import Response




class Lister:

    def list_spiders(self, res:Response, spider_id:int=None):
        spider_data = json.loads(res.text)

        if spider_id:
            click.echo(click.style(f"Spider id: {click.style(spider_id, bold=True)}", fg="yellow"))
            click.echo("="*75)
            self.pretty_print(spider_data)

        else:
            table = PrettyTable(["id", "Spider", "Active", "Domain", "Description"], align="l")
            for spider in spider_data:
                if len(spider['description']) > 48:
                    spider['description'] = f"{spider['description'][:45]}..."
                table.add_row(self.styled_row(spider))

            click.echo(table)


    def list_campaigns(self, res:Response, campaign_id:int=None):
        campaign_data = json.loads(res.text)
        if campaign_id:
            click.echo(click.style(f"Campaign id: {click.style(campaign_id, bold=True)}", fg="yellow"))
            click.echo("="*70)
            self.pretty_print(campaign_data)

        else:
            table = PrettyTable(["id", "campaign_name", "is_recurring"], align="l")
            for campaign in campaign_data:
                table.add_row([campaign["id"], campaign["campaign_name"], campaign["is_recurring"]])
            click.echo(table)


    def list_jobs(self, res_text:str, id:int=None, last:bool=False):
        job_data = json.loads(res_text)
        if id or last:
            click.echo(click.style(f"ScrapeJob id: {click.style(job_data['id'], bold=True)}", fg="yellow"))
            click.echo("="*70)
            del job_data['id']
            self.pretty_print(job_data)

        else:
            table = PrettyTable(["id", "campaign_id", "date_scraped"])
            for job in job_data:
                date_scraped = datetime.strptime(job["date_scraped"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d  %H:%M:%S")
                table.add_row([job["id"], job["campaign_id"], date_scraped])
            click.echo(table)


    def styled_row(self, spider:dict) -> list:
        """Style the row visually before adding it to the table."""
        id = click.style(spider["id"], fg="green")
        spider_name = click.style(spider["spider_name"], bold=True, underline=True)
        domain = click.style(spider["domain"], fg="green", bold=True)
        description = click.style(spider["description"], fg="green")
        if spider["is_active"]:
            is_active = click.style(spider["is_active"], fg="cyan", bold=True)
        else:
            is_active = click.style(spider["is_active"], fg="red")
        row = [id, spider_name, is_active, domain, description]
        return row
    

    def pretty_print(self, data, indent=0):
        for key, value in data.items():
            # Print key in bold
            click.secho(' ' * indent + str(key), bold=True, nl=False)
            if isinstance(value, dict):
                # If value is a dictionary, recursively pretty print its contents
                click.echo()  # Move to next line before printing contents
                self.pretty_print(value, indent=indent + 5)
            elif isinstance(value, list):
                # If value is a list, iterate over items and pretty print each one
                click.echo()
                for item in value:
                    self.pretty_print(item, indent=indent + 5)
            else:
                # Print value in green
                click.secho(' ' * (30 - indent - len(key)) + str(value), fg='green')







            # max_key_length = max(len(key) for key in spider_data.keys())

            # for key, value in spider_data.items():
            #     if key != "params":
            #         if value == False:
            #             click.echo(click.style(f"{key.ljust(max_key_length)}", bold=True) + "\t" + click.style(f"{value}", fg="red"))
            #         else:
            #             click.echo(click.style(f"{key.ljust(max_key_length)}", bold=True) + "\t" + click.style(f"{value}", fg="green"))
            #     else:
            #         if len(spider_data['params']) > 0:
            #             click.echo(click.style(f"{key.ljust(max_key_length)}", bold=True))
            #         else:
            #             click.echo(click.style(f"{key.ljust(max_key_length)}", bold=True)+ "\t" + click.style(None, fg="red"))
            #         for param in value:
            #             for param_key, param_value in param.items():
            #                 if param_value:
            #                     click.echo("    " + click.style(f"{param_key.ljust(max_key_length - 2)}", bold=True) + "\t" + click.style(f"{param_value}", fg="green"))
            #             click.echo()
            # click.echo()