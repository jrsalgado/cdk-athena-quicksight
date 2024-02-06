import os
from qs.utils import mask_aws_account_id, cleanDirs, writeYaml

def fetchQSAllResources(quicksight_client, account_id):
    print("\nDeleting old Quicksight resource files...")
    masked_account_id = mask_aws_account_id(account_id)
    cleanDirs([
        f'./infra_base/{masked_account_id}/analyses',
        f'./infra_base/{masked_account_id}/dashboards',
        f'./infra_base/{masked_account_id}/data-sets',
        f'./infra_base/{masked_account_id}/data-sources',
    ])

    print("\nFetching Quicksight Data Sources...")
    fetchQSDataSourcesResources(quicksight_client, account_id)

    print("Fetching Quicksight Data Sets...")
    fetchQSDataSetsResources(quicksight_client, account_id)

    print("Fetching Quicksight Dashboards...")
    fetchQSDashboardsResources(quicksight_client, account_id)

    print("Fetching Quicksight Analyses...")
    fetchQSAnalysesResources(quicksight_client, account_id)

    print("Fetch Completed.\n")


# DataSources

def fetchQSDataSourcesResources(quicksight_client, account_id: str) -> dict:
    masked_origin_aws_account_id = mask_aws_account_id(account_id)
    parent_dir = f'./infra_base/{masked_origin_aws_account_id}'
    child_dir = f'./infra_base/{masked_origin_aws_account_id}/data-sources'

    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, mode=0o777)

    if not os.path.exists(child_dir):
        os.makedirs(child_dir, mode=0o777)

    dataSources, file_path = listQsResource(
        account_id,
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
            account_id
        )

    return qsDataSourceResources


def createDataSourceDescriptionYaml(quicksight_client, dataSourceId: str, account_id: str):
    descriptionAggr = {}
    masked_origin_aws_account_id = mask_aws_account_id(account_id)

    data_source_res = quicksight_client.describe_data_source(
        AwsAccountId=account_id,
        DataSourceId=dataSourceId
    )
    descriptionAggr = appendToDescriptionData(
        descriptionAggr,
        'DescribeDataSource',
        data_source_res
    )

    data_source_permissions_res = quicksight_client.describe_data_source_permissions(
        AwsAccountId=account_id,
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


def fetchQSDataSetsResources(quicksight_client, account_id: str) -> dict:
    masked_origin_aws_account_id = mask_aws_account_id(account_id)
    parent_dir = f'./infra_base/{masked_origin_aws_account_id}'
    child_dir = f'./infra_base/{masked_origin_aws_account_id}/data-sets'

    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, mode=0o777)

    if not os.path.exists(child_dir):
        os.makedirs(child_dir, mode=0o777)


    dataSets, file_path = listQsResource(
        account_id,
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
            account_id)

    return qsDataSetResources


def createDataSetDescriptionYaml(quicksight_client, dataSetId: str, account_id: str):
    descriptionAggr = {}
    masked_origin_aws_account_id = mask_aws_account_id(account_id)
    data_set_res = quicksight_client.describe_data_set(
        AwsAccountId=account_id,
        DataSetId=dataSetId
    )
    descriptionAggr = appendToDescriptionData(
        descriptionAggr,
        'DescribeDataSet',
        data_set_res)

    data_set_permissions_res = quicksight_client.describe_data_set_permissions(
        AwsAccountId=account_id,
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


def fetchQSDashboardsResources(quicksight_client, account_id: str) -> dict:
    masked_origin_aws_account_id = mask_aws_account_id(account_id)
    parent_dir = f'./infra_base/{masked_origin_aws_account_id}'
    child_dir = f'./infra_base/{masked_origin_aws_account_id}/dashboards'

    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, mode=0o777)

    if not os.path.exists(child_dir):
        os.makedirs(child_dir, mode=0o777)

    dashboards, file_path = listQsResource(
        account_id,
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
            account_id)

    return qsDashboardResources


def createDashboardDescriptionYaml(quicksight_client, dashboardId: str, account_id: str):
    descriptionAggr = {}
    masked_origin_aws_account_id = mask_aws_account_id(account_id)
    dashboard_res = quicksight_client.describe_dashboard(
        AwsAccountId=account_id,
        DashboardId=dashboardId
    )
    descriptionAggr = appendToDescriptionData(
        descriptionAggr,
        'DescribeDashboard',
        dashboard_res)

    dashboard_definition_res = quicksight_client.describe_dashboard_definition(
        AwsAccountId=account_id,
        DashboardId=dashboardId
    )
    descriptionAggr = appendToDescriptionData(
        descriptionAggr,
        'DescribeDashboardDefinition',
        dashboard_definition_res)

    dashboard_permissions_res = quicksight_client.describe_dashboard_permissions(
        AwsAccountId=account_id,
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


def fetchQSAnalysesResources(quicksight_client, account_id: str) -> dict:
    masked_origin_aws_account_id = mask_aws_account_id(account_id)
    parent_dir = f'./infra_base/{masked_origin_aws_account_id}'
    child_dir = f'./infra_base/{masked_origin_aws_account_id}/analyses'

    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir, mode=0o777)

    if not os.path.exists(child_dir):
        os.makedirs(child_dir, mode=0o777)

    list_analysis, file_path = listQsResource(
        account_id,
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
            account_id)

    return qsAnalysisResources


def createAnalysisDescriptionYaml(quicksight_client, analysisId: str, account_id: str):
    descriptionAggr = {}
    masked_origin_aws_account_id = mask_aws_account_id(account_id)
    analysis_res = quicksight_client.describe_analysis(
        AwsAccountId=account_id,
        AnalysisId=analysisId
    )
    descriptionAggr = appendToDescriptionData(
        descriptionAggr,
        'DescribeAnalysis',
        analysis_res)

    analysis_definition_res = quicksight_client.describe_analysis_definition(
        AwsAccountId=account_id,
        AnalysisId=analysisId
    )
    descriptionAggr = appendToDescriptionData(
        descriptionAggr,
        'DescribeAnalysisDefinition',
        analysis_definition_res)

    analysis_permissions_res = quicksight_client.describe_analysis_permissions(
        AwsAccountId=account_id,
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
def listQsResource(account_id: str, quicksight_action, file_path: str):
    resource_list = quicksight_action(AwsAccountId=account_id)
    writeYaml(resource_list, file_path)
    return resource_list, file_path


# Utils
def appendToDescriptionData(descriptionAggr: dict, method: str, resourceResponse: dict):
    descriptionAggr[method] = resourceResponse
    return descriptionAggr