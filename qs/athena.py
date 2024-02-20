import yaml
from yaml.loader import SafeLoader
from aws_cdk import aws_athena as athena
from aws_cdk import Aws
from os import getenv
from qs.utils import convert_keys_to_snake_case
from qs.utils import convert_keys_to_camel_case
from qs.utils import mask_aws_account_id
from qs.utils import create_params_override
from qs.utils import read_origin_resource_file

def createAthena(self, account_id):

    params_object = {}

    ######################
    ## Workgroup 
    ######################
    if getenv('ORIGIN_WORKGROUP_NAME') == 'base':
        params_object['AthenaWorkgroupName'] = f"BaseWorkGroup{getenv('HASH_SUFFIX')}"

        resource_path = f"./base_templates/workgroup.yaml"
        workgroup_origin_camel, workgroup_origin_snake = read_origin_resource_file(resource_path=resource_path)

        workgroup = athena.CfnWorkGroup(self, 
            "AthenaWorkGroup01",
            name=f"{self.configParams['Environment'].value_as_string}-{self.configParams['AthenaWorkgroupName'].value_as_string}",
            recursive_delete_option=True,
            state='ENABLED',
            work_group_configuration=athena.CfnWorkGroup.WorkGroupConfigurationProperty(
                enforce_work_group_configuration=False,
                bytes_scanned_cutoff_per_query=1099511627776000,
                engine_version=athena.CfnWorkGroup.EngineVersionProperty(
                    effective_engine_version='AUTO',
                    selected_engine_version='Athena engine version 3'
                ),
                publish_cloud_watch_metrics_enabled=False,
                requester_pays_enabled=False
            )
        )
    else:
        workgroupOriginCamel, workgroupOriginSnake = readFromAthenaOriginResourceFile(mask_aws_account_id(account_id), resource_type='workgroups', resource_name=getenv('ORIGIN_WORKGROUP_NAME'))

        params_object['AthenaWorkgroupName'] = f"{workgroupOriginSnake['work_group']['name']}{getenv('HASH_SUFFIX')}"
        workgroupCamelConfiguration = workgroupOriginCamel['workGroup']['configuration']
        workgroupSnakeConfiguration = workgroupOriginSnake['work_group']['configuration']
        workgroupSnakeConfiguration.pop('enable_minimum_encryption_configuration', None)
        workgroupSnakeConfiguration.pop('result_configuration', None)
        workgroupSnakeConfiguration.pop('engine_version', None)

        engine_version = workgroupCamelConfiguration['engineVersion']

        ## check if workgroupSnakeConfiguration['bytes_scanned_cutoff_per_query'] exists first
        if 'bytes_scanned_cutoff_per_query' in workgroupSnakeConfiguration:
            workgroupSnakeConfiguration['bytes_scanned_cutoff_per_query'] = int(workgroupSnakeConfiguration['bytes_scanned_cutoff_per_query'])

        workgroupSnakeConfigurationParsedBooleans = convertValuesToRealBoolean(workgroupSnakeConfiguration)

        workgroup01 = athena.CfnWorkGroup(self, 
            "AthenaWorkGroup01",
            name=f"{self.configParams['Environment'].value_as_string}-{self.configParams['AthenaWorkgroupName'].value_as_string}",
            work_group_configuration=athena.CfnWorkGroup.WorkGroupConfigurationProperty(
                **workgroupSnakeConfigurationParsedBooleans,
                engine_version=engine_version
            )
        )
    

    ######################
    ## Data CAtalog 
    ######################
    if getenv('ORIGIN_CATALOG_NAME') == 'base':
        params_object['AthenaDataCatalogName'] = f"BaseDataCatalog{getenv('HASH_SUFFIX')}"

        data_catalog = athena.CfnDataCatalog(self,
            "AthenaDataCatalog01",
            name=f"{self.configParams['Environment'].value_as_string}-{self.configParams['AthenaDataCatalogName'].value_as_string}",
            type="GLUE",
            parameters={
                "catalog-id": Aws.ACCOUNT_ID
            },
        )
    else:
        catalogOriginCamel, catalogOriginSnake = readFromAthenaOriginResourceFile(mask_aws_account_id(account_id), resource_type='data-catalogs', resource_name=getenv('ORIGIN_CATALOG_NAME'))

        params_object['AthenaDataCatalogName'] = f"{catalogOriginSnake['data_catalog']['name']}{getenv('HASH_SUFFIX')}"
        catalogSnakeConfiguration = catalogOriginSnake['data_catalog']
        catalogSnakeConfiguration.pop('name', None)
        catalogSnakeConfiguration.pop('type', None)
        catalogSnakeConfiguration.pop('parameters', None)

        athena.CfnDataCatalog(self,
            "AthenaDataCatalog01",
            name=f"{self.configParams['Environment'].value_as_string}-{self.configParams['AthenaDataCatalogName'].value_as_string}",
            type="GLUE",
            parameters={
                "catalog-id": Aws.ACCOUNT_ID
            },
            **catalogSnakeConfiguration
        )
        pass

    create_params_override(file_name='athena.origin.txt', params=params_object)


def readFromAthenaOriginResourceFile(masked_account_id, resource_type, resource_name):
    originalResourcePath=f"infra_base/{masked_account_id}/athena/{resource_type}/{resource_name}.yaml"

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