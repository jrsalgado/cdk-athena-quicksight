import random
import string
import re
import yaml
from yaml.loader import SafeLoader
import os
import boto3
import shutil
import subprocess

def pascal_to_camel(key):
    if key == "KPIVisual":
        return "kpiVisual"
    elif key == "KPIOptions":
        return "kpiOptions"
    else:
        return key[0].lower() + key[1:]

def convert_keys_to_camel_case(d):
    if isinstance(d, dict):
        return {pascal_to_camel(key): convert_keys_to_camel_case(value) for key, value in d.items()}
    elif isinstance(d, list):
        return [convert_keys_to_camel_case(item) for item in d]
    else:
        return d

def generate_id(n=64):
    characters = string.ascii_letters + string.digits
    alphanumeric_id = ''.join(random.choice(characters) for _ in range(n))
    return alphanumeric_id

def extract_id_from_arn(arn):
    # Define a regular expression pattern to extract the ID
    pattern = r'arn:aws:quicksight:.*:.*/(.*)'

    # Use re.match to find the pattern at the beginning of the string
    match = re.match(pattern, arn)

    # Check if there is a match and extract the ID
    if match:
        return match.group(1)
    else:
        return None  # Return None if no match is found

def readFromOriginResourceFile(resourceType, originId, originAWSAccountId):
    # Copy from original resources
    originalResourcePath=f"infra_base/{originAWSAccountId}/{resourceType}/{originId}.yaml"

    with open(originalResourcePath) as f:
        originalResource = yaml.load(f, Loader=SafeLoader)
    camelOriginalResource = convert_keys_to_camel_case(originalResource)
    snakeOriginalResource =  convert_keys_to_snake_case(originalResource)

    return camelOriginalResource, snakeOriginalResource

def pascal_to_snake(key):
    result = [key[0].lower()]
    for char in key[1:]:
        if char.isupper():
            result.append('_')
            result.append(char.lower())
        else:
            result.append(char)
    return ''.join(result)

def convert_keys_to_snake_case(d):
    if isinstance(d, dict):
        return {pascal_to_snake(key): convert_keys_to_snake_case(value) for key, value in d.items()}
    elif isinstance(d, list):
        return [convert_keys_to_snake_case(item) for item in d]
    else:
        return d


def find_all_values_iterative(obj, keySearch):
    stack = [obj]
    founds= []
    while stack:
        current = stack.pop()

        if isinstance(current, list):
            # If the current element is a list, extend the stack with its elements
            stack.extend(current)
        elif isinstance(current, dict):
            # If the current element is a dictionary, update keys and values
            for key, value in current.items():
                if key == keySearch:
                    founds.append(current[key])
                else:
                    stack.append(value)

    return founds


def mask_account_ids(obj):
    aws_account_id_pattern = re.compile(r'\b\d{12}\b')
    mask_value= mask_aws_account_id(os.environ['ORIGIN_AWS_ACCOUNT_ID']) if os.environ['ORIGIN_AWS_ACCOUNT_ID'] else 'MASKED_ACCOUNT_ID'
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (str, int)):
                # Replace AWS account IDs in strings and integers
                obj[key] = aws_account_id_pattern.sub(mask_value, str(value))
            elif isinstance(value, (dict, list)):
                # Recursively mask AWS account IDs in nested structures
                mask_account_ids(value)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if isinstance(item, (str, int)):
                # Replace AWS account IDs in strings and integers
                obj[i] = aws_account_id_pattern.sub(mask_value, str(item))
            elif isinstance(item, (dict, list)):
                # Recursively mask AWS account IDs in nested structures
                mask_account_ids(item)
    return obj

def convert_element_values_to_int(layout_data):
    for layout_config in layout_data:
        configuration = layout_config.get('configuration', {})

        for layout_type, layout_details in configuration.items():
            elements = layout_details.get('elements', [])
            for element in elements:
                if 'columnIndex' in element:
                    element['columnIndex'] = int(element.get('columnIndex', 0))
                if 'columnSpan' in element:
                    element['columnSpan'] = int(element.get('columnSpan', 0))
                if 'rowIndex' in element:
                    element['rowIndex'] = int(element.get('rowIndex', 0))
                if 'rowSpan' in element:
                    element['rowSpan'] = int(element.get('rowSpan', 0))

    return layout_data

def mask_aws_account_id(account_id):
    """
    Replace the first 8 characters of an AWS account ID with "Xs".

    Parameters:
    - account_id (str): The AWS account ID.

    Returns:
    - str: The masked AWS account ID.
    """
    if len(account_id) >= 8:
        return "X" * 8 + account_id[8:]
    else:
        # Handle the case where the account ID is less than 8 characters
        return account_id

def updateTemplateAfterSynth(template_path: str):
    # Read YAML file
    with open(template_path) as f:
        templateOutput = yaml.load(f, Loader=SafeLoader)

    # Delete BootstrapVersion from parameters
    if 'BootstrapVersion' in templateOutput['Parameters']:
        del templateOutput['Parameters']['BootstrapVersion']

    # Delete CDKMetadata from resources
    if 'CDKMetadata' in templateOutput['Resources']:
        del templateOutput['Resources']['CDKMetadata']

    # Delete Rules section
    if 'Rules' in templateOutput:
        del templateOutput['Rules']

    # Delete conditions
    if 'Conditions' in templateOutput:
        del templateOutput['Conditions']

    # Write updated dictionary to the same YAML file
    with open(template_path, 'w') as yaml_file:
        yaml.dump(templateOutput, yaml_file, default_flow_style=False)

def deploy_stack(template_file_path, parameters_path, aws_region, aws_profile, stack_name_prefix='stack'):
    parameter_overrides = []
    parameter_file_path = f'parameter-overrides/{parameters_path}'
    with open(parameter_file_path, 'r') as file:
        for line in file:
            print(line)
            if not line.strip() == '':
                key, value = line.strip().split('=')
                parameter_overrides.append({'ParameterKey': key, 'ParameterValue': value})

    session = boto3.Session(profile_name=aws_profile)
    cloudformation_client = session.client('cloudformation', region_name=aws_region)
    stack_name = f'{stack_name_prefix}-{generate_id(8)}'

    response = cloudformation_client.create_stack(
        StackName=stack_name,
        TemplateBody=open(template_file_path, 'r').read(),
        Parameters=parameter_overrides,
    )

    print(f"Stack creation initiated. Stack ID: {response['StackId']}")

    waiter = cloudformation_client.get_waiter('stack_create_complete')
    waiter.wait(StackName=stack_name)
    print("Stack creation complete.")

    stack_info = cloudformation_client.describe_stacks(StackName=stack_name)
    return stack_info['Stacks'][0]

def cleanDirs(paths):
    """
    Deletes a directory and all its contents. If the directory does not exist, nothing is done.

    Parameters:
    - paths (str or list): The path or list of paths to the directories to be cleaned.

    Returns:
    - None
    """
    if isinstance(paths, str):
        paths = [paths]

    for path in paths:
        if not os.path.exists(path):
            print(f"Nothing to delete at '{path}'.")
            continue
        try:
            shutil.rmtree(path)
            print(f"Directory '{path}' and its contents successfully deleted.")
        except OSError as e:
            print(f"Error removing directory '{path}': {e}")

def convertToYaml(data: dict):
    yaml_data = yaml.dump(data, default_flow_style=False)
    return yaml_data

def writeYaml(dataObj: dict, path: str):
    maskedData = mask_account_ids(dataObj)
    dataYaml = convertToYaml(maskedData)
    with open(path, 'w') as file:
        file.write(dataYaml)

def read_parameters(params_file_name):
    parameter_overrides = []
    parameter_file_path = f'parameter-overrides/{params_file_name}'
    with open(parameter_file_path, 'r') as file:
        for line in file:
            print(line)
            if not line.strip() == '':
                key, value = line.strip().split('=')
                parameter_overrides.append({'ParameterKey': key, 'ParameterValue': value})
    return parameter_overrides

def update_stack(stack_name, template_body, template_url, parameters_path, region, profile):
    parameters = read_parameters(parameters_path)

    session = boto3.Session(profile_name=profile)
    cloudformation_client = session.client('cloudformation', region_name=region)
    change_set_name = f'update-{generate_id(8)}'

    change_set_args = {
        'StackName': stack_name,
        'ChangeSetName': change_set_name,
        'Parameters': parameters,
    }

    if template_body:
        change_set_args['TemplateBody'] = open(template_body, 'r').read()
    elif template_url:
        change_set_args['TemplateURL'] = template_url

    create_response = cloudformation_client.create_change_set(**change_set_args)

    print(f"Change set creation initiated. Stack ID:{create_response['StackId']}")

    create_waiter = cloudformation_client.get_waiter('change_set_create_complete')
    create_waiter.wait(
        ChangeSetName=change_set_name,
        StackName=stack_name
    )
    print("Change set creation complete.")

    print('Executing change set')
    execute_response = cloudformation_client.execute_change_set(
        ChangeSetName=change_set_name,
        StackName=stack_name
    )

def replace_slashes_with_double_underscores(string):
    if '/' not in string:
        return string
    else:
        return string.replace('/', '__')

def extract_role_name_from_arn(input_string):
    pattern = r"\/([^\/]+)$"  # Regex pattern to match the role name at the end of the string
    match = re.search(pattern, input_string)
    if match:
        return match.group(1)
    else:
        return None

def zip_directory(directory, zip_filename):  
    if os.path.exists(directory):
        try:
            subprocess.run([
                    'zip',
                    '-r',
                    zip_filename,
                    directory
                ],check=True,)
        except subprocess.CalledProcessError as e:
            print(f"Error creating a zip file of infra_base content: {e}")

        print(f"Contents of {directory} zipped successfully to {zip_filename}.")
    else:
        print(f"Directory {directory} does not exist.")

def create_params_override(file_name, params): 
	with open(f"./parameter-overrides/{file_name}", 'w') as f: 
		for key, value in params.items(): 
			f.write(f"{key}={value}\n")

def list_resources(action, file_path: str ):
    resource_list = action()
    writeYaml(resource_list, file_path)
    return resource_list