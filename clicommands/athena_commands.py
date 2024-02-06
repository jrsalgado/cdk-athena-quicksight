import boto3
import os
import subprocess
from infra_base.athena_fetch import fetchAthenaResources, fetchAthenaWorkgroups, fetchAthenaDataCatalogs

from qs.utils import mask_aws_account_id, updateTemplateAfterSynth, deploy_stack

def fetch_all(account_id, profile=None, region_name='us-east-1'):
    """
    Fetch and store the description of all the exisiting Athena Workgroups and Data Catalogs
    
    :param account_id: Origin AWS Account ID
    :param profile: Local AWS Profile
    :pass:
    """
    session = boto3.Session(profile_name=profile)
    os.environ['ORIGIN_AWS_ACCOUNT_ID']= account_id

    athena_client = session.client('athena', region_name)
    fetchAthenaResources(athena_client, account_id)


def fetch_workgroups(account_id, profile=None, region_name='us-east-1'):
    """
    Fetch and store the description of all the exisiting Athena Workgroups
    
    :param account_id: Origin AWS Account ID
    :param profile: Local AWS Profile
    :pass:
    """
    print("Fetching All Athena Workgroups...")
    session = boto3.Session(profile_name=profile)
    os.environ['ORIGIN_AWS_ACCOUNT_ID']= account_id

    athena_client = session.client('athena', region_name)
    fetchAthenaWorkgroups(athena_client, account_id)
    pass

def fetch_data_catalogs(account_id, profile=None, region_name='us-east-1'):
    """
    Fetch and store the description of all the exisiting Athena Data Catalogs
    
    :param account_id: Origin AWS Account ID
    :param profile: Local AWS Profile
    :pass:
    """
    print("Fetching All Athena Data Catalogs...")
    session = boto3.Session(profile_name=profile)
    os.environ['ORIGIN_AWS_ACCOUNT_ID']= account_id

    athena_client = session.client('athena', region_name)
    fetchAthenaDataCatalogs(athena_client, account_id)
    pass

def build(account_id, workgroup_name, catalog_name):
    os.environ['SYNTH_ATHENA'] = 'True'

    os.environ['ORIGIN_AWS_ACCOUNT_ID']= account_id
    os.environ['ORIGIN_WORKGROUP_NAME'] = workgroup_name
    os.environ['ORIGIN_CATALOG_NAME'] = catalog_name

    cdk_command = [
        "cdk", 
        "synth", 
        "--context", 
        "general_params=parameters/general.yaml",
        "--context", 
        "athena_params=parameters/just-athena.yaml",
    ]

    masked_origin_aws_account_id = mask_aws_account_id(account_id)
    template_dir= f"./CFTemplates/{masked_origin_aws_account_id}/athena/"
    template_path= f"./CFTemplates/{masked_origin_aws_account_id}/athena/athena_template.yaml"

    try:
        subprocess.run([
                'mkdir',
                '-p',
                template_dir,
            ],
            check=True,)
        
        with open(template_path, "w") as output_file:
            subprocess.run(cdk_command, env= os.environ , check=True, stdout=output_file)
            updateTemplateAfterSynth(template_path)
    except subprocess.CalledProcessError as e:
        print(f"Error running CDK deploy: {e}")

    
    pass

def deploy_by_id(template_file_path, parameters_path, aws_region, aws_profile):
    deploy_stack(template_file_path, parameters_path, aws_region, aws_profile, stack_name_prefix='athena')