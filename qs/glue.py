import yaml
from yaml.loader import SafeLoader
from aws_cdk import aws_glue as glue
from aws_cdk import Aws
from os import getenv
from qs.utils import convert_keys_to_snake_case
from qs.utils import convert_keys_to_camel_case
from qs.utils import mask_aws_account_id

def createGlue(self, account_id):

    ######################
    ## Database 
    ######################

    databaseOriginCamel, databaseOriginSnake = readFromGlueOriginResourceFile(mask_aws_account_id(account_id), database_name=getenv('ORIGIN_DATABASE_NAME'))


    databaseCamelConfiguration = databaseOriginCamel['databaseDescription']['database']

    database01 = glue.CfnDatabase(self, 
        "GlueDatabase01", 
        catalog_id=Aws.ACCOUNT_ID, 
        database_input=glue.CfnDatabase.DatabaseInputProperty(
            name=self.configParams['GlueDatabaseName'].value_as_string,
            create_table_default_permissions=databaseCamelConfiguration['createTableDefaultPermissions']
    ))

    ######################
    ## Tables
    ######################

    databaseCamelOriginTables = databaseOriginCamel['databaseTables']['tableList']
    databaseSnakeOriginTables = databaseOriginSnake['database_tables']['table_list']

    for index in range(len(databaseCamelOriginTables)):
        createTable(self, database01.ref, databaseCamelOriginTables[index], databaseSnakeOriginTables[index], index)

def createTable(self, database_ref, camel_table_config, snake_table_config, index):
    tableOriginCamelConfiguration = camel_table_config
    tableOriginSnakeConfiguration = snake_table_config

    tableOriginCamelStorageDescriptor = convertValuesToRealBoolean(tableOriginCamelConfiguration['storageDescriptor']) 
    tableOriginSnakeStorageDescriptor = convertValuesToRealBoolean(tableOriginSnakeConfiguration['storage_descriptor']) 
    
    serdeInfo = tableOriginCamelStorageDescriptor['serdeInfo']
    tableOriginSnakeStorageDescriptor.pop('serde_info', None)

    numberOfBuckets = int(tableOriginSnakeStorageDescriptor['number_of_buckets'])
    tableOriginSnakeStorageDescriptor.pop('number_of_buckets', None)

    if 'skewedInfo' in tableOriginCamelStorageDescriptor:
        skewedInfo = tableOriginCamelStorageDescriptor['skewedInfo']
        tableOriginSnakeStorageDescriptor.pop('skewed_info', None)
    else:
        skewedInfo = None

    table01 = glue.CfnTable(self,
        f"GlueTable0{index}",
        catalog_id=Aws.ACCOUNT_ID,
        database_name=database_ref,
        table_input=glue.CfnTable.TableInputProperty(
            name=tableOriginCamelConfiguration['name'],
            parameters=tableOriginCamelConfiguration['parameters'],
            table_type=tableOriginCamelConfiguration['tableType'],
            storage_descriptor=glue.CfnTable.StorageDescriptorProperty(
                number_of_buckets=numberOfBuckets,
                skewed_info=skewedInfo,
                serde_info=glue.CfnTable.SerdeInfoProperty(
                    parameters=serdeInfo['parameters'],
                    serialization_library=serdeInfo['serializationLibrary']
                ),
                **tableOriginSnakeStorageDescriptor
            ),
        )
    )

def readFromGlueOriginResourceFile(masked_account_id, database_name):
    originalResourcePath=f"infra_base/{masked_account_id}/glue/{database_name}.yaml"

    with open(originalResourcePath) as f:
        originalResource = yaml.load(f, Loader=SafeLoader)

    camelOriginalResource = convert_keys_to_camel_case(originalResource)
    snakeOriginalResource =  convert_keys_to_snake_case(originalResource)

    return camelOriginalResource, snakeOriginalResource

def convertValuesToRealBoolean(config_object: dict):
    if not isinstance(config_object, dict):
        return config_object

    real_booleans_obj = config_object.copy()

    for key, value in real_booleans_obj.items():
        if isinstance(value, str) and value.lower() in ['true', 'false']:
            real_booleans_obj[key] = True if value.lower() == 'true' else False
        elif isinstance(value, dict):
            real_booleans_obj[key] = convertValuesToRealBoolean(value)

    return real_booleans_obj