import click
from clicommands.data_source_commands import deploy_by_id as data_source_deploy_by_id
from clicommands.data_set_commands import deploy_by_id as data_set_deploy_by_id
from clicommands.analisys_commands import deploy_by_id as analysis_deploy_by_id
from clicommands.dashboard_commands import deploy_by_id as dashboard_deploy_by_id
from clicommands.athena_commands import deploy_by_id as athena_deploy_by_id
from clicommands.glue_commands import deploy_by_id as glue_deploy_by_id

@click.group()
def deploy():
    click.echo("Inside Deploy group")

################################
### Analyses Commands
################################
@deploy.command()
@click.option('--account-id', default="aaa-bbb-ccc-ddd", help='The AWS Account ID to deploy the Analysis clone')
@click.option('--region', default="us-east-1", help='AWS Region')
@click.option('--profile', default=None, help='AWS Profile')
@click.option('--parameters-path', default="analysis.local.txt", help='Parameter overrides file located on dir ./parameter-overrides')
@click.argument('template-file-path', type=click.Path(exists=True))
def analysis(account_id, parameters_path , template_file_path, region, profile):
    click.echo("Deploying Analysis")
    click.echo(f'Deploying to AWS AccountId = {account_id} ...')
    click.echo(f'Deploying analysis from CF template path = {template_file_path} ...')
    analysis_deploy_by_id(template_file_path, parameters_path, region, profile)

@deploy.command()
def analyses():
    click.echo("Deploying multiple Analysis")


################################
### Data Sources Commands
################################
@deploy.command()
@click.option('--account-id', default="aaa-bbb-ccc-ddd", help='The AWS Account ID to deploy the Data Source clone')
@click.option('--region', default="us-east-1", help='AWS Region')
@click.option('--profile', default=None, help='AWS Profile')
@click.option('--parameters-path', default="datasource.local.txt", help='Parameter overrides file located on dir ./parameter-overrides')
@click.argument('template-file-path', type=click.Path(exists=True))
def data_source(account_id, parameters_path , template_file_path, region, profile):
    click.echo(f'Deploying to AWS AccountId = {account_id} ...')
    click.echo(f'Deploying DataSource from CF template path = {template_file_path} ...')
    data_source_deploy_by_id(template_file_path, parameters_path, region, profile)

@deploy.command()
def data_sources():
    click.echo("Deploying multiple DataSources")


################################
### Data Set Commands
################################
@deploy.command()
@click.option('--account-id', default="aaa-bbb-ccc-ddd", help='The AWS Account ID to deploy the Data Set clone')
@click.option('--region', default="us-east-1", help='AWS Region')
@click.option('--profile', default=None, help='AWS Profile')
@click.option('--parameters-path', default="dataset.local.txt", help='Parameter overrides file located on dir ./parameter-overrides')
@click.argument('template-file-path', type=click.Path(exists=True))
def data_set(account_id, parameters_path , template_file_path, region, profile):
    click.echo("Deploying DataSets")
    click.echo(f'Deploying to AWS AccountId = {account_id} ...')
    click.echo(f'Deploying Data Set from CF template path = {template_file_path} ...')
    data_set_deploy_by_id(template_file_path, parameters_path, region, profile)

@deploy.command()
def data_sets():
    click.echo("Deploying multiple DataSets")


################################
### Dashboards Commands
################################
@deploy.command()
@click.option('--account-id', default="aaa-bbb-ccc-ddd", help='The AWS Account ID to deploy the dashboard clone')
@click.option('--region', default="us-east-1", help='AWS Region')
@click.option('--profile', default=None, help='AWS Profile')
@click.option('--parameters-path', default="dashboard.local.txt", help='Parameter overrides file located on dir ./parameter-overrides')
@click.argument('template-file-path', type=click.Path(exists=True))
def dashboard(account_id, parameters_path , template_file_path, region, profile):
    click.echo("Deploying Dashboard")
    click.echo(f'Deploying to AWS AccountId = {account_id} ...')
    click.echo(f'Deploying dashboard from CF template path = {template_file_path} ...')
    dashboard_deploy_by_id(template_file_path, parameters_path, region, profile)

@deploy.command()
def dashboards():
    click.echo("Deploying multiple Dashboards")

################################
### Athena Commands
################################
@deploy.command()
@click.option('--account-id', default="aaa-bbb-ccc-ddd", help='The AWS Account ID to deploy the Athena cloned resources')
@click.option('--region', default="us-east-1", help='AWS Region')
@click.option('--profile', default=None, help='AWS Profile')
@click.option('--parameters-path', default="athena.origin.txt", help='Parameter overrides file located on dir ./parameter-overrides')
@click.argument('template-file-path', type=click.Path(exists=True))
def athena(account_id, parameters_path, template_file_path, region, profile):
    click.echo(f'Deploying to AWS AccountId = {account_id} ...')
    click.echo(f'Deploying Athena resources from CF template path = {template_file_path} ...')
    athena_deploy_by_id(template_file_path, parameters_path, region, profile)

################################
### Glue Commands
################################
@deploy.command()
@click.option('--account-id', default="aaa-bbb-ccc-ddd", help='The AWS Account ID to deploy the Glue cloned resources')
@click.option('--region', default="us-east-1", help='AWS Region')
@click.option('--profile', default=None, help='AWS Profile')
@click.option('--parameters-path', default="glue.origin.txt", help='Parameter overrides file located on dir ./parameter-overrides')
@click.argument('template-file-path', type=click.Path(exists=True))
def glue(account_id, parameters_path, template_file_path, region, profile):
    click.echo(f'Deploying to AWS AccountId = {account_id} ...')
    click.echo(f'Deploying Glue resources from CF template path = {template_file_path} ...')
    glue_deploy_by_id(template_file_path, parameters_path, region, profile)