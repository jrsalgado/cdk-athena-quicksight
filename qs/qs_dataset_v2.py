import yaml
from yaml.loader import SafeLoader
import humps
from glom import glom, assign
from aws_cdk import aws_quicksight as quicksight
from aws_cdk import Fn, Aws
from aws_cdk import Stack
from os import getenv
from qs.utils import mask_aws_account_id, extract_id_from_arn

def createDataSet(stack: Stack, originDatasetId:str , param_id:str, origin_resource ):
    
    with open("base_templates/data-set.yaml") as f:
        common_base = yaml.load(f, Loader=SafeLoader)

    # Set dataset name
    dataset_name = glom(origin_resource,'DescribeDataSet.DataSet.Name')
    name = f"{stack.configParams['Environment'].value_as_string}-{stack.configParams[param_id].value_as_string}"

    # Set import mode
    import_mode = glom(origin_resource,'DescribeDataSet.DataSet.ImportMode')
   
    # Set Permissions
    datasetPrincipal= Fn.sub(
        'arn:aws:quicksight:${aws_region}:${aws_account}:${principalType}/${qsNamespace}/${user}',
        {
            'aws_account': Aws.ACCOUNT_ID,
            'aws_region': Aws.REGION,
            'principalType': stack.configParams['QuickSightPrincipalType'].value_as_string, # type: ignore
            'user': stack.configParams['QuickSightUsername'].value_as_string, # type: ignore
            'qsNamespace': stack.configParams['QuickSightNamespace'].value_as_string, # type: ignore
        }
    )
    permissions = glom(common_base, 'BaseDataSetAthenaRelationalTable.Properties.Permissions')
    for i in range(len(permissions)):
        assign(permissions,f'{i}.Principal', datasetPrincipal )
    
    # Set data_set_usage_configuration
    data_set_usage_configuration = glom(common_base,'BaseDataSetAthenaRelationalTable.Properties.DataSetUsageConfiguration')

    # Set logical_table_map
    oLogicalTableMap = glom(origin_resource, 'DescribeDataSet.DataSet.LogicalTableMap')
    logical_table_map = {}
    for key, _ in oLogicalTableMap.items():
        ltprop = oLogicalTableMap[key]
        logical_table_map[key] = quicksight.CfnDataSet.LogicalTableProperty(
            alias = ltprop.get('Alias'),
            source = logical_table_source_builder(ltprop.get('Source')),
            data_transforms = humps.camelize(ltprop.get('DataTransforms')) if ltprop.get('DataTransforms', False) else None
        )

    # Set physical_table_map
    oPhysiscalTableMap = glom(origin_resource, 'DescribeDataSet.DataSet.PhysicalTableMap')
    physical_table_map = {}
    for key, ptmItem in oPhysiscalTableMap.items():
        if 'CustomSql' in ptmItem:
            tmcf = ptmItem['CustomSql']
            # Set DataSourceArn
            datasourceid = extract_id_from_arn(tmcf['DataSourceArn'])
            datasource = stack._datasources[datasourceid]
            tmcf['DataSourceArn'] = datasource.attr_arn
            #tmcf['Name'] = stack.configParams['DataSetAthenaTableName01'].value_as_string
            #print(tmcf['Name'])
            physical_table_map[key] = quicksight.CfnDataSet.PhysicalTableProperty(
                custom_sql = humps.camelize(tmcf)
                )
        elif 'RelationalTable' in ptmItem:
            tmcf = ptmItem['RelationalTable']
            # Set DataSourceArn
            datasourceid = extract_id_from_arn(tmcf['DataSourceArn'])
            datasource = stack._datasources[datasourceid]
            tmcf['DataSourceArn'] = datasource.attr_arn
            #tmcf['Name'] = self.configParams['DataSetAthenaTableName01'].value_as_string
            #print(tmcf['Name'])
            physical_table_map[key] = quicksight.CfnDataSet.PhysicalTableProperty(
                relational_table = humps.camelize(tmcf)
                )
        else:
            raise CustomError("This kind of PysicalTableMap is not implemented please ask Jayro Salgado")

    # Template - Data Set reource
    quicksightDataSet = quicksight.CfnDataSet(
        stack,
        dataset_name,
        aws_account_id= Aws.ACCOUNT_ID,
        data_set_id= stack.configParams[param_id].value_as_string,
        name = name,
        import_mode = import_mode,
        permissions = humps.camelize(permissions),
        data_set_usage_configuration = humps.camelize(data_set_usage_configuration),
        physical_table_map=  humps.camelize(physical_table_map),
        logical_table_map= logical_table_map,
    )

    return quicksightDataSet

class CustomError(Exception):
    pass

def physical_table_map_to_template(tableMapConfig, propertyClass, name, data_source_arn):
    tableMapConfig['name'] = name
    tableMapConfig['data_source_arn'] = data_source_arn
    return propertyClass(**tableMapConfig)


def logical_table_source_builder(ltsource):
    ltsourceformat = None
    if 'PhysicalTableId' in ltsource:
        jiprops = humps.camelize(ltsource.get('PhysicalTableId'))
        ltsourceformat = quicksight.CfnDataSet.LogicalTableSourceProperty(
            physical_table_id = jiprops
        )
    elif 'JoinInstruction' in ltsource :
        jiprops = humps.camelize(ltsource.get('JoinInstruction'))
        ltsourceformat = quicksight.CfnDataSet.LogicalTableSourceProperty(
            join_instruction = jiprops
        )
    else:
        print('Other Logical Table Source')
        print(ltsource)

    return ltsourceformat
