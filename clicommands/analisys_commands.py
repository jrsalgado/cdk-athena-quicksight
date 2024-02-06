import boto3
import os
import subprocess
from infra_base.qs_fetch import fetchQSAnalysesResources
from qs.utils import mask_aws_account_id, updateTemplateAfterSynth, deploy_stack

def fetch_all(account_id, profile=None, region_name='us-east-1'):
    print("Fetching All Analysis from commands...")
    session = boto3.Session(profile_name=profile)
    os.environ['ORIGIN_AWS_ACCOUNT_ID']= account_id
    quicksight_client = session.client('quicksight', region_name)
    fetchQSAnalysesResources(quicksight_client, account_id)
    pass

def build_by_id(origin_account_id:str, analysis_id:str, create_dependencies:bool= True, data_source_id= None, data_set_id= None ):
    """
    Create a CloudFormation template from an already created quicksight analysis
    
    :param origin_account_id: Origin AWS Account ID of the Analysis
    :param analysis_id: Origin Analysis Id
    :pass:
    """
    os.environ['ORIGIN_IDS_RESOLVE'] = str(create_dependencies)
    if data_set_id is not None:
        os.environ['ORIGIN_DATASET_ID'] = data_set_id
    if data_source_id is not None:
        os.environ['ORIGIN_DATASOURCE_ID'] = data_source_id
    os.environ['ORIGIN_AWS_ACCOUNT_ID'] = origin_account_id
    os.environ['ORIGIN_ANALYSIS_ID'] = analysis_id

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
        "analysis_params=parameters/just-analysis.yaml",
    ]

    masked_origin_aws_account_id = mask_aws_account_id(origin_account_id)
    template_dir= f"./CFTemplates/{masked_origin_aws_account_id}/analyses"
    template_path= f"./CFTemplates/{masked_origin_aws_account_id}/analyses/{analysis_id}.yaml"

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
    deploy_stack(template_file_path, parameters_path, aws_region, aws_profile, stack_name_prefix='analysis')