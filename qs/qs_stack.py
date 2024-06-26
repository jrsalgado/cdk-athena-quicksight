import yaml
from glom import glom
from yaml.loader import SafeLoader
from constructs import Construct
from aws_cdk import (
    CfnParameter,
    Stack,
)
from os import getenv
from qs.utils import extract_id_from_arn, readFromOriginResourceFile
from qs.utils import find_all_values_iterative, mask_aws_account_id
###########################################################
from qs.qs_datasource import createDataSource
from qs.qs_dataset import createDataSet
from qs.qs_dashboard import createDashboard
from qs.qs_analysis import createAnalysis
###########################################################
from qs.athena import createAthena
###########################################################
from qs.glue import createGlue

class QsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.configParams = {}

        general_params = self.node.try_get_context("general_params")
        general_params_file = self.read_params_file(general_params)
        self.define_parameters(general_params_file)

        data_source_id = getenv('ORIGIN_DATASOURCE_ID', None)
        data_set_id = getenv('ORIGIN_DATASET_ID', None)
        dashboard_id = getenv('ORIGIN_DASHBOARD_ID', None)
        analysis_id = getenv('ORIGIN_ANALYSIS_ID', None)
        masked_origin_aws_account_id = mask_aws_account_id(getenv('ORIGIN_AWS_ACCOUNT_ID'))

        # Build athena template
        if getenv('SYNTH_ATHENA'):
            athena_params = self.node.try_get_context("athena_params")
            athena_params_file = self.read_params_file(athena_params)
            self.define_parameters(athena_params_file)

            createAthena(self, account_id=getenv('ORIGIN_AWS_ACCOUNT_ID'))

        # Build glue template
        if getenv('ORIGIN_DATABASE_NAME'):
            glue_params = self.node.try_get_context("glue_params")
            glue_params_file = self.read_params_file(glue_params)
            self.define_parameters(glue_params_file)

            database01 = createGlue(self, account_id=getenv('ORIGIN_AWS_ACCOUNT_ID'))
            return

        if getenv('ORIGIN_IDS_RESOLVE') is not None:
            if dashboard_id is not None:
                # From original resource Dashboard file resolve the datasSetId
                resourceFileDashboard = readFromOriginResourceFile('dashboards',dashboard_id , masked_origin_aws_account_id)
                originalDashboard = resourceFileDashboard[0]
                data_set_arns = glom(originalDashboard,'DescribeDashboard.Dashboard.Version.DataSetArns')
                # TODO: Allow resolve all datasets
                data_set_id = extract_id_from_arn(data_set_arns[0])
                linkEntities = glom(originalDashboard,'DescribeDashboard.Dashboard.LinkEntities')
                # TODO: Allow resolve all analisys
                if linkEntities is not None:
                    analysis_id = extract_id_from_arn(linkEntities[0])

            elif analysis_id is not None:
                # From original resource Dashboard file resolve the datasSetId
                camelOriginalResource = readFromOriginResourceFile('analyses',analysis_id , masked_origin_aws_account_id)[1]
                data_set_arn = camelOriginalResource['describeAnalysis']['analysis']['dataSetArns'][0] # type: ignore
                data_set_id = extract_id_from_arn(data_set_arn)

            # From datasSetId get the original resource DataSete file and resolve its DataSourceId
            camDataSetOriginalResource = readFromOriginResourceFile('data-sets', data_set_id, masked_origin_aws_account_id)[1]
            data_source_arns = find_all_values_iterative(camDataSetOriginalResource['describeDataSet'], 'dataSourceArn')
            data_source_id = extract_id_from_arn(data_source_arns[0])
        
        if data_source_id:
            params_file = self.node.try_get_context("params")
            file_params = self.read_params_file(params_file)
            self.define_parameters(file_params)

        if data_set_id:
            dataset_params = self.node.try_get_context("dataset_params")
            dataset_params_files = self.read_params_file(dataset_params)
            self.define_parameters(dataset_params_files)

        if analysis_id:
            analysis_params = self.node.try_get_context("analysis_params")
            analysis_params_files = self.read_params_file(analysis_params)
            self.define_parameters(analysis_params_files)

        if dashboard_id:
            dashboard_params = self.node.try_get_context("dashboard_params")
            dashboard_params_files = self.read_params_file(dashboard_params)
            self.define_parameters(dashboard_params_files)

        ######################################################
        # Creates An Cloudformation file with: 
        if data_source_id is not None:
            data_source_01 = createDataSource( self, datasource_name="AthenaDataSource01" )
        if data_set_id is not None:
            data_set_01 = createDataSet(self, originDatasetId=data_set_id, dataset_name="AthenaDataSetTable01", dataSource=data_source_01)
        if dashboard_id is not None:
            dashboard1 = createDashboard(self, dashboard_name="QuickSightDashboard01", dataSet=data_set_01)
        if analysis_id is not None:
            analysis01 = createAnalysis(self, analysis_id=analysis_id, analysis_name="QuickSightAnalysis01", dataSet=data_set_01)
            
        ######################################################

    def read_params_file(self, params_file):
        with open(params_file) as f:
            data = yaml.load(f, Loader=SafeLoader)
            return data

    def define_parameters(self, data):
        for key, value in data.items():
            params = {
                'type': value['Type'],
                'description': value['Description']
            }

            # if default value exist, add it to the params
            if 'Default' in value:
                params['default'] = value['Default']

            # if allowed values exist, add it to the params
            if 'AllowedValues' in value:
                params['allowed_values'] = value['AllowedValues']

            self.configParams[key] = CfnParameter(
                self,
                key,
                **params
            ) # IMPLEMENTACION: self.configParams['AthenaDataSourceName'].value_as_string