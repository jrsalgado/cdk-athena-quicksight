import os
import shutil
import yaml
from qs.utils import mask_aws_account_id, mask_account_ids


def fetchQSAllResources(quicksight_client, qs_aws_account_id):
    print("Cleaning old resource files...")
    cleanDirs(path=f'./{qs_aws_account_id}')

    print("\nFetching DataSource Resources...")
    fetchQSDataSourcesResources(quicksight_client, qs_aws_account_id)

    print("Fetching DataSet Resources...")
    fetchQSDataSetsResources(quicksight_client, qs_aws_account_id)

    print("Fetching Dashboard Resources...")
    fetchQSDashboardsResources(quicksight_client, qs_aws_account_id)

    print("Fetching Analysis Resources...")
    fetchQSAnalysesResources(quicksight_client, qs_aws_account_id)

    print("\nFetch Completed.")


# DataSources

def fetchQSDataSourcesResources(quicksight_client, qs_aws_account_id: str) -> dict:
    masked_origin_aws_account_id = mask_aws_account_id(qs_aws_account_id)
    print(masked_origin_aws_account_id)
    parent_dir = f'./infra_base/{masked_origin_aws_account_id}'
    child_dir = f'./infra_base/{masked_origin_aws_account_id}/data-sources'

    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, mode=0o777)

    if not os.path.exists(child_dir):
        os.makedirs(child_dir, mode=0o777)

    dataSources, file_path = listQsResource(
        qs_aws_account_id,
        quicksight_client.list_data_sources,
        f'./infra_base/{masked_origin_aws_account_id}/data-sources/list-data-sources.yaml'
    )

    qsDataSourceResources = {
        'filePathList': file_path,
    }

    for dataSource in dataSources['DataSources']:
        createDataSourceDescriptionYaml(
            quicksight_client,
            dataSource['DataSourceId'],
            qs_aws_account_id
        )

    return qsDataSourceResources


def createDataSourceDescriptionYaml(quicksight_client, dataSourceId: str, qs_aws_account_id: str):
    descriptionAggr = {}
    masked_origin_aws_account_id = mask_aws_account_id(qs_aws_account_id)

    data_source_res = quicksight_client.describe_data_source(
        AwsAccountId=qs_aws_account_id,
        DataSourceId=dataSourceId
    )
    descriptionAggr = appendToDescriptionData(
        descriptionAggr,
        'DescribeDataSource',
        data_source_res
    )

    data_source_permissions_res = quicksight_client.describe_data_source_permissions(
        AwsAccountId=qs_aws_account_id,
        DataSourceId=dataSourceId
    )
    descriptionAggr = appendToDescriptionData(
        descriptionAggr,
        'DescribeDataSourcePermissions',
        data_source_permissions_res
    )

    file_path = f'./infra_base/{masked_origin_aws_account_id}/data-sources/{dataSourceId}.yaml'
    writeYaml(descriptionAggr, file_path)
    return file_path

# DataSet


def fetchQSDataSetsResources(quicksight_client, qs_aws_account_id: str) -> dict:
    masked_origin_aws_account_id = mask_aws_account_id(qs_aws_account_id)
    parent_dir = f'./infra_base/{masked_origin_aws_account_id}'
    child_dir = f'./infra_base/{masked_origin_aws_account_id}/data-sets'

    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, mode=0o777)

    if not os.path.exists(child_dir):
        os.makedirs(child_dir, mode=0o777)


    dataSets, file_path = listQsResource(
        qs_aws_account_id,
        quicksight_client.list_data_sets,
        f'./infra_base/{masked_origin_aws_account_id}/data-sets/list-data-sets.yaml'
    )

    qsDataSetResources = {
        'filePathList': file_path,
    }

    for dataSet in dataSets['DataSetSummaries']:
        createDataSetDescriptionYaml(
            quicksight_client,
            dataSet['DataSetId'],
            qs_aws_account_id)

    return qsDataSetResources


def createDataSetDescriptionYaml(quicksight_client, dataSetId: str, qs_aws_account_id: str):
    descriptionAggr = {}
    masked_origin_aws_account_id = mask_aws_account_id(qs_aws_account_id)
    data_set_res = quicksight_client.describe_data_set(
        AwsAccountId=qs_aws_account_id,
        DataSetId=dataSetId
    )
    descriptionAggr = appendToDescriptionData(
        descriptionAggr,
        'DescribeDataSet',
        data_set_res)

    data_set_permissions_res = quicksight_client.describe_data_set_permissions(
        AwsAccountId=qs_aws_account_id,
        DataSetId=dataSetId
    )
    descriptionAggr = appendToDescriptionData(
        descriptionAggr,
        'DescribeDataSetPermissions',
        data_set_permissions_res)

    file_path = f'./infra_base/{masked_origin_aws_account_id}/data-sets/{dataSetId}.yaml'
    writeYaml(descriptionAggr, file_path)
    return file_path

# Dashboards


def fetchQSDashboardsResources(quicksight_client, qs_aws_account_id: str) -> dict:
    masked_origin_aws_account_id = mask_aws_account_id(qs_aws_account_id)
    parent_dir = f'./infra_base/{masked_origin_aws_account_id}'
    child_dir = f'./infra_base/{masked_origin_aws_account_id}/dashboards'

    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, mode=0o777)

    if not os.path.exists(child_dir):
        os.makedirs(child_dir, mode=0o777)

    dashboards, file_path = listQsResource(
        qs_aws_account_id,
        quicksight_client.list_dashboards,
        f'./infra_base/{masked_origin_aws_account_id}/dashboards/list-dashboards.yaml'
    )

    qsDashboardResources = {
        'filePathList': file_path,
    }

    for dashboard in dashboards['DashboardSummaryList']:
        createDashboardDescriptionYaml(
            quicksight_client,
            dashboard['DashboardId'],
            qs_aws_account_id)

    return qsDashboardResources


def createDashboardDescriptionYaml(quicksight_client, dashboardId: str, qs_aws_account_id: str):
    descriptionAggr = {}
    masked_origin_aws_account_id = mask_aws_account_id(qs_aws_account_id)
    dashboard_res = quicksight_client.describe_dashboard(
        AwsAccountId=qs_aws_account_id,
        DashboardId=dashboardId
    )
    descriptionAggr = appendToDescriptionData(
        descriptionAggr,
        'DescribeDashboard',
        dashboard_res)

    dashboard_definition_res = quicksight_client.describe_dashboard_definition(
        AwsAccountId=qs_aws_account_id,
        DashboardId=dashboardId
    )
    descriptionAggr = appendToDescriptionData(
        descriptionAggr,
        'DescribeDashboardDefinition',
        dashboard_definition_res)

    dashboard_permissions_res = quicksight_client.describe_dashboard_permissions(
        AwsAccountId=qs_aws_account_id,
        DashboardId=dashboardId
    )
    descriptionAggr = appendToDescriptionData(
        descriptionAggr,
        'DescribeDashboardPermissions',
        dashboard_permissions_res)

    file_path = f'./infra_base/{masked_origin_aws_account_id}/dashboards/{dashboardId}.yaml'
    writeYaml(descriptionAggr, file_path)
    return file_path

# Analysis


def fetchQSAnalysesResources(quicksight_client, qs_aws_account_id: str) -> dict:
    masked_origin_aws_account_id = mask_aws_account_id(qs_aws_account_id)
    parent_dir = f'./infra_base/{masked_origin_aws_account_id}'
    child_dir = f'./infra_base/{masked_origin_aws_account_id}/analyses'

    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, mode=0o777)

    if not os.path.exists(child_dir):
        os.makedirs(child_dir, mode=0o777)

    list_analysis, file_path = listQsResource(
        qs_aws_account_id,
        quicksight_client.list_analyses,
        f'./infra_base/{masked_origin_aws_account_id}/analyses/list-analysis.yaml'
    )

    qsAnalysisResources = {
        'filePathList': file_path,
    }

    for analysis in list_analysis['AnalysisSummaryList']:
        createAnalysisDescriptionYaml(
            quicksight_client,
            analysis['AnalysisId'],
            qs_aws_account_id)

    return qsAnalysisResources


def createAnalysisDescriptionYaml(quicksight_client, analysisId: str, qs_aws_account_id: str):
    descriptionAggr = {}
    masked_origin_aws_account_id = mask_aws_account_id(qs_aws_account_id)
    analysis_res = quicksight_client.describe_analysis(
        AwsAccountId=qs_aws_account_id,
        AnalysisId=analysisId
    )
    descriptionAggr = appendToDescriptionData(
        descriptionAggr,
        'DescribeAnalysis',
        analysis_res)

    analysis_definition_res = quicksight_client.describe_analysis_definition(
        AwsAccountId=qs_aws_account_id,
        AnalysisId=analysisId
    )
    descriptionAggr = appendToDescriptionData(
        descriptionAggr,
        'DescribeAnalysisDefinition',
        analysis_definition_res)

    analysis_permissions_res = quicksight_client.describe_analysis_permissions(
        AwsAccountId=qs_aws_account_id,
        AnalysisId=analysisId
    )
    descriptionAggr = appendToDescriptionData(
        descriptionAggr,
        'DescribeAnalysisPermissions',
        analysis_permissions_res)

    file_path = f'./infra_base/{masked_origin_aws_account_id}/analyses/{analysisId}.yaml'
    writeYaml(descriptionAggr, file_path)
    return file_path

# General Functions


def listQsResource(qs_aws_account_id: str, quicksight_action, file_path: str):
    resource_list = quicksight_action(AwsAccountId=qs_aws_account_id)
    writeYaml(resource_list, file_path)
    return resource_list, file_path


# Utils

def cleanDirs(path: str):
    if not os.path.exists(path):
        print("Nothing to delete.")
        return

    try:
        shutil.rmtree(path)
    except OSError as e:
        print(f"Error removing directory '{path}': {e}")


def appendToDescriptionData(descriptionAggr: dict, method: str, resourceResponse: dict):
    descriptionAggr[method] = resourceResponse
    return descriptionAggr


def convertToYaml(data: dict):
    yaml_data = yaml.dump(data, default_flow_style=False)
    return yaml_data


def writeYaml(dataObj: dict, path: str):
    maskedData = mask_account_ids(dataObj)
    dataYaml = convertToYaml(maskedData)
    with open(path, 'w') as file:
        file.write(dataYaml)
