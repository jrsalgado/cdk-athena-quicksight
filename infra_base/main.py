import os
import boto3
from dotenv import load_dotenv
from qs_fetch import fetchQSAllResources

load_dotenv()

aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')
aws_account_id = os.getenv('AWS_ACCOUNT_ID')
aws_role_to_assume = os.getenv('AWS_ROLE_TO_ASSUME')

if aws_role_to_assume:
    sts_client = boto3.client('sts',
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key,
                              region_name=aws_region)

    assumed_role_object = sts_client.assume_role(
        RoleArn=aws_role_to_assume,
        RoleSessionName="AssumeRoleSession1"
    )
    credentials = assumed_role_object['Credentials']

    quicksight_client = boto3.client(
        'quicksight',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
        aws_region=credentials['SessionToken'],
    )
else:
    quicksight_client = boto3.client(
        'quicksight',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )

if __name__ == '__main__':
    fetchQSAllResources(quicksight_client, aws_account_id)
