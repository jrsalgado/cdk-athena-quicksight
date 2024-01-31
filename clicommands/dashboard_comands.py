import boto3
import os
import subprocess
#from infra_base.qs_fetch import fetchQSAnalysesResources
from qs.utils import mask_aws_account_id, updateTemplateAfterSynth

def build_by_id(origin_account_id:str, dashboard_id:str, create_dependencies:bool, data_source_id= None, data_set_id= None ):
    """
    Create a CloudFormation template from an already created quicksight dashboard
    
    :param origin_account_id: Origin AWS Account ID of the Dashboard
    :param analysis_id: Origin Dashboard Id
    :pass:
    """
    print(create_dependencies)
    assert create_dependencies is True or (data_source_id is not None and data_set_id is not None), "Either create_dependencies must be explicitly True or both data_source_id and data_set_id must be set to non-None values."

    os.environ['ORIGIN_AWS_ACCOUNT_ID'] = origin_account_id
    os.environ['ORIGIN_DASHBOARD_ID'] = dashboard_id

    if create_dependencies is True:
        os.environ['ORIGIN_IDS_RESOLVE'] = str(create_dependencies)
    if data_set_id is not None:
        os.environ['ORIGIN_DATASET_ID'] = data_set_id
    if data_source_id is not None:
        os.environ['ORIGIN_DATASOURCE_ID'] = data_source_id

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

    masked_origin_aws_account_id = mask_aws_account_id(origin_account_id)
    template_dir= f"./CFTemplates/{masked_origin_aws_account_id}/dashboards"
    template_path= f"./CFTemplates/{masked_origin_aws_account_id}/dashboards/{dashboard_id}.yaml"

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

