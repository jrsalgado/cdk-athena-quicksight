import yaml
from yaml.loader import SafeLoader
from aws_cdk import aws_quicksight as quicksight
from aws_cdk import Fn, Aws

#from qs_utils.id_generator import generate_id
#from qs_utils.case_parser import convert_keys_to_camel_case

def createDataSet(self, dataset_name: str, dataSource: quicksight.CfnDataSource ):

    with open("base-templates/data-set.yaml") as f:
        template = yaml.load(f, Loader=SafeLoader)
    converted_data = convert_keys_to_camel_case(template)
    base_dataset = converted_data['baseDataSetAthenaRelationalTable']['properties'] # type: ignore
    
    # Copy from original resources
    #TODO: (jayro) select from cdk synth context
    # PhysicalTableMap.CustomSql
    originalResourcePath="infra_base/064855577434/data-sets/2adf1225-b13e-4b4c-a701-ea6ccc5502a1.yaml"
    # PhysicalTableMap.RelationalTable
    #originalResourcePath="infra_base/064855577434/data-sets/2384dd87-5baa-4308-b2e4-1ec602bba012.yaml"

    with open(originalResourcePath) as f:
        originalResource = yaml.load(f, Loader=SafeLoader)
    originalResource = convert_keys_to_camel_case(originalResource)
    snakeOriginalResource =  convert_keys_to_snake_case(originalResource)

    permissions = base_dataset['permissions']

    # Set principal arn to dataset
    principal_arn = Fn.sub(
        "arn:aws:quicksight:${AWS::Region}:${AWS::AccountId}:user/default/${username}",
        {
            "aws_account": Aws.ACCOUNT_ID,
            "aws_region": Aws.REGION,
            "principal_type": self.configParams['QuickSightPrincipalType'].value_as_string,
            "namespace": self.configParams['QuickSightNamespace'].value_as_string,
            "username": self.configParams['QuickSightUsername'].value_as_string
        }
    )
    permissions[0]['principal'] = principal_arn
    
    # Template - Physical Table Map
    physical_table_map = snakeOriginalResource['describe_data_set']['data_set']['physical_table_map']
    for key, ptmItem in physical_table_map.items():
        if 'custom_sql' in ptmItem:
            physical_table_map[key] = physical_table_map_to_template(ptmItem['custom_sql'], quicksight.CfnDataSet.CustomSqlProperty,self.configParams['DataSetAthenaTableName01'].value_as_string, dataSource.attr_arn )
        elif 'relational_table' in ptmItem:
            physical_table_map[key] = physical_table_map_to_template(ptmItem['relational_table'], quicksight.CfnDataSet.RelationalTableProperty, self.configParams['DataSetAthenaTableName01'].value_as_string, dataSource.attr_arn )

    # Template - Logical Table Map
    logical_table_map = snakeOriginalResource['describe_data_set']['data_set']['logical_table_map']
    camelLogicalTableMap = originalResource['describeDataSet']['dataSet']['logicalTableMap']
    for key, _ in logical_table_map.items():
        logical_table_map[key]['alias'] = self.configParams['DataSetAthenaTableName01'].value_as_string
        logical_table_map[key] = quicksight.CfnDataSet.LogicalTableProperty(
            alias= self.configParams['DataSetAthenaTableName01'].value_as_string,
            source= quicksight.CfnDataSet.LogicalTableSourceProperty(**logical_table_map[key]['source']),
            data_transforms= camelLogicalTableMap[key]['dataTransforms']
        )

    # Template - Data Set reource
    quicksightDataSet = quicksight.CfnDataSet(self,
        dataset_name,
        aws_account_id= Aws.ACCOUNT_ID,
        data_set_id= self.configParams['DataSetAthenaId01'].value_as_string,
        name= self.configParams['DataSetAthenaName01'].value_as_string,
        import_mode= base_dataset['importMode'],
        permissions= permissions,
        data_set_usage_configuration= base_dataset['dataSetUsageConfiguration'],
        physical_table_map= physical_table_map,
        logical_table_map= logical_table_map
    )

    return quicksightDataSet

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

def physical_table_map_to_template(tableMapConfig, propertyClass, name, data_source_arn):
    tableMapConfig['name'] = name
    tableMapConfig['data_source_arn'] = data_source_arn
    physical_table_map_property = quicksight.CfnDataSet.PhysicalTableProperty(
        custom_sql= propertyClass(**tableMapConfig)
    )
    return physical_table_map_property