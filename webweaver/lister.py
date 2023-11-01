import click
import json
from prettytable import PrettyTable
from requests import Response




class Lister:

    def list_spiders(self, res:Response, spider_id:int=None):
        spider_data = json.loads(res.text)

        if spider_id:
            max_key_length = max(len(key) for key in spider_data.keys())

            for key, value in spider_data.items():
                if key != "params":
                    if value == False:
                        click.echo(click.style(f"{key.ljust(max_key_length)}", bold=True) + "\t" + click.style(f"{value}", fg="red"))
                    else:
                        click.echo(click.style(f"{key.ljust(max_key_length)}", bold=True) + "\t" + click.style(f"{value}", fg="green"))
                else:
                    if len(spider_data['params']) > 0:
                        click.echo(click.style(f"{key.ljust(max_key_length)}", bold=True))
                    else:
                        click.echo(click.style(f"{key.ljust(max_key_length)}", bold=True)+ "\t" + click.style(None, fg="red"))
                    for param in value:
                        for param_key, param_value in param.items():
                            if param_value:
                                click.echo("    " + click.style(f"{param_key.ljust(max_key_length - 2)}", bold=True) + "\t" + click.style(f"{param_value}", fg="green"))
                        click.echo()
            click.echo()
        else:
            table = PrettyTable(["id", "Spider", "Active", "Domain", "Description"], align="l")
            for spider in spider_data:
                if len(spider['description']) > 48:
                    spider['description'] = f"{spider['description'][:45]}..."
                table.add_row(self.styled_row(spider))

            click.echo(table)


    def list_campaigns(self):
        ...


    def list_jobs(self):
        ...

        
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