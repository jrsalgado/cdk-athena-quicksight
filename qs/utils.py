import random
import string

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
