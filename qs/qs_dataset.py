import yaml
from yaml.loader import SafeLoader
from aws_cdk import aws_quicksight as quicksight
from aws_cdk import Fn, Aws

#from qs_utils.id_generator import generate_id
#from qs_utils.case_parser import convert_keys_to_camel_case

def createDataSet(self, dataset_name: str, dataSource: quicksight.CfnDataSource ):

    with open("poc/base_dashboard.yaml") as f:
        data = yaml.load(f, Loader=SafeLoader)

    converted_data = convert_keys_to_camel_case(data)
    base_dataset = converted_data['resources']['baseDataSet']['properties'] # type: ignore
    permissions = base_dataset['permissions']

    # Set principal arn to dataset
    principal_arn = Fn.sub(
        "arn:aws:quicksight:${AWS::Region}:${AWS::AccountId}:user/default/${user}",
        {"user": self.configParams['QuickSightUsername'].value_as_string}
    )
    permissions[0]['principal'] = principal_arn

    # Set datasource arn to dataset
    datasource_arn = dataSource.attr_arn
    base_dataset['physicalTableMap']['s3PhysicalTable']['s3Source']['dataSourceArn'] = datasource_arn
    
    # TODO: (jayro) Create and substitute datataset as RelationalTableProperty for Athena tables
    # relational_table=quicksight.CfnDataSet.RelationalTableProperty(
    # TODO: (jayro) this is a POC, once the POC success then update the Base
    # TODO: (jayro) Also can use CustomSqlProperty using the same data source
    # TODO: (jayro) Lets figure out how the real connection has been made
    # TODO: (jayro) Create 3 bases one for test with s3 and the other with the other connections 
    physical_table_map = {
        "athena-santander-table": quicksight.CfnDataSet.PhysicalTableProperty(
            relational_table=quicksight.CfnDataSet.RelationalTableProperty(
                data_source_arn= dataSource.attr_arn,
                input_columns=base_dataset['physicalTableMap']['s3PhysicalTable']['s3Source']['inputColumns'],
                catalog="AWSDataCatalog",
                schema="athena_database_name_value_as_string",
                name="santander"
            )
        )
    }
    
    quicksightDataSet = quicksight.CfnDataSet(self,
        dataset_name,
        aws_account_id= Aws.ACCOUNT_ID,
        data_set_id= self.configParams['QuickSightDataSetId'].value_as_string,
        name= dataset_name,
        import_mode= base_dataset['importMode'],
        permissions= permissions,
        data_set_usage_configuration= base_dataset['dataSetUsageConfiguration'],
        #physical_table_map= base_dataset['physicalTableMap'],
        physical_table_map= physical_table_map,
        logical_table_map= base_dataset['logicalTableMap']
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