import click
import logging
import pyfiglet
# import requests
from webweaver.webweaver import WebWeaver
from webweaver.create_spider import CreateSpider

logger = logging.getLogger('client')

banner = pyfiglet.figlet_format("Web Weaver")
click.echo()
click.echo(banner)



@click.group()
def webweaver():
    """Client-side CLI tool for interacting with the spider server"""
    webweaver = WebWeaver()
    pass


# For the `campaigns` command group
@click.group()
def campaigns():
    """Manage campaigns."""
    pass


@campaigns.command()
@click.option('--all', is_flag=True, help='List all campaigns.')
@click.argument('campaign_name', required=False)
def list(all, campaign_name):
    """List campaigns. If a campaign name is provided, details of that specific campaign will be shown."""
    if all:
        # Logic to list all campaigns
        click.echo("Listing all campaigns...")
    elif campaign_name:
        # Logic to list a specific campaign
        click.echo(f"Details for campaign: {campaign_name}")
    else:
        click.echo("Please specify either --all or provide a campaign name.")


@campaigns.command()
def launch():
    """Launch a campaign."""
    # Your code to launch a campaign goes here.
    click.echo("Launching campaign...")

# Add the campaigns group to the main cli group
webweaver.add_command(campaigns)





# For the `spiders` command group
@click.group()
def spiders():
    """Manage spiders."""
    pass


@spiders.command()
@click.option('--all', is_flag=True, help='List all spiders.')
@click.argument('spider_number', required=False)
def list(all:bool, spider_number:int):
    """List spiders. If a spider name is provided, details of that specific spider will be shown."""
    weaver = WebWeaver()
    if all:
        weaver.list_data(weaver.SPIDERS)
    elif spider_number:
        weaver.list_data(weaver.SPIDERS, spider_number)
    else:
        click.echo("Please specify either --all or provide a spider's id.")


@spiders.command(help="Launch a spider by its id.")
@click.argument('spider_number', required=True, type=int)
def launch(spider_number):
    """Function logic for launching spider."""
    pass

@spiders.command()
def create():
    """Create a new spider."""
    # Your code to create a spider goes here.
    click.echo("Creating spider...")

# Add the spiders group to the main cli group
webweaver.add_command(spiders)

# For the `jobs` command group
@click.group()
def jobs():
    """Manage jobs."""
    pass

@jobs.command()
def list():
    """List all jobs."""
    # Your code to list jobs goes here.
    click.echo("Listing all jobs...")

# Add the jobs group to the main cli group
webweaver.add_command(jobs)

if __name__ == '__main__':
    webweaver()





# @webweaver.command()
# def create():
#     """Create a new spider."""
#     CreateSpider().create_scraper()


# @webweaver.command()
# @click.option('--all', 'all_spiders', is_flag=True, help='List all spiders.')
# @click.option('-s', 'spider_name', type=str, help='List a single spider by name.')
# def list(all_spiders, spider_name):
#     """List spider details."""
#     webweaver = webweaver()
#     if all_spiders:
#         table = webweaver.list_spiders()
#     elif spider_name:
#         table = webweaver.list_spiders(spider_name)
#     else:
#         click.echo("Please specify --all or provide a spider name with -s.")

#     click.echo(table)


# @webweaver.command()
# @click.option('--all', 'all_spiders', is_flag=True, help='Launch all spiders.')
# @click.option('-c', 'campaign', type=str, help='Launch a scraping campaign.')
# @click.option('-s', 'spider_name', type=str, help='Launch a single spider by name.')
# def launch(all_spiders, campaign, spider_name):
#     """Launch spiders for scraping."""
#     webweaver = webweaver()
#     headers = webweaver.get_headers()
#     if headers is None:
#         exit(0)

#     if all_spiders:
#         webweaver.launch_all(headers)

#     elif spider_name:
#         webweaver.launch_one(headers, spider_name)

#     elif campaign:
#         webweaver.launch_campaign(headers, campaign)

#     else:
#         click.echo("Please specify a spider or campaign for scraping.")

