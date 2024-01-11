import yaml
from yaml.loader import SafeLoader
from constructs import Construct
from aws_cdk import (
    CfnParameter,
    Stack,
)
from os import getenv

###########################################################
from qs.qs_datasource import createDataSource
from qs.qs_dataset import createDataSet
from qs.qs_dashboard import createDashboard, createNoDepsDashboard
###########################################################

class QsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.configParams = {}

        general_params = self.node.try_get_context("general_params")
        general_params_file = self.read_params_file(general_params)
        self.define_parameters(general_params_file)

        if getenv('ORIGIN_DATASOURCE_ID'):
            params_file = self.node.try_get_context("params")
            file_params = self.read_params_file(params_file)
            self.define_parameters(file_params)

        if getenv('ORIGIN_DATASET_ID'):
            dataset_params = self.node.try_get_context("dataset_params")
            dataset_params_files = self.read_params_file(dataset_params)
            self.define_parameters(dataset_params_files)

        if getenv('ORIGIN_DASHBOARD_ID'):
            dashboard_params = self.node.try_get_context("dashboard_params")
            dashboard_params_files = self.read_params_file(dashboard_params)
            self.define_parameters(dashboard_params_files)

        ######################################################
        # Creates An Cloudformation file with: 
        # From already created Quicksight resources able to be deployed on any account
        if getenv('ORIGIN_DATASOURCE_ID'):
            data_source_01 = createDataSource( self, datasource_name="AthenaDataSource01" )
        if getenv('ORIGIN_DATASET_ID'):
            data_set_01 = createDataSet(self, dataset_name="AthenaDataSetTable01", dataSource=data_source_01)
        if getenv('ORIGIN_DASHBOARD_ID'):
            dashboard1 = createDashboard(self, dashboard_name="QuickSightDashboard01", dataset_object=data_set_01)
            
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
