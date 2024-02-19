import os
import json
from qs.utils import mask_aws_account_id, cleanDirs, writeYaml, replace_slashes_with_double_underscores, extract_role_name_from_arn, list_resources

def fetchLambdaResources(session, account_id, region):
    print(f"Deleting old Lambda related resource files from {region}...")
    cleanDirs(f'./infra_base/{mask_aws_account_id(account_id)}/lambda/{region}')

    print("\nFetching Lambda Functions...")
    fetchLambdaFunctions(session, account_id, region)

    print("\nFetching Lambda Roles...")
    iam_client = session.client('iam', region)
    fetchLambdaRoles(iam_client, account_id, region)

    print("\nFetching Lambda Policies...")
    fetchLambdaPolicies(iam_client, account_id, region)
    fetchAllAuthDetails(iam_client, account_id, region)
    
    print("\nFetching Lambda Logs...")
    cwlogs_client = session.client('logs', region)
    fetchLambdaLogs(cwlogs_client, account_id, region)

    print("Fetch Completed.\n")

##################################################################
# Lambda Functions
def fetchLambdaFunctions(session, account_id, region):
    parent_dir = f'./infra_base/{mask_aws_account_id(account_id)}/lambda/{region}/functions'

    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, mode=0o777)

    lambda_client = session.client('lambda', region)
    list_functions = list_resources(
        action=lambda_client.list_functions,
        file_path=f'{parent_dir}/list-functions.yaml'
    )

    iam_client = session.client('iam', region)
    for function in list_functions['Functions']:

        # extraer lambda function
        lambda_description = lambda_client.get_function(FunctionName=function['FunctionName'])

        # extraer lambda policy
        lambda_policy_description = lambda_client.get_policy(FunctionName=function['FunctionName'])
        lambda_policy_description['Policy'] = json.loads(lambda_policy_description['Policy'])

        # extraer role
        lambda_role_name = extract_role_name_from_arn(function['Role'])
        lambda_role_description = iam_client.get_role(RoleName=lambda_role_name)

        # extraer role inline policies
        lambda_role_inline_policies = iam_client.list_role_policies(RoleName=lambda_role_name)
        lambda_role_inline_policies_descriptions = {}
        for inline_policy_name in lambda_role_inline_policies['PolicyNames']:
            description = iam_client.get_role_policy(RoleName=lambda_role_name, PolicyName=inline_policy_name)
            lambda_role_inline_policies_descriptions[inline_policy_name] = description

        # extraer role attached policies
        lambda_role_attached_policies = iam_client.list_attached_role_policies(RoleName=lambda_role_name)
        lambda_role_attached_policies_descriptions = {}
        for attached_policy in lambda_role_attached_policies['AttachedPolicies']:
            get_policy_description = iam_client.get_policy(PolicyArn=attached_policy['PolicyArn'])
            get_policy_version_description = iam_client.get_policy_version(PolicyArn=get_policy_description['Policy']['Arn'], VersionId=get_policy_description['Policy']['DefaultVersionId'])

            attached_policy_info = {'Policy': get_policy_description['Policy'], 'PolicyVersion': get_policy_version_description['PolicyVersion']}
            lambda_role_attached_policies_descriptions[attached_policy['PolicyName']] = attached_policy_info

        # crear yaml
        resource_description = {
            'DescribeLambda': lambda_description,
            'DescribeLambdaPolicy': lambda_policy_description,
            'DescribeLambdaRole': lambda_role_description,
            'DescribeLambdaRoleInlinePolicies': lambda_role_inline_policies_descriptions,
            'DescribeLambdaRoleAttachedPolicies': lambda_role_attached_policies_descriptions,
        }
        createLambdaFunctionDescriptionYaml(name=function['FunctionName'], description=resource_description, directory=parent_dir)

def createLambdaFunctionDescriptionYaml(name, description, directory):
    file_path = f'{directory}/{name}.yaml'
    writeYaml(description, file_path)
    return file_path
##################################################################


##################################################################
# IAM Roles
def fetchLambdaRoles(client, account_id, region):
    parent_dir = f'./infra_base/{mask_aws_account_id(account_id)}/lambda/{region}/iam/roles'

    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, mode=0o777)

    list_roles = list_resources(
        action=client.list_roles,
        file_path=f'{parent_dir}/list-roles.yaml'
    )

    for role in list_roles['Roles']:
        createLambdaRolesDescriptionYaml(name=role['RoleName'],description=role, directory=parent_dir)

def createLambdaRolesDescriptionYaml(name, description, directory):
    output = {'DescribeRole': description }
    file_path = f'{directory}/{name}.yaml'
    writeYaml(output, file_path)
    return file_path
##################################################################


##################################################################
# IAM Policies
def fetchLambdaPolicies(client, account_id, region):
    parent_dir = f'./infra_base/{mask_aws_account_id(account_id)}/lambda/{region}/iam/policies'

    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, mode=0o777)

    list_policies = list_resources(
        action=client.list_policies,
        file_path=f'{parent_dir}/list-policies.yaml'
    )

    for policy in list_policies['Policies']:
        createLambdaPolicyDescriptionYaml(name=policy['PolicyName'],description=policy, directory=parent_dir)

def createLambdaPolicyDescriptionYaml(name, description, directory):
    output = {'DescribePolicy': description }
    file_path = f'{directory}/{name}.yaml'
    writeYaml(output, file_path)
    return file_path
##################################################################


##################################################################
# CloudWatch Log Groups
def fetchLambdaLogs(client, account_id, region):
    parent_dir = f'./infra_base/{mask_aws_account_id(account_id)}/lambda/{region}/log-groups'

    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, mode=0o777)

    list_log_groups = list_resources(
        action=client.describe_log_groups,
        file_path=f'{parent_dir}/list-log-groups.yaml'
    )

    for log_group in list_log_groups['logGroups']:
        createLambdaLogsDescriptionYaml(name=replace_slashes_with_double_underscores(log_group['logGroupName']), description=log_group, directory=parent_dir)

def createLambdaLogsDescriptionYaml(name, description, directory):
    output = {'DescribeLogGroup': description }
    file_path = f'{directory}/{name}.yaml'
    writeYaml(output, file_path)
    return file_path
##################################################################


##################################################################
# IAM All Auth Details
def fetchAllAuthDetails(client, account_id, region):
    parent_dir = f'./infra_base/{mask_aws_account_id(account_id)}/lambda/{region}/iam'

    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, mode=0o777)
        
    auth_details_dict  = {}

    paginator = client.get_paginator('get_account_authorization_details')
    response_iterator = paginator.paginate()

    for response in response_iterator:
        for key, value in response.items():
            if isinstance(value, list):
                if key not in auth_details_dict:
                    auth_details_dict[key] = []
                auth_details_dict[key].extend(value)
        if 'Marker' not in response:
            break
        else:
            paginator = client.get_paginator('get_account_authorization_details')
            response_iterator = paginator.paginate(Marker=response['Marker'])
    
    writeYaml(auth_details_dict, f'{parent_dir}/all.yaml')
