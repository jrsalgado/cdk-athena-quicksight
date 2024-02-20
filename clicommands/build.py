import click
from clicommands.data_source_commands import build_by_id as data_source_build_by_id
from clicommands.data_set_commands import build_by_id as data_set_build_by_id
from clicommands.analisys_commands import build_by_id as analysis_build_by_id
from clicommands.dashboard_commands import build_by_id as dashboard_build_by_id
from clicommands.athena_commands import build as athena_build
from clicommands.glue_commands import build_by_id as glue_database_build_by_id

@click.group()
def build():
    pass

################################
### Analyses Commands
################################
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


################################
### Data Sources Commands
################################
@build.command()
@click.option('--account-id', required=True, help='The origin account id')
@click.argument('data-source-id', required=True)
def data_source(account_id, data_source_id):
    assert account_id is not None, "--account-id must be provided"
    assert data_source_id is not None, "data_source_id argument must be provided" 
    click.echo("Building DataSources")

    click.echo(f"Building Data Source from Account={account_id}")
    click.echo(f"Data Source Id={data_source_id}")
    data_source_build_by_id(account_id,data_source_id)


################################
### Data Set Commands
################################
@build.command()
@click.option('--account-id', required=True, help='The origin account id')
@click.option('--data-source-id', required=False, help='Id of an already created data source')
@click.option('--create-dependencies', default=False, help='Id of an already created data source')
@click.argument('data-set-id', required=True)
def data_set(account_id, data_set_id, data_source_id, create_dependencies):
    assert account_id is not None, "--account-id must be provided"
    assert data_set_id is not None, "data-set-id argument must be provided" 
    
    click.echo(f"Building Data Set from Account={account_id}")
    click.echo(f"Building Data Set Id={data_set_id}")
    click.echo(f"Data Source Id={data_source_id}")
    click.echo(f"Creating dependencies too [data-source, data-set]= {create_dependencies}")
    data_set_build_by_id(account_id,data_set_id,data_source_id,create_dependencies)


################################
### Dashboards Commands
################################
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


################################
### Athena Commands
################################
@build.command()
@click.option('--account-id', required=True, help='The origin account id')
@click.option('--workgroup-name', default="base", help='The name of the existing Athena Workgroup to be cloned')
@click.option('--catalog-name', default="base", help='The name of the existing Athena Data Catalog to be cloned')
@click.option('--same-env', is_flag=True) # Boolean option, if present adds hash sufix to resource names/ids
def athena(account_id, workgroup_name, catalog_name, same_env):
    assert account_id is not None, "--account-id must be provided"

    click.echo(f"Building Athena template from Account={account_id}")
    click.echo(f"Building Workgroup = {workgroup_name}")
    click.echo(f"Building Athena Data Catalog = {catalog_name}")
    
    athena_build(account_id, workgroup_name, catalog_name, same_env)


################################
### Glue Commands
################################
@build.command()
@click.option('--account-id', required=True, help='The origin account id')
@click.option('--same-env', is_flag=True)
@click.argument('database-name', required=True)
def glue(account_id, database_name, same_env):
    assert account_id is not None, "--account-id must be provided"
    assert database_name is not None, "database-name must be provided"
    
    click.echo(f"Building Glue Database template from Account={account_id}")
    click.echo(f"Building Database = {database_name}")
    
    glue_database_build_by_id(account_id, database_name, same_env)