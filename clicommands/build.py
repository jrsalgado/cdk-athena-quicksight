import click
from clicommands.analisys_comands import build_by_id as analysis_build_by_id
from clicommands.dashboard_comands import build_by_id as dashboard_build_by_id

@click.group()
def build():
    click.echo("Inside build group")

# Analysis Commands
@build.command()
@click.option('--account-id', required=True, help='The origin account id')
@click.option('--data-set-id', required=False, help='Id of an already created data set')
@click.option('--data-source-id', required=False, help='Id of an already created data source')
@click.option('--create-dependencies', default=False, help='Id of an already created data source')
@click.argument('analysis-id', required=True)
def analysis(account_id, analysis_id, data_set_id, data_source_id, create_dependencies ):
    assert account_id is not None, "--account-id must be provided"
    assert analysis_id is not None, "analysis-id argument must be provided"
    
    click.echo(f"Building Analysis from Account={account_id}")
    click.echo(f"Building Analysis Id={analysis_id}")
    click.echo(f"Data Set Id={data_set_id}")
    click.echo(f"Data Source Id={data_source_id}")
    click.echo(f"Creating dependencies too [data-source, data-set]= {create_dependencies}")
    analysis_build_by_id(account_id, analysis_id, create_dependencies, data_source_id, data_set_id)
    pass


# DataSources Commands
@build.command()
def data_source():
    click.echo("Building DataSources")


# DataSet Commands
@build.command()
def data_set():
    click.echo("Building DataSets")


# Dashboards Commands
@build.command()
@click.option('--account-id', required=True, help='The origin account id')
@click.option('--data-set-id', required=False, help='Id of an already created data set')
@click.option('--data-source-id', required=False, help='Id of an already created data source')
@click.option('--create-dependencies', default=False, help='Id of an already created data source')
@click.argument('dashboard-id', required=True)
def dashboard(account_id, dashboard_id, data_set_id, data_source_id, create_dependencies ):
    assert account_id is not None, "--account-id must be provided"
    assert dashboard_id is not None, "dashboard-id argument must be provided" 
    
    click.echo(f"Building Dashboard from Account={account_id}")
    click.echo(f"Building Dashboard Id={dashboard_id}")
    click.echo(f"Data Set Id={data_set_id}")
    click.echo(f"Data Source Id={data_source_id}")
    click.echo(f"Creating dependencies too [data-source, data-set]= {create_dependencies}")
    dashboard_build_by_id(account_id, dashboard_id, create_dependencies, data_source_id, data_set_id)
    pass
