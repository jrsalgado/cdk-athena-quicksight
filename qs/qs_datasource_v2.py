import humps
import yaml
from yaml.loader import SafeLoader
from aws_cdk import aws_quicksight as quicksight
from aws_cdk import Stack
from aws_cdk import Fn, Aws
from glom import glom, assign

def createDataSource( stack: Stack, datasource_name: str, param_id: str,param_name: str, origin_resource ):
    aws_account_id = Aws.ACCOUNT_ID
    
    with open("base_templates/data-source.yaml") as f:
        common_base = yaml.load(f, Loader=SafeLoader)
    
    # Add params 
    # addTemplateParam(stack)
    
    # set DataSourceParameters
    data_source_parameters = glom(origin_resource,'DescribeDataSource.DataSource.DataSourceParameters')
    assign(data_source_parameters,'AthenaParameters.WorkGroup', stack.configParams['DataSourceAthenaWorkGroup01'].value_as_string )
    
    # set Permissions
    datasourcePrincipal= Fn.sub(
        'arn:aws:quicksight:${aws_region}:${aws_account}:${principalType}/${qsNamespace}/${user}',
        {
            'aws_account': Aws.ACCOUNT_ID,
            'aws_region': Aws.REGION,
            'principalType': stack.configParams['QuickSightPrincipalType'].value_as_string, # type: ignore
            'user': stack.configParams['QuickSightUsername'].value_as_string, # type: ignore
            'qsNamespace': stack.configParams['QuickSightNamespace'].value_as_string, # type: ignore
        }
    )
    permissions = glom(common_base, 'BaseDataSource.Properties.Permissions')
    for i in range(len(permissions)):
        assign(permissions,f'{i}.Principal', datasourcePrincipal )

    # Set SSL Properties
    #ssl_properties = glom(origin_resource,'DescribeDataSource.DataSource.SslProperties')
    #print(humps.camelize(ssl_properties))
    ssl_properties = quicksight.CfnDataSource.SslPropertiesProperty(
        disable_ssl = False
    )
    
    # Set type
    datasourcetype = glom(origin_resource,'DescribeDataSource.DataSource.Type')

    quicksightDataSource =  quicksight.CfnDataSource(
        stack,
        id = datasource_name,
        aws_account_id = aws_account_id,
        data_source_id = stack.configParams[param_id].value_as_string,
        name           = f"{stack.configParams['Environment'].value_as_string}-{stack.configParams[param_name].value_as_string}", # type: ignore
        type           = datasourcetype,
        data_source_parameters= humps.camelize(data_source_parameters),
        permissions    = humps.camelize(permissions),
        ssl_properties = ssl_properties
    )

    return quicksightDataSource


#def addTemplateParam(stack):
#    param_id=f'DataSource{datasource_name}'
#    if not parameter_exists(param_id):
#        self.configParams[param_id] = CfnParameter(
#            self,
#            param_id,
#            type= 'String',
#            description= f'Data Source Id - {datasource_name}',
#            default= datasource_id
#            )