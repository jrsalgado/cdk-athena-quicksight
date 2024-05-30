from aws_cdk import CfnParameter, Stack
from constructs import Construct
import yaml
from yaml.loader import SafeLoader
from glom import glom
from qs.utils import mask_aws_account_id, readOriginResourceFile
from qs.utils import find_all_values_iterative, extract_id_from_arn
# Quicksight Resources
from qs.qs_datasource_v2 import createDataSource
from qs.qs_dataset_v2 import createDataSet
from qs.qs_dashboard import createDashboard
from qs.qs_analysis import createAnalysis

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
        #print(self._datasources)
        #print(self._datasets)
        #dashboard1 = createDashboard(self, dashboard_name="QuickSightDashboard01", dataSet=data_set_01)
        pass

    def create_dataset(self, datasetarn):
        datasetid = extract_id_from_arn(datasetarn)
        oResource = readOriginResourceFile('data-sets', datasetid, self.masked_origin_aws_account_id)
        datasourcearns = find_all_values_iterative(oResource.get('DescribeDataSet'),'DataSourceArn')
        for _ , datasourcearn in enumerate(datasourcearns):
            self.create_datasource(datasourcearn)
        dataset_name = glom(oResource,'DescribeDataSet.DataSet.Name')
        #dataset = createDataSet(self, originDatasetId=datasetid, dataset_name=dataset_name)
        #self._datasets[datasetid] = dataset
        self._datasets[datasetid] = dataset_name
        return oResource

    def create_datasource(self, datasourcearn):
        datasourceid = extract_id_from_arn(datasourcearn)
        if datasourceid in self._datasources:
            return
        oResource = readOriginResourceFile('data-sources', datasourceid, self.masked_origin_aws_account_id)
        datasource_name = glom(oResource,'DescribeDataSource.DataSource.Name')
        datasource_id = glom(oResource,'DescribeDataSource.DataSource.DataSourceId')

        def parameter_exists(parameter: str) -> bool:
            try:
                self.node.find_child(parameter)
                return True
            except:
                return False
    
        param_id=f'DataSource{datasource_name}'
        if not parameter_exists(param_id):
            self.configParams[param_id] = CfnParameter(
                self,
                param_id,
                type= 'String',
                description= f'Data Source Id - {datasource_name}',
                default= datasource_id
                )

        datasource = createDataSource(self, datasource_name=datasource_name, param_id = param_id, origin_resource = oResource)
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