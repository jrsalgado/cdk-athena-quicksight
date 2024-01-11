import yaml
from yaml.loader import SafeLoader
from aws_cdk import aws_quicksight as quicksight
from aws_cdk import Fn, Aws
from os import getenv
from qs.utils import generate_id
from qs.utils import convert_keys_to_camel_case

def createDashboard(self, dashboard_name: str, dataSet: quicksight.CfnDataSet):

    with open("base-templates/dashboard.yaml") as f:
        base_template = yaml.load(f, Loader=SafeLoader)
    camel_base_template = convert_keys_to_camel_case(base_template)
    base_dashboard = camel_base_template['baseDashboard']['properties'] # type: ignore

    # Copy from original resources
    originDashboardtId= getenv('ORIGIN_DASHBOARD_ID')
    originAWSAccounttId= getenv('ORIGIN_AWS_ACCOUNT_ID')
    originalResourcePath=f"infra_base/{originAWSAccounttId}/dashboards/{originDashboardtId}.yaml"

    with open(originalResourcePath) as f:
        originalResource = yaml.load(f, Loader=SafeLoader)
    originalResource = convert_keys_to_camel_case(originalResource)
    snakeOriginalResource =  convert_keys_to_snake_case(originalResource)

    # Template - Permissions
    permissions = base_dashboard['permissions']
    principal_arn = Fn.sub(
        "arn:aws:quicksight:${aws_region}:${aws_account}:${principal_type}/${namespace}/${username}",
        {
            "aws_account": Aws.ACCOUNT_ID,
            "aws_region": Aws.REGION,
            "principal_type": self.configParams['QuickSightPrincipalType'].value_as_string,
            "namespace": self.configParams['QuickSightNamespace'].value_as_string,
            "username": self.configParams['QuickSightUsername'].value_as_string
        }
    )

    for i in range(len(permissions)):
        permissions[i]['principal'] = principal_arn

    # Template - Definition
    camel_raw_definition= originalResource['describeDashboardDefinition']['definition']
    raw_definition= snakeOriginalResource['describe_dashboard_definition']['definition']
    raw_definition.pop('options', None)
    idds= raw_definition.pop('data_set_identifier_declarations', None)
    data_set_identifier_declarations= []
    for i in range(len(idds)):
        idp = quicksight.CfnDashboard.DataSetIdentifierDeclarationProperty(
            data_set_arn= dataSet.attr_arn,
            identifier= self.configParams['DashboardDataSetIdentifier01'].value_as_string
        )
        data_set_identifier_declarations.append(idp)

    raw_definition['data_set_identifier_declarations']= data_set_identifier_declarations

    definition = quicksight.CfnDashboard.DashboardVersionDefinitionProperty(
        data_set_identifier_declarations= data_set_identifier_declarations,
        analysis_defaults= camel_raw_definition.get('analysisDefaults', None),
        calculated_fields= camel_raw_definition.get('calculatedFields', None),
        column_configurations= camel_raw_definition.get('columnConfigurations', None),
        filter_groups= camel_raw_definition.get('filterGroups', None),
        parameter_declarations= camel_raw_definition.get('parameterDeclarations', None),
        sheets= camel_raw_definition.get('sheets', None),
    )
    
    quicksightdashboard = quicksight.CfnDashboard(
        self,
        dashboard_name,
        aws_account_id= Aws.ACCOUNT_ID,
        dashboard_id=self.configParams['DashboardId01'].value_as_string,
        name=self.configParams['DashboardName01'].value_as_string,
        permissions=permissions,
        definition=definition
    )

    return quicksightdashboard


def createNoDepsDashboard(self):
    originDashboardtId= getenv('ORIGIN_DASHBOARD_ID')
    originAWSAccounttId= getenv('ORIGIN_AWS_ACCOUNT_ID')
    originalResourcePath=f"infra_base/{originAWSAccounttId}/dashboards/{originDashboardtId}.yaml"

    with open(originalResourcePath) as f:
        dashboard_data = yaml.load(f, Loader=SafeLoader)
    cvt_dashboard_data = convert_keys_to_camel_case(dashboard_data)

    with open("base-templates/dashboard.yaml") as f:
        data = yaml.load(f, Loader=SafeLoader)

    converted_data = convert_keys_to_camel_case(data)

    #base_dashboard = converted_data['resources']['baseDashboard']['properties']

    definition = cvt_dashboard_data['definition']
    permissions = cvt_dashboard_data['permissions']

    # Set principal arn to dataset
    principal_arn = Fn.sub(
        "arn:aws:quicksight:${AWS::Region}:${AWS::AccountId}:user/default/${user}",
        {"user": self.configParams['QuickSightUsername'].value_as_string}
    )
    permissions[0]['principal'] = principal_arn
    
    definition['dataSetIdentifierDeclarations'] = [
        {
            'dataSetArn': self.configParams['QuickSightDashboardDataSetARN01'].value_as_string,
            'identifier': self.configParams['QuickSightDashboardDataSetName01'].value_as_string,
        }
    ]

    modifyDataSetIdentifier(self, definition['sheets'], cvt_dashboard_data['dashboard']['name'])

    quicksightdashboard = quicksight.CfnDashboard(
        self,
        cvt_dashboard_data['dashboard']['name'],
        aws_account_id= Aws.ACCOUNT_ID,
        dashboard_id= self.configParams['QuickSightDashboardId'].value_as_string,
        name= cvt_dashboard_data['dashboard']['name'],
        permissions= permissions,
        definition= definition
    )

    return quicksightdashboard


#visuals[0]['lineChartVisual']['chartConfiguration']['fieldWells']['lineChartAggregatedFieldWells']['category'][0]['dateDimensionField']['column']['dataSetIdentifier'] = identifierName
def modifyDataSetIdentifier(self, sheets, identifierName: str):
    for index, sheet in enumerate(sheets):
        sheet['sheetId'] = self.configParams[f'QuickSightDashboardSheetId01'].value_as_string
        visuals = sheet['visuals']

        # Iterate through each visual in the list
        for visual in visuals:
            # Get the type of the visual (e.g., LineChartVisual, PieChartVisual, etc.)
            visual_type = next(iter(visual))

            visual[visual_type]['visualId'] = generate_id()

            # Get the chart configuration of the current visual
            chart_config = visual[visual_type]['chartConfiguration']
            
            # Define a function to recursively update DataSetIdentifier
            def update_data_set_identifier(obj):
                if isinstance(obj, list):
                    for i, item in enumerate(obj):
                        obj[i] = update_data_set_identifier(item)
                elif isinstance(obj, dict):
                    if 'column' in obj and 'dataSetIdentifier' in obj['column']:
                        obj['column']['dataSetIdentifier'] = identifierName
                    for key, value in obj.items():
                        obj[key] = update_data_set_identifier(value)
                return obj

            # Update DataSetIdentifier inside the Column of each visual
            chart_config = update_data_set_identifier(chart_config)

    return visuals

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