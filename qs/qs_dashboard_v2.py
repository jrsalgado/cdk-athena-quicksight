import yaml
import humps
from glom import glom, assign
from yaml.loader import SafeLoader
from aws_cdk import aws_quicksight as quicksight
from aws_cdk import Fn, Aws
from aws_cdk import Stack
from os import getenv
from qs.utils import convert_element_values_to_int
from qs.utils import convert_keys_to_camel_case
from qs.utils import mask_aws_account_id

def createDashboard(stack: Stack, dashboard_name:str , param_id:str, origin_resource ):
    with open("base_templates/dashboard.yaml") as f:
        common_base = yaml.load(f, Loader=SafeLoader)

    # Set Permissions
    permissions = glom(common_base,'BaseDashboard.Properties.Permissions')
    principal_arn = Fn.sub(
        "arn:aws:quicksight:${aws_region}:${aws_account}:${principal_type}/${namespace}/${username}",
        {
            "aws_account": Aws.ACCOUNT_ID,
            "aws_region": Aws.REGION,
            "principal_type": stack.configParams['QuickSightPrincipalType'].value_as_string,
            "namespace": stack.configParams['QuickSightNamespace'].value_as_string,
            "username": stack.configParams['QuickSightUsername'].value_as_string
        }
    )

    for i in range(len(permissions)):
        permissions[i]['Principal'] = principal_arn

    # Template - Sheets
    oSheets = glom(origin_resource,'DescribeDashboardDefinition.Definition.Sheets')
    sheets = definitions_sheets_builder(oSheets)

    # Set Definition
    oDefinition = glom(origin_resource,'DescribeDashboardDefinition.Definition')

    # Set data set identifier
    data_set_identifier_declarations= []
    idds = oDefinition.get('DataSetIdentifierDeclarations')
    #print(idds)
    for i in range(len(idds)):
        #print(i)
        idp = quicksight.CfnDashboard.DataSetIdentifierDeclarationProperty(
            data_set_arn = idds[i]['DataSetArn'],
            identifier = idds[i]['Identifier']
        )
        data_set_identifier_declarations.append(idp)

    # Template - Sheets
    oSheets = glom(origin_resource,'DescribeDashboardDefinition.Definition.Sheets')
    sheets = definitions_sheets_builder(oSheets)

    definition = quicksight.CfnDashboard.DashboardVersionDefinitionProperty(
        analysis_defaults= humps.camelize(oDefinition.get('AnalysisDefaults', None)),
        calculated_fields= humps.camelize(oDefinition.get('CalculatedFields', None)),
        column_configurations= humps.camelize(oDefinition.get('ColumnConfigurations')) if oDefinition.get('ColumnConfigurations', False) else None,
        filter_groups= humps.camelize(oDefinition.get('FilterGroups', None)),
        parameter_declarations= humps.camelize(oDefinition.get('ParameterDeclarations', None)),
        data_set_identifier_declarations= data_set_identifier_declarations,
        sheets= sheets # type: ignore
    )

    quicksightdashboard = quicksight.CfnDashboard(
        stack,
        dashboard_name,
        aws_account_id= Aws.ACCOUNT_ID,
        dashboard_id= stack.configParams[param_id].value_as_string,
        name= f"{stack.configParams['Environment'].value_as_string}-{stack.configParams[param_id].value_as_string}",
        permissions= humps.camelize(permissions),
        definition= definition
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