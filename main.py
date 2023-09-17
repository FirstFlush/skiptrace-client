import click
import logging
import pyfiglet
import requests
from tracer.tracer import Tracer


logger = logging.getLogger('client')


banner = pyfiglet.figlet_format("Tracer")
click.echo(banner)

@click.group()
def tracer():
    """Client-side CLI tool for interacting with the spider server"""
    pass



@tracer.command()
@click.option('--all', 'all_spiders', is_flag=True, help='List all spiders.')
@click.option('-s', 'spider_name', type=str, help='List a single spider by name.')
def list(all_spiders, spider_name):
    """List spider details."""
    tracer = Tracer()
    if all_spiders:    
        table = tracer.list()
    elif spider_name:
        table = tracer.list(spider_name)
    else:
        click.echo("Please specify --all or provide a spider name with -s.")

    click.echo(table)



@tracer.command()
@click.option('--all', 'all_spiders', is_flag=True, help='Launch all spiders.')
@click.option('-s', 'spider_name', type=str, help='Launch a single spider by name.')
def launch(all_spiders, spider_name):
    """Launch spiders for scraping."""
    tracer = Tracer()
    headers = tracer.get_headers()
    if headers is None:
        exit(0)

    if all_spiders:
        tracer.launch_all(headers)

    elif spider_name:
        tracer.launch_one(headers, spider_name)

    else:
        click.echo("Please specify --all or provide a spider name with -s.")

