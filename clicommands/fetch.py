import click
from clicommands.analisys_comands import fetch_all as analisys_fetch_all


@click.group()
def fetch():
    """
        Fetch and store the Analysis resources
    """
    click.echo("Inside fetch group")


# Analysis Commands
@fetch.command()
def analysis():
    click.echo("Fetching Analysis")

@fetch.command()
@click.option('--account-id', required=True, help='The origin account id')
@click.option('--profile', default=None, help='Local AWS profile')
def analyses(account_id, profile):
    assert account_id is not None, "--account-id must be provided"
    click.echo(f"Fetching All Analyses from account={account_id}")
    click.echo(f"AWS Profile={profile}")
    analisys_fetch_all(account_id, profile)
    pass


# DataSources Commands
@fetch.command()
def data_source():
    click.echo("Fetching DataSources")

@fetch.command()
def data_sources():
    click.echo("Fetching multiple DataSources")


# DataSources Commands
@fetch.command()
def data_set():
    click.echo("Fetching DataSets")

@fetch.command()
def data_sets():
    click.echo("Fetching multiple DataSets")


# Dashboards Commands
@fetch.command()
def dashboard():
    click.echo("Fetching Dashboard")

@fetch.command()
def dashboards():
    click.echo("Fetching multiple Dashboards")

