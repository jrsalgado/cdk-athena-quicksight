import click
import subprocess
import os
from qs.utils import readFromOriginResourceFile

@click.group()
def cli():
    pass

@cli.command()
@click.option('--account-id', default="aaa-bbb-ccc-ddd", help='The origin account id')
@click.argument('dashboardid')
def cloneFromDashboardId(account_id, dashboardid):
    click.echo(f'Cloning from AWS AccountId = {account_id} ...')
    click.echo(f'Creating template from DashboardId= {dashboardid} ...')
    cdk_synth(account_id, dashboardid)

@cli.command()
@click.option('--account-id', default="aaa-bbb-ccc-ddd", help='The origin account id')
def cloneAllDashboards(account_id):
    click.echo(f'Cloning from AWS AccountId = {account_id} ...')
    # for each dashboard on the --list-dashboard file
    camelOriginalResource, _ = readFromOriginResourceFile('dashboards', 'list-dashboards', account_id)
    print(camelOriginalResource['dashboardSummaryList'])
    for dashboard in camelOriginalResource['dashboardSummaryList']:
        cdk_synth(account_id, dashboard['dashboardId'])

### TEMPORARY SOLUTION
### TODO: move to own library
def cdk_synth(originAccountId:str , dashboardId: str):
    # Define the CDK command to deploy your stack
    os.environ['ORIGIN_AWS_ACCOUNT_ID']= originAccountId
    os.environ['ORIGIN_DASHBOARD_ID']= dashboardId
    os.environ['ORIGIN_IDS_RESOLVE']= "True"

    cdk_command = [
        "cdk", 
        "synth", 
        "--context", 
        "general_params=parameters/general.yaml",
        "--context",
        "params=parameters/just-data-source.yaml",
        "--context",
        "dataset_params=parameters/just-data-set.yaml",
        "--context",
        "dashboard_params=parameters/just-dashboard.yaml",
    ]
    template_path= f"./CFTemplates/{originAccountId}/dashboard/{dashboardId}.yaml"
    try:
        # Run the CDK deploy command
        with open(template_path, "w") as output_file:
            subprocess.run(cdk_command, env= os.environ , check=True, stdout=output_file)
    except subprocess.CalledProcessError as e:
        print(f"Error running CDK deploy: {e}")

if __name__ == '__main__':
    cli()

