import boto3
import os
import subprocess
from infra_base.qs_fetch import fetchQSDataSourcesResources
from qs.utils import mask_aws_account_id, updateTemplateAfterSynth, deploy_stack

def fetch_all(account_id, profile=None, region_name='us-east-1'):
    """
    Fetch and store the description of all the exisiting Quicksight Data Sources
    
    :param account_id: Origin AWS Account ID of the Dashboard
    :param profile: Local AWS Profile
    :pass:
    """
    print("Fetching all existing Data Sources...")
    session = boto3.Session(profile_name=profile)
    os.environ['ORIGIN_AWS_ACCOUNT_ID']= account_id
    quicksight_client = session.client('quicksight', region_name)
    fetchQSDataSourcesResources(quicksight_client, account_id)
    pass



def build_by_id(origin_account_id:str, data_source_id:str):
    """
    Create a CloudFormation template from an already created Quicksight Data Source
    
    :param origin_account_id: Origin AWS Account ID of the Data Set
    :param data_source_id: Origin Data Set Id
    :pass:
    """
    os.environ['ORIGIN_AWS_ACCOUNT_ID'] = origin_account_id
    os.environ['ORIGIN_DATASOURCE_ID'] = data_source_id

    cdk_command = [
        "cdk", 
        "synth", 
        "--context", 
        "general_params=parameters/general.yaml",
        "--context",
        "params=parameters/just-data-source.yaml"
    ]

    masked_origin_aws_account_id = mask_aws_account_id(origin_account_id)
    template_dir= f"./CFTemplates/{masked_origin_aws_account_id}/data-source"
    template_path= f"./CFTemplates/{masked_origin_aws_account_id}/data-source/{data_source_id}.yaml"

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
            updateTemplateAfterSynth(template_path)
    except subprocess.CalledProcessError as e:
        print(f"Error running CDK synth: {e}")
    pass

def deploy_by_id(template_file_path, parameters_path, aws_region, aws_profile):
    deploy_stack(template_file_path, parameters_path, aws_region, aws_profile, stack_name_prefix='datasource')