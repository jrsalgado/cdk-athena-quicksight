import yaml
from yaml.loader import SafeLoader
from aws_cdk import aws_quicksight as quicksight
from aws_cdk import Stack
from aws_cdk import Fn, Aws

def createDataSource( stack: Stack, datasource_name: str ):

    with open("base-templates/data-source.yaml") as f:
        data = yaml.load(f, Loader=SafeLoader)

    converted_data = convert_keys_to_camel_case(data)
    base_datasource = converted_data['baseDataSource']['properties'] # type: ignore
    aws_account_id = Aws.ACCOUNT_ID

    datasourcePrincipal= Fn.sub(
        'arn:aws:quicksight:${aws_region}:${aws_account}:${principalType}/${qsNamespace}/${user}',
        {
            'aws_account': Aws.ACCOUNT_ID,
            'aws_region': Aws.REGION,
            'principalType': stack.configParams['QuickSightPrincipalType'].value_as_string, # type: ignore
            'user': stack.configParams['QuickSightUsername'].value_as_string, # type: ignore
            'qsNamespace': stack.configParams['QuickSightNamespace'].value_as_string, # type: ignore
        }
    )

    base_datasource['dataSourceParameters']['athenaParameters']['workGroup']= stack.configParams['DataSourceAthenaWorkGroup01'].value_as_string # type: ignore
    
    base_datasource['permissions'][0]['principal'] = datasourcePrincipal
    quicksightDataSource =  quicksight.CfnDataSource(stack,
        id= datasource_name,
        aws_account_id= aws_account_id,
        data_source_id= stack.configParams['DataSourceId01'].value_as_string, # type: ignore
        name=           stack.configParams['DataSourceName01'].value_as_string, # type: ignore
        type=           base_datasource['type'],
        data_source_parameters= base_datasource['dataSourceParameters'],
        permissions=    base_datasource['permissions'],
        ssl_properties= base_datasource['sslProperties'],
    )

    return quicksightDataSource


## UTILS
def pascal_to_camel(key):
    return key[0].lower() + key[1:]

def convert_keys_to_camel_case(d):
    if isinstance(d, dict):
        return {pascal_to_camel(key): convert_keys_to_camel_case(value) for key, value in d.items()}
    elif isinstance(d, list):
        return [convert_keys_to_camel_case(item) for item in d]
    else:
        return d