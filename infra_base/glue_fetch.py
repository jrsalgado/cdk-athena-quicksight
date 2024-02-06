import os
from qs.utils import mask_aws_account_id, cleanDirs, writeYaml

def fetchGlueResources(glue_client, account_id):
    print("Deleting old Glue resource files...")
    cleanDirs(f'./infra_base/{mask_aws_account_id(account_id)}/glue')

    print("\nFetching Glue Databases...")
    fetchGlueDatabases(glue_client, account_id)

    print("Fetch Completed.\n")

def fetchGlueDatabases(glue_client, account_id):
    masked_origin_aws_account_id = mask_aws_account_id(account_id)
    parent_dir = f'./infra_base/{masked_origin_aws_account_id}/glue'

    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, mode=0o777)

    list_databases, file_path = listGlueResource(
        glue_client.get_databases,
        f'{parent_dir}/list-databases.yaml'
    )

    glueDatabaseResources = {
        'filePathList': file_path,
    }

    for database in list_databases['DatabaseList']:
        createDatabaseDescriptionYaml(
            glue_client,
            database['Name'],
            parent_dir)

    return glueDatabaseResources

def createDatabaseDescriptionYaml(glue_client, database_name, parent_dir):
    database_description = glue_client.get_database(Name=database_name)
    database_tables = glue_client.get_tables(DatabaseName=database_name)

    database_output = { 'DatabaseDescription': database_description, 'DatabaseTables': database_tables}

    file_path = f'{parent_dir}/{database_name}.yaml'
    writeYaml(database_output, file_path)
    return file_path

def listGlueResource(glue_action, file_path: str):
    resource_list = glue_action()
    writeYaml(resource_list, file_path)
    return resource_list, file_path