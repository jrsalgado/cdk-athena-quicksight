import random
import string
import re
import yaml
from yaml.loader import SafeLoader
import os

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
