import click
import os
import boto3
from infra_base.qs_fetch import fetchQSAllResources
from qs.utils import mask_aws_account_id

from clicommands.data_source_commands import fetch_all as data_source_fetch_all
from clicommands.data_set_commands import fetch_all as data_set_fetch_all
from clicommands.analisys_commands import fetch_all as analisys_fetch_all
from clicommands.dashboard_commands import fetch_all as dashboard_fetch_all

from clicommands.athena_commands import fetch_all as athena_fetch_all
from clicommands.athena_commands import fetch_workgroups as athena_fetch_workgroups
from clicommands.athena_commands import fetch_data_catalogs as athena_fetch_data_catalogs

from clicommands.glue_commands import fetch_all as glue_fetch_all

@click.group()
def fetch():
    """
        Fetch and store the description of Quicksight, Athena and Glue resources
    """

@fetch.command()
@click.option('--account-id', default="aaa-bbb-ccc-ddd", help='The origin account id')
@click.option('--profile', default=None, help='AWS CLI Profile')
def all(account_id, profile):
    click.echo('Fetching all resources from Quicksight, Athena and Glue.')
    click.echo(f'AWS Account ID: {account_id}')
    click.echo(f'Output directory: ./infra_base/{mask_aws_account_id(account_id)}/')
    os.environ['ORIGIN_AWS_ACCOUNT_ID']= account_id
    session = boto3.Session(profile_name=profile)

    quicksight_client = session.client('quicksight',region_name='us-east-1')
    fetchQSAllResources(quicksight_client, account_id)
    
    athena_fetch_all(account_id, profile)

    glue_fetch_all(account_id, profile)


################################
### Analyses Commands
################################
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


################################
### DataSources Commands
################################
@fetch.command()
def data_source():
    click.echo("Fetching DataSources")

@fetch.command()
@click.option('--account-id', required=True, help='The origin account id')
@click.option('--profile', default=None, help='Local AWS profile')
def data_sources(account_id, profile):
    click.echo("Fetching multiple DataSources")
    data_source_fetch_all(account_id, profile)


################################
### DataSets Commands
################################
@fetch.command()
def data_set():
    click.echo("Fetching a Data Set by ID")

@fetch.command()
@click.option('--account-id', required=True, help='The origin account id')
@click.option('--profile', default=None, help='Local AWS profile')
def data_sets(account_id, profile):
    click.echo("Fetching all DataSets")
    data_set_fetch_all(account_id, profile)


################################
### Dashboards Commands
################################
@fetch.command()
def dashboard():
    click.echo("Fetching Dashboard")

@fetch.command()
@click.option('--account-id', required=True, help='The origin account id')
@click.option('--profile', default=None, help='Local AWS profile')
def dashboards(account_id, profile):
    assert account_id is not None, "--account-id must be provided"
    click.echo(f"Fetching All Dashboards from account={account_id}")
    click.echo(f"AWS Profile={profile}")
    dashboard_fetch_all(account_id, profile)


################################
### Athena Workgroups Commands
################################
@fetch.command()
def workgroup():
    click.echo("Fetching workgroup")

@fetch.command()
@click.option('--account-id', required=True, help='The origin account id')
@click.option('--profile', default=None, help='Local AWS profile')
def workgroups(account_id, profile):
    assert account_id is not None, "--account-id must be provided"
    click.echo(f"Fetching All Athena Workgroups from account={account_id}")
    click.echo(f"AWS Profile={profile}")
    athena_fetch_workgroups(account_id, profile)


################################
### Athena Data Catalog Commands
################################
@fetch.command()
def data_catalog():
    click.echo("Fetching an Athena Data Catalog by name")

@fetch.command()
@click.option('--account-id', required=True, help='The origin account id')
@click.option('--profile', default=None, help='Local AWS profile')
def data_catalogs(account_id, profile):
    assert account_id is not None, "--account-id must be provided"
    click.echo(f"Fetching All Athena Data Catalog from account={account_id}")
    click.echo(f"AWS Profile={profile}")
    athena_fetch_data_catalogs(account_id, profile)


################################
### Glue Commands
################################
@fetch.command()
@click.option('--account-id', required=True, help='The origin account id')
@click.option('--profile', default=None, help='Local AWS profile')
def glue(account_id, profile):
    assert account_id is not None, "--account-id must be provided"
    click.echo(f"Fetching All Glue Databases from account={account_id}")
    click.echo(f"AWS Profile={profile}")

    glue_fetch_all(account_id, profile)