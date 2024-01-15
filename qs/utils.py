import random
import string
import re
import yaml
from yaml.loader import SafeLoader

def pascal_to_camel(key):
    return key[0].lower() + key[1:]

def convert_keys_to_camel_case(d):
    if isinstance(d, dict):
        return {pascal_to_camel(key): convert_keys_to_camel_case(value) for key, value in d.items()}
    elif isinstance(d, list):
        return [convert_keys_to_camel_case(item) for item in d]
    else:
        return d

def generate_id():
    characters = string.ascii_letters + string.digits
    alphanumeric_id = ''.join(random.choice(characters) for _ in range(64))
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
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (str, int)):
                # Replace AWS account IDs in strings and integers
                obj[key] = aws_account_id_pattern.sub('MASKED_ACCOUNT_ID', str(value))
            elif isinstance(value, (dict, list)):
                # Recursively mask AWS account IDs in nested structures
                mask_account_ids(value)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if isinstance(item, (str, int)):
                # Replace AWS account IDs in strings and integers
                obj[i] = aws_account_id_pattern.sub('MASKED_ACCOUNT_ID', str(item))
            elif isinstance(item, (dict, list)):
                # Recursively mask AWS account IDs in nested structures
                mask_account_ids(item)
    return obj

