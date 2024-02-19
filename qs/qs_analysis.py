import yaml
from yaml.loader import SafeLoader
from aws_cdk import aws_quicksight as quicksight
from aws_cdk import Fn, Aws
from os import getenv
from qs.utils import convert_element_values_to_int
from qs.utils import convert_keys_to_camel_case
from qs.utils import mask_aws_account_id
from qs.utils import readFromOriginResourceFile

def createAnalysis(self, analysis_id: str, analysis_name: str, dataSet: quicksight.CfnDataSet):

    with open("base-templates/analysis.yaml") as f:
        base_template = yaml.load(f, Loader=SafeLoader)
    camel_base_template = convert_keys_to_camel_case(base_template)
    base_analysis = camel_base_template['baseAnalysis']['properties']

    camelOriginalResource, snakeOriginalResource = readFromOriginResourceFile('analyses', analysis_id, mask_aws_account_id(getenv('ORIGIN_AWS_ACCOUNT_ID')))

    permissions = camelOriginalResource['describeAnalysisPermissions']['permissions']
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
    camel_raw_definition= camelOriginalResource['describeAnalysisDefinition']['definition']
    snake_raw_definition= snakeOriginalResource['describe_analysis_definition']['definition']

    snake_raw_definition.pop('options', None)

    data_set_identifier_declarations= []
    for i in range(len(camel_raw_definition['dataSetIdentifierDeclarations'])):
        idp = quicksight.CfnAnalysis.DataSetIdentifierDeclarationProperty(
            data_set_arn= dataSet.attr_arn,
            identifier= self.configParams['DataSetAthenaName01'].value_as_string
        )
        data_set_identifier_declarations.append(idp)
    snake_raw_definition['data_set_identifier_declarations']= data_set_identifier_declarations

    # Template - Sheets
    snake_raw_definition_mod = replace_data_set_identifier_iterative(snake_raw_definition.get('sheets', None), self.configParams['DataSetAthenaName01'].value_as_string)
    camel_raw_definition_mod = replace_data_set_identifier_iterative(camel_raw_definition.get('sheets', None), self.configParams['DataSetAthenaName01'].value_as_string)
    sheets = []

    for i in range(len(snake_raw_definition_mod)):
        snake_raw_definition_mod[i].pop('visuals', None)
        snake_raw_definition_mod[i].pop('layouts', None)

        camel_visuals = camel_raw_definition_mod[i]['visuals']
        camel_layouts_config = convert_element_values_to_int(camel_raw_definition_mod[i]['layouts'])
        sheets.append(quicksight.CfnAnalysis.SheetDefinitionProperty(
            visuals= camel_visuals,
            layouts= camel_layouts_config,
            **snake_raw_definition_mod[i])
        )

    definition = quicksight.CfnAnalysis.AnalysisDefinitionProperty(
        data_set_identifier_declarations= data_set_identifier_declarations,
        analysis_defaults= camel_raw_definition.get('analysisDefaults', None),
        calculated_fields= camel_raw_definition.get('calculatedFields', None),
        column_configurations= camel_raw_definition.get('columnConfigurations', None),
        filter_groups= camel_raw_definition.get('filterGroups', None),
        parameter_declarations= camel_raw_definition.get('parameterDeclarations', None),
        sheets= sheets
    )

    quicksightanalysis = quicksight.CfnAnalysis(
        self,
        analysis_name,
        analysis_id=self.configParams['AnalysisId01'].value_as_string,
        aws_account_id=Aws.ACCOUNT_ID,
        name=f"{self.configParams['Environment'].value_as_string}-{self.configParams['AnalysisName01'].value_as_string}",
        definition=definition,
        permissions=permissions
        )

    return quicksightanalysis
   
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
