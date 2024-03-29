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
aws_profile = os.getenv('AWS_PROFILE')

session = boto3.Session(profile_name=aws_profile)
def initSession():
    if aws_access_key_id:
        quicksight_client = session.client(
            'quicksight',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )

    elif aws_role_to_assume:
        sts_client = session.client('sts')

        response = sts_client.assume_role(
            RoleArn=aws_role_to_assume,
            RoleSessionName="QuickSightRoleSession"
        )
        credentials = response['Credentials']

        quicksight_client = session.client(
            'quicksight',
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
            region_name=aws_region,
        )
    else:
        quicksight_client = session.client(
            'quicksight',
            region_name=aws_region
        )

    return quicksight_client

if __name__ == '__main__':
    quicksight_client= initSession()
    fetchQSAllResources(quicksight_client, aws_account_id)