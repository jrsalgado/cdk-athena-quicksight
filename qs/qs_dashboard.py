import yaml
import humps
from glom import glom, assign
from yaml.loader import SafeLoader
from aws_cdk import aws_quicksight as quicksight
from aws_cdk import Fn, Aws
from os import getenv
from qs.utils import convert_element_values_to_int
from qs.utils import convert_keys_to_camel_case
from qs.utils import mask_aws_account_id

def readFromOriginResourceFile():
    # Copy from original resources
    originDashboardtId= getenv('ORIGIN_DASHBOARD_ID')
    originAWSAccounttId= getenv('ORIGIN_AWS_ACCOUNT_ID')
    originalResourcePath=f"infra_base/{mask_aws_account_id(originAWSAccounttId)}/dashboards/{originDashboardtId}.yaml"

    with open(originalResourcePath) as f:
        originalResource = yaml.load(f, Loader=SafeLoader)
    camelOriginalResource = convert_keys_to_camel_case(originalResource)
    snakeOriginalResource =  convert_keys_to_snake_case(originalResource)

    return originalResource, camelOriginalResource, snakeOriginalResource

def createDashboard(self, dashboard_name: str, dataSet: quicksight.CfnDataSet):

    with open("base_templates/dashboard.yaml") as f:
        base_template = yaml.load(f, Loader=SafeLoader)
    camel_base_template = convert_keys_to_camel_case(base_template)
    base_dashboard = camel_base_template['baseDashboard']['properties'] # type: ignore

    oResource, originalResource, snakeOriginalResource = readFromOriginResourceFile()
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

    # Template - DataSetIdentifierDeclarations
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

    # Template - Sheets
    oSheets = glom(oResource,'DescribeDashboardDefinition.Definition.Sheets')
    sheets = definitions_sheets_builder(oSheets)

    definition = quicksight.CfnDashboard.DashboardVersionDefinitionProperty(
        data_set_identifier_declarations= data_set_identifier_declarations,
        analysis_defaults= camel_raw_definition.get('analysisDefaults', None),
        calculated_fields= camel_raw_definition.get('calculatedFields', None),
        column_configurations= camel_raw_definition.get('columnConfigurations', None),
        filter_groups= camel_raw_definition.get('filterGroups', None),
        parameter_declarations= camel_raw_definition.get('parameterDeclarations', None),
        sheets= sheets # type: ignore
    )
    
    quicksightdashboard = quicksight.CfnDashboard(
        self,
        dashboard_name,
        aws_account_id= Aws.ACCOUNT_ID,
        dashboard_id=self.configParams['DashboardId01'].value_as_string,
        name=f"{self.configParams['Environment'].value_as_string}-{self.configParams['DashboardName01'].value_as_string}",
        permissions=permissions,
        definition=definition
    )

    return quicksightdashboard

def definitions_sheets_builder(oSheets):
    sheets= []

    # Format Visuals
    for i, sheet in enumerate(oSheets):
        visuals = [ conv_digits_to_ints(humps.camelize(visual)) for visual in glom(sheet, 'Visuals')  ]
        layouts = [ conv_digits_to_ints(humps.camelize(layout)) for layout in glom(sheet, 'Layouts')  ]

        sheets.append(quicksight.CfnDashboard.SheetDefinitionProperty(
            sheet_id= sheet.get('SheetId'),
            name= sheet.get('Name'),
            content_type= sheet.get('ContentType'),
            visuals= visuals,
            layouts= layouts,
        ))

    return sheets

def conv_digits_to_ints(d):
    if isinstance(d, dict):
        return {key:conv_digits_to_ints(value) for key, value in d.items()}
    elif isinstance(d, list):
        return [conv_digits_to_ints(item) for item in d]
    elif isinstance(d, tuple):
        return (conv_digits_to_ints(item) for item in d)
    elif isinstance(d, str) and d.isdigit():
        return int(d)
    else:
        return d

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
    
def replace_data_set_identifier_iterative(obj, data_set_identifier_name):
    stack = [obj]

    while stack:
        current = stack.pop()

        if isinstance(current, list):
            # If the current element is a list, extend the stack with its elements
            stack.extend(current)
        elif isinstance(current, dict):
            # If the current element is a dictionary, update keys and values
            for key, value in current.items():
                if key == 'dataSetIdentifier':
                    current[key] = data_set_identifier_name
                else:
                    stack.append(value)

    return obj
