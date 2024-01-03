import yaml
from yaml.loader import SafeLoader
from aws_cdk import aws_quicksight as quicksight
from aws_cdk import Fn, Aws

from qs.utils import generate_id
from qs.utils import convert_keys_to_camel_case

def createDashboard(self, dashboard_name: str, dataset_object: quicksight.CfnDataSet):

    with open("poc/base_dashboard.yaml") as f:
        data = yaml.load(f, Loader=SafeLoader)

    converted_data = convert_keys_to_camel_case(data)
    base_dashboard = converted_data['resources']['baseDashboard']['properties']

    definition = base_dashboard['definition']
    permissions = base_dashboard['permissions']

    # Set principal arn to dataset
    principal_arn = Fn.sub(
        "arn:aws:quicksight:${AWS::Region}:${AWS::AccountId}:user/default/${user}",
        {"user": self.configParams['QuickSightUsername'].value_as_string}
    )
    permissions[0]['principal'] = principal_arn

    definition['dataSetIdentifierDeclarations'] = [
        {
            'dataSetArn': dataset_object.attr_arn,
            'identifier': dataset_object.name
        }
    ]

    modifyDataSetIdentifier(self, definition['sheets'], dataset_object.name)

    quicksightdashboard = quicksight.CfnDashboard(
        self,
        dashboard_name,
        aws_account_id= Aws.ACCOUNT_ID,
        dashboard_id=self.configParams['QuickSightDashboardId'].value_as_string,
        name=dashboard_name,
        permissions=permissions,
        definition=definition
    )

    return quicksightdashboard


def createNoDepsDashboard(self):

    with open("infra_base/jaypoc/e6390395-4a03-4d80-b862-a4d3506173c8.yaml") as f:
        dashboard_data = yaml.load(f, Loader=SafeLoader)
    cvt_dashboard_data = convert_keys_to_camel_case(dashboard_data)

    with open("poc/base_dashboard.yaml") as f:
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
        sheet['sheetId'] = self.configParams[f'QuickSightDashboardSheetId0{index+1}'].value_as_string
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