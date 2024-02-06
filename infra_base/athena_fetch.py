import os
from qs.utils import mask_aws_account_id, cleanDirs, writeYaml

def fetchAthenaResources(athena_client, account_id):
    print("Deleting old Athena resource files...")
    cleanDirs(f'./infra_base/{mask_aws_account_id(account_id)}/athena')

    print("\nFetching Athena Workgroups...")
    fetchAthenaWorkgroups(athena_client, account_id)

    print("Fetching Athena Data Catalogs...")
    fetchAthenaDataCatalogs(athena_client, account_id)

    print("Fetch Completed.\n")

def fetchAthenaWorkgroups(athena_client, account_id):
    masked_origin_aws_account_id = mask_aws_account_id(account_id)
    parent_dir = f'./infra_base/{masked_origin_aws_account_id}/athena'
    child_dir = f'./infra_base/{masked_origin_aws_account_id}/athena/workgroups'

    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, mode=0o777)

    if not os.path.exists(child_dir):
        os.makedirs(child_dir, mode=0o777)

    list_work_groups, file_path = listAthenaResource(
        athena_action=athena_client.list_work_groups,
        file_path=f'./infra_base/{masked_origin_aws_account_id}/athena/workgroups/list-workgroups.yaml'
    )

    athenaWorkgroupResources = {
        'filePathList': file_path,
    }

    for workgroup in list_work_groups['WorkGroups']:
        createWorkgroupDescriptionYaml(
            athena_client,
            workgroup['Name'],
            account_id)

    return athenaWorkgroupResources

def createWorkgroupDescriptionYaml(athena_client, workgroup_name, account_id):
    masked_origin_aws_account_id = mask_aws_account_id(account_id)

    workgroup_res = athena_client.get_work_group(
        WorkGroup=workgroup_name
    )

    file_path = f'./infra_base/{masked_origin_aws_account_id}/athena/workgroups/{workgroup_name}.yaml'
    writeYaml(workgroup_res, file_path)
    return file_path

def fetchAthenaDataCatalogs(athena_client, account_id):
    masked_origin_aws_account_id = mask_aws_account_id(account_id)
    parent_dir = f'./infra_base/{masked_origin_aws_account_id}/athena'
    child_dir = f'./infra_base/{masked_origin_aws_account_id}/athena/data-catalogs'

    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, mode=0o777)

    if not os.path.exists(child_dir):
        os.makedirs(child_dir, mode=0o777)

    list_data_catalogs, file_path = listAthenaResource(
        athena_client.list_data_catalogs,
        f'./infra_base/{masked_origin_aws_account_id}/athena/data-catalogs/list-data-catalogs.yaml'
    )

    athenaDataCatalogResources = {
        'filePathList': file_path,
    }

    for data_catalog in list_data_catalogs['DataCatalogsSummary']:
        if data_catalog['CatalogName'] != "AwsDataCatalog":
            createDataCatalogDescriptionYaml(
                athena_client,
                data_catalog['CatalogName'],
                account_id)

    return athenaDataCatalogResources

def createDataCatalogDescriptionYaml(athena_client, data_catalog_name, account_id):
    masked_origin_aws_account_id = mask_aws_account_id(account_id)

    data_catalog_res = athena_client.get_data_catalog(
        Name=data_catalog_name
    )

    file_path = f'./infra_base/{masked_origin_aws_account_id}/athena/data-catalogs/{data_catalog_name}.yaml'
    writeYaml(data_catalog_res, file_path)
    return file_path

def listAthenaResource(athena_action, file_path: str):
    resource_list = athena_action()
    writeYaml(resource_list, file_path)
    return resource_list, file_path