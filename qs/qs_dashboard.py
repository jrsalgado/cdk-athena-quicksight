import yaml
from yaml.loader import SafeLoader
from aws_cdk import aws_quicksight as quicksight

def createDashboard(self, dashboard_name, account_id, dashboard_id, permissions_principal, datasetObj):

    with open("base_dashboard.yaml") as f:
        data = yaml.load(f, Loader=SafeLoader)

    converted_data = convert_keys_to_camel_case(data)
    base_dashboard = converted_data['resources']['baseDashboard']
    definition = base_dashboard['properties']['definition']
    permissions = base_dashboard['properties']['permissions']

    permissions[0]['principal'] = permissions_principal.value_as_string

    definition['dataSetIdentifierDeclarations'] = [
        {
            'dataSetArn': datasetObj.attr_arn,
            'identifier': datasetObj.name
        }
    ]

    quicksightdashboard = quicksight.CfnDashboard(
        self,
        dashboard_name,
        aws_account_id=account_id.value_as_string, # ADD PARAMETER
        dashboard_id=dashboard_id, # ADD PARAMETER
        name=dashboard_name, # ADD PARAMETER OPTIONAL
        permissions=permissions,
        definition=definition
    )

    return quicksightdashboard


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