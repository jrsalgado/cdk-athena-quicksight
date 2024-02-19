import boto3
import os
import subprocess
from infra_base.lambda_fetch import fetchLambdaResources
from qs.utils import mask_aws_account_id, updateTemplateAfterSynth, deploy_stack, update_stack

def fetch_all(account_id, region, profile=None):
    """
    Fetch and store the description of all the exisiting Lambda functions and related resources
    
    :param account_id: Origin AWS Account ID
    :param profile: Local AWS Profile
    :param region: Origin AWS Region
    """
    os.environ['ORIGIN_AWS_ACCOUNT_ID']= account_id

    session = boto3.Session(profile_name=profile)
    
    fetchLambdaResources(session, account_id, region)
    pass
