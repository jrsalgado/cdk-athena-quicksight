#!.venv/bin/python
import click
import subprocess
import os
import boto3
import sys
from qs.utils import readFromOriginResourceFile, mask_aws_account_id, generate_id, updateTemplateAfterSynth
from infra_base.qs_fetch import fetchQSAllResources

@click.group()
def cli():
    pass

@cli.command()
@click.option('--account-id', default="aaa-bbb-ccc-ddd", help='The origin account id')
@click.option('--profile', default=None, help='AWS CLI Profile')
def fetchAllQuicksightResources(account_id, profile):
    os.environ['ORIGIN_AWS_ACCOUNT_ID']= account_id
    click.echo(f'Fetch all resources from AWS Account = {account_id} ...')
    session = boto3.Session(profile_name=profile)
    quicksight_client = session.client(
        'quicksight',
        region_name='us-east-1'
    )
    fetchQSAllResources(quicksight_client, account_id)

@cli.command()
@click.option('--account-id', default="aaa-bbb-ccc-ddd", help='The origin account id')
@click.argument('dashboardid')
def cloneFromDashboardId(account_id, dashboardid):
    os.environ['ORIGIN_AWS_ACCOUNT_ID']= account_id
    click.echo(f'Cloning from AWS AccountId = {account_id} ...')
    click.echo(f'Creating template from DashboardId= {dashboardid} ...')
    cdk_synth(account_id, dashboardid)

@cli.command()
@click.option('--account-id', default="aaa-bbb-ccc-ddd", help='The origin account id')
def cloneAllDashboards(account_id):
    os.environ['ORIGIN_AWS_ACCOUNT_ID']= account_id
    click.echo(f'Cloning from AWS AccountId = {account_id} ...')
    # for each dashboard on the --list-dashboard file
    camelOriginalResource, _ = readFromOriginResourceFile('dashboards', 'list-dashboards', mask_aws_account_id(account_id))
    for dashboard in camelOriginalResource['dashboardSummaryList']:
        cdk_synth(account_id, dashboard['dashboardId'])


@cli.command()
@click.option('--account-id', default="aaa-bbb-ccc-ddd", help='The AWS Account ID to deploy the dasboard clone')
@click.option('--region', default="us-east-1", help='AWS Region')
@click.option('--profile', default=None, help='AWS Profile')
@click.option('--parameters-path', default="local.txt", help='Parameter overrides file located on dir ./parameter-overrides')
@click.argument('template-file-path', type=click.Path(exists=True))
def deployDashboard(account_id, parameters_path , template_file_path, region, profile):
    click.echo(f'Cloning from AWS AccountId = {account_id} ...')
    click.echo(f'Cloning dashboard from CF template path = {template_file_path} ...')
    cfDeployDashboard(template_file_path, parameters_path, account_id, region, profile)

### TEMPORARY SOLUTION
### TODO: move to own library
def cdk_synth(originAccountId:str , dashboardId: str):
    # Define the CDK command to deploy your stack
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
    masked_origin_aws_account_id = mask_aws_account_id(originAccountId)
    template_dir= f"./CFTemplates/{masked_origin_aws_account_id}/dashboards"
    template_path= f"./CFTemplates/{masked_origin_aws_account_id}/dashboards/{dashboardId}.yaml"
    try:
        subprocess.run([
                'mkdir',
                '-p',
                template_dir,
            ],
            check=True,)
        # Run the CDK deploy command
        with open(template_path, "w") as output_file:
            subprocess.run(cdk_command, env= os.environ , check=True, stdout=output_file)
    except subprocess.CalledProcessError as e:
        print(f"Error running CDK deploy: {e}")
    updateTemplateAfterSynth(template_path)

    pass


def cfDeployDashboard(template_file_path, parameters_path, account_id, aws_region, aws_profile):
    # Load parameter overrides from file
    parameter_overrides = []
    parameter_file_path = f'parameter-overrides/{parameters_path}'
    with open(parameter_file_path, 'r') as file:
        for line in file:
            print(line)
            if not line.strip() == '':
                key, value = line.strip().split('=')
                parameter_overrides.append({'ParameterKey': key, 'ParameterValue': value})

    # Deploy CloudFormation stack using boto3
    session = boto3.Session(profile_name=aws_profile)
    cloudformation_client = session.client('cloudformation',
                                        region_name=aws_region,
                                        )
    stack_name = f'dashboard-{generate_id(8)}'

    response = cloudformation_client.create_stack(
        StackName=stack_name,
        TemplateBody=open(template_file_path, 'r').read(),
        Parameters=parameter_overrides,
    )

    print(f"Stack creation initiated. Stack ID: {response['StackId']}")

    # Wait for the stack creation to complete
    waiter = cloudformation_client.get_waiter('stack_create_complete')
    waiter.wait(StackName=stack_name)
    print("Stack creation complete.")

    # Describe the stack for more information
    stack_info = cloudformation_client.describe_stacks(StackName=stack_name)
    return stack_info['Stacks'][0]


if __name__ == '__main__':
    cli()

