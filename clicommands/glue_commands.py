import boto3
import os
import subprocess
from infra_base.glue_fetch import fetchGlueResources
from qs.utils import mask_aws_account_id, updateTemplateAfterSynth, deploy_stack

def fetch_all(account_id, profile=None, region_name='us-east-1'):
    """
    Fetch and store the description of all the exisiting Glue Databases
    
    :param account_id: Origin AWS Account ID
    :param profile: Local AWS Profile
    :param region_name: Origin AWS Region
    """
    os.environ['ORIGIN_AWS_ACCOUNT_ID']= account_id

    session = boto3.Session(profile_name=profile)
    glue_client = session.client('glue', region_name)
    
    fetchGlueResources(glue_client, account_id)
    pass

def build_by_id(account_id, database_name):
    os.environ['ORIGIN_AWS_ACCOUNT_ID']= account_id
    os.environ['ORIGIN_DATABASE_NAME'] = database_name

    cdk_command = [
        "cdk", 
        "synth", 
        "--context", 
        "general_params=parameters/general.yaml",
        "--context", 
        "glue_params=parameters/just-glue.yaml",
    ]

    masked_origin_aws_account_id = mask_aws_account_id(account_id)
    template_dir= f"./CFTemplates/{masked_origin_aws_account_id}/glue/"
    template_path= f"./CFTemplates/{masked_origin_aws_account_id}/glue/{database_name}.yaml"

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
    deploy_stack(template_file_path, parameters_path, aws_region, aws_profile, stack_name_prefix='glue')