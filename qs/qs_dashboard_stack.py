from aws_cdk import CfnParameter, Stack
from constructs import Construct
import yaml
import random
from yaml.loader import SafeLoader
from glom import glom
from qs.utils import mask_aws_account_id, readOriginResourceFile
from qs.utils import find_all_values_iterative, extract_id_from_arn
# Quicksight Resources
from qs.qs_datasource_v2 import createDataSource
from qs.qs_dataset_v2 import createDataSet
from qs.qs_dashboard_v2 import createDashboard
#from qs.qs_analysis import createAnalysis

class QsDashboardStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id)
        self.configParams = {}
        # Dependencies Setup
        self.dashboard_id = kwargs.get('dashboard_id', None)
        self.origin_account_id = kwargs.get('origin_account_id', None)
        self.masked_origin_aws_account_id = mask_aws_account_id(self.origin_account_id)
        self.params_setup()

        # Extract dependencies
        oResource = readOriginResourceFile('dashboards', self.dashboard_id, self.masked_origin_aws_account_id)
        self._datasets = {}
        self._datasources = {}
        self.create_dashboard(oResource)

        #dashboard1 = createDashboard(self, dashboard_name="QuickSightDashboard01", dataSet=data_set_01)


    def create_dashboard(self, oResource):
        datasetarns=glom(oResource,'DescribeDashboard.Dashboard.Version.DataSetArns')
        for _ , datasetarn in enumerate(datasetarns):
            self.create_dataset(datasetarn)
        
        dashboard_name = glom(oResource,'DescribeDashboard.Dashboard.Name')
        param_id= f'DashboardId'
        dashboard_arn = glom(oResource,'DescribeDashboard.Dashboard.Arn')
        dashboard_id = extract_id_from_arn(dashboard_arn)
        
        idpart1 = random.randint(10**7, 10**8 - 1)
        idpart2 = random.randint(10**3, 10**4 - 1)
        if not self.parameter_exists(param_id):
            self.configParams[param_id] = CfnParameter(
                self,
                param_id,
                type= 'String',
                description= f'Dashboard id - {dashboard_name}',
                default= f'{idpart1}-{idpart2}'
                )
        if not self.parameter_exists('DashboardName'):
            self.configParams['DashboardName'] = CfnParameter(
                self,
                'DashboardName',
                type= 'String',
                description= f'Dashboard Name - {dashboard_name}',
                default= f'{dashboard_name}-{idpart2}'
                )
        
        dashboard1 = createDashboard(self, dashboard_name=dashboard_name, param_id = param_id, origin_resource = oResource)
        pass

    def create_dataset(self, datasetarn):
        datasetid = extract_id_from_arn(datasetarn)
        oResource = readOriginResourceFile('data-sets', datasetid, self.masked_origin_aws_account_id)
        datasourcearns = find_all_values_iterative(oResource.get('DescribeDataSet'),'DataSourceArn')
        for _ , datasourcearn in enumerate(datasourcearns):
            self.create_datasource(datasourcearn)
                
        idpart1 = random.randint(10**7, 10**8 - 1)
        idpart2 = random.randint(10**3, 10**4 - 1)

        dataset_name = glom(oResource,'DescribeDataSet.DataSet.Name')
        param_id=f'DataSetId{dataset_name}'
        if not self.parameter_exists(param_id):
            self.configParams[param_id] = CfnParameter(
                self,
                param_id,
                type= 'String',
                description= f'Original Data Set Id - {datasetid}',
                default= f'{idpart1}-{idpart2}'
                )

        param_name=f'DataSetName{dataset_name}'
        if not self.parameter_exists(param_name):
            self.configParams[param_name] = CfnParameter(
                self,
                param_name,
                type= 'String',
                description= f'Original Data Set Name - {dataset_name}',
                default= f'{dataset_name}-{idpart2}'
                )

        dataset = createDataSet(self, originDatasetId=datasetid, param_id=param_id, param_name=param_name, origin_resource = oResource)
        self._datasets[datasetid] = dataset
        return oResource

    def create_datasource(self, datasourcearn):
        datasourceid = extract_id_from_arn(datasourcearn)
        if datasourceid in self._datasources:
            return
        oResource = readOriginResourceFile('data-sources', datasourceid, self.masked_origin_aws_account_id)
        datasource_name = glom(oResource,'DescribeDataSource.DataSource.Name')
        datasource_id = glom(oResource,'DescribeDataSource.DataSource.DataSourceId')
        
        idpart1 = random.randint(10**7, 10**8 - 1)
        idpart2 = random.randint(10**3, 10**4 - 1)
        param_id=f'DataSourceId{datasource_name}'
        if not self.parameter_exists(param_id):
            self.configParams[param_id] = CfnParameter(
                self,
                param_id,
                type= 'String',
                description= f'Original Data Source Id - {datasource_id}',
                default= f'{idpart1}-{idpart2}'
                )

        param_name=f'DataSourceName{datasource_name}'
        if not self.parameter_exists(param_name):
            self.configParams[param_name] = CfnParameter(
                self,
                param_name,
                type= 'String',
                description= f'Data Source Name - {datasource_name}',
                default= f'{datasource_name}-{idpart2}'
                )

        datasource = createDataSource(self, datasource_name=datasource_name, param_id = param_id, param_name= param_name, origin_resource = oResource)
        self._datasources[datasourceid] = datasource
        pass

    def parameter_exists(self, parameter: str) -> bool:
        try:
            self.node.find_child(parameter)
            return True
        except:
            return False

    def read_params_file(self, params_file):
        with open(params_file) as f:
            data = yaml.load(f, Loader=SafeLoader)
            if data is None:
                data = {}
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

    def params_setup(self):
        # Params setup
        general_params = self.node.try_get_context("general_params")
        general_params_file = self.read_params_file(general_params)
        self.define_parameters(general_params_file)

        # Dashboard params setup
        dashboard_params = self.node.try_get_context("dashboard_params")
        dashboard_params_files = self.read_params_file(dashboard_params)
        self.define_parameters(dashboard_params_files)
        
        # Datasource params setup
        params_file = self.node.try_get_context("params")
        file_params = self.read_params_file(params_file)
        self.define_parameters(file_params)
        
        # Dataset params setup
        dataset_params = self.node.try_get_context("dataset_params")
        dataset_params_files = self.read_params_file(dataset_params)
        self.define_parameters(dataset_params_files)
        pass