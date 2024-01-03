import os, yaml
from yaml.loader import SafeLoader
from constructs import Construct
from aws_cdk import (
    CfnParameter,
    Stack,
    aws_iam as iam,
    aws_quicksight as quicksight,
    aws_athena as athena,
)

###########################################################
from qs.qs_datasource import createDataSource
from qs.qs_dataset import createDataSet
from qs.qs_dashboard import createDashboard, createNoDepsDashboard
###########################################################

class QsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        params_file = self.node.try_get_context("params")
        file_params = self.read_params_file(params_file)
        self.define_parameters(file_params)

        ######################################################

        # TODO: refactor configparams to object instead map
        # data_source_01 = createDataSource( self, datasource_name="AthenaDataSource01" )
        # data_set_01 = createDataSet(self, dataset_name="AthenaDataSetTable01", dataSource=data_source_01)
        # dashboard1 = createDashboard(self, dashboard_name="QuickSightDashboard01", dataset_object=data_set_01)
            
        ######################################################

        dashboardNoDeps = createNoDepsDashboard(self)


    def read_params_file(self, params_file):
        with open(params_file) as f:
            data = yaml.load(f, Loader=SafeLoader)
            return data

    def define_parameters(self, data):
        self.configParams = {}
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
