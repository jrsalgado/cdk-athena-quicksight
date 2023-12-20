import os
from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_quicksight as quicksight,
    aws_athena as athena
)
from constructs import Construct

APPLICATION = "cdk-quicksight-dataset-athena"
TAGS = {
    "application": APPLICATION,
}
BUCKET_NAME = os.getenv("BUCKET_NAME")
QUICKSIGHT_USERNAME = os.getenv("QUICKSIGHT_USERNAME")

class QsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        bucket_name = "mybucket"
        qs_username = "jayro"
        athena_database_name = "santander"
        tags = TAGS
        # AWS defined service role name
        qs_service_role_names = [
            "aws-quicksight-service-role-v0",
            "aws-quicksight-s3-consumers-role-v0",
        ]

        athena_output_prefix = "athena-results"
        qs_managed_policy = iam.CfnManagedPolicy(
            self,
            "QuickSightPolicy",
            managed_policy_name="QuickSightDemoAthenaS3Policy",
            policy_document=dict(
                Statement=[
                    dict(
                        Action=["s3:ListAllMyBuckets"],
                        Effect="Allow",
                        Resource=["arn:aws:s3:::*"],
                    ),
                    dict(
                        Action=["s3:ListBucket"],
                        Effect="Allow",
                        Resource=[
                            f"arn:aws:s3:::{bucket_name}",
                        ],
                    ),
                    dict(
                        Action=[
                            "s3:GetObject",
                            "s3:List*",
                        ],
                        Effect="Allow",
                        Resource=[
                            f"arn:aws:s3:::{bucket_name}/tables/*",
                        ],
                    ),
                    dict(
                        Action=[
                            "s3:GetObject",
                            "s3:List*",
                            "s3:AbortMultipartUpload",
                            "s3:PutObject",
                        ],
                        Effect="Allow",
                        Resource=[
                            f"arn:aws:s3:::{bucket_name}/{athena_output_prefix}/*",
                        ],
                    ),
                ],
                Version="2012-10-17",
            ),
            roles=qs_service_role_names,
        )

        qs_principal_arn = f"arn:aws:quicksight:{self.region}:{self.account}:user/default/{qs_username}"

        qs_data_source_permissions = [
            quicksight.CfnDataSource.ResourcePermissionProperty(
                principal=qs_principal_arn,
                actions=[
                    "quicksight:DescribeDataSource",
                    "quicksight:DescribeDataSourcePermissions",
                    "quicksight:PassDataSource",
                ],
            ),
        ]

        qs_dataset_permissions = [
            quicksight.CfnDataSet.ResourcePermissionProperty(
                principal=qs_principal_arn,
                actions=[
                    "quicksight:DescribeDataSet",
                    "quicksight:DescribeDataSetPermissions",
                    "quicksight:PassDataSet",
                    "quicksight:DescribeIngestion",
                    "quicksight:ListIngestions",
                ],
            )
        ]

        athena_workgroup_name = f"athena-santander-wg"
        athena_workgroup = athena.CfnWorkGroup(
            self,
            "Workgroup",
            name=athena_workgroup_name,
            work_group_configuration=athena.CfnWorkGroup.WorkGroupConfigurationProperty(
                result_configuration=athena.CfnWorkGroup.ResultConfigurationProperty(
                    output_location=f"s3://{bucket_name}/{athena_output_prefix}/",
                    encryption_configuration=athena.CfnWorkGroup.EncryptionConfigurationProperty(
                        encryption_option="SSE_S3"
                    ),
                )
            ),
            recursive_delete_option=True,
        )

        qs_principal_arn = f"arn:aws:quicksight:{self.region}:{self.account}:user/default/{qs_username}"

        qs_athena_data_source_name = "athena-santander"
        qs_athena_data_source = quicksight.CfnDataSource(
            self,
            "AthenaDataSource",
            name=qs_athena_data_source_name,
            data_source_parameters=quicksight.CfnDataSource.DataSourceParametersProperty(
                athena_parameters=quicksight.CfnDataSource.AthenaParametersProperty(
                    work_group=athena_workgroup_name
                )
            ),
            type="ATHENA",
            aws_account_id=self.account,
            data_source_id=qs_athena_data_source_name,
            ssl_properties=quicksight.CfnDataSource.SslPropertiesProperty(
                disable_ssl=False
            ),
            permissions=qs_data_source_permissions,
        )

        qs_athena_data_source.add_depends_on(qs_managed_policy)

        qs_athena_dataset_santander_physical_table = (
            quicksight.CfnDataSet.PhysicalTableProperty(
                relational_table=quicksight.CfnDataSet.RelationalTableProperty(
                    data_source_arn=qs_athena_data_source.attr_arn,
                    input_columns=[
                        quicksight.CfnDataSet.InputColumnProperty(
                            name="Survived", type="INTEGER"
                        ),
                        quicksight.CfnDataSet.InputColumnProperty(
                            name="Pclass", type="INTEGER"
                        ),
                        quicksight.CfnDataSet.InputColumnProperty(
                            name="Name", type="STRING"
                        ),
                        quicksight.CfnDataSet.InputColumnProperty(
                            name="Sex", type="STRING"
                        ),
                        quicksight.CfnDataSet.InputColumnProperty(
                            name="Age", type="DECIMAL"
                        ),
                        quicksight.CfnDataSet.InputColumnProperty(
                            name="Siblings/Spouses Aboard", type="INTEGER"
                        ),
                        quicksight.CfnDataSet.InputColumnProperty(
                            name="Parents/Children Aboard", type="INTEGER"
                        ),
                        quicksight.CfnDataSet.InputColumnProperty(
                            name="Fare", type="DECIMAL"
                        ),
                    ],
                    catalog="AWSDataCatalog",
                    schema=athena_database_name,
                    name="santander",
                )
            )
        )

        qs_import_mode = "SPICE"
        qs_dataset_santander_name = "athena-santander-ds"
        qs_athena_dataset_santander = quicksight.CfnDataSet(
            self,
            f"Dataset-athena-santander",
            import_mode=qs_import_mode,
            name=qs_dataset_santander_name,
            aws_account_id=self.account,
            data_set_id=qs_dataset_santander_name,
            physical_table_map={
                "athena-santander-table": qs_athena_dataset_santander_physical_table
            },
            permissions=qs_dataset_permissions,
        )

        sql_statement = f"""
            SELECT
                Survived,
                Name,
                Sex,
                "Siblings/Spouses Aboard"+"Parents/Children Aboard" AS Related
            FROM {athena_database_name}.santander
        """
        qs_athena_dataset_santander_physical_table_sql = (
            quicksight.CfnDataSet.PhysicalTableProperty(
                custom_sql=quicksight.CfnDataSet.CustomSqlProperty(
                    name="santander-sql",
                    data_source_arn=qs_athena_data_source.attr_arn,
                    sql_query=sql_statement,
                    columns=[
                        quicksight.CfnDataSet.InputColumnProperty(
                            name="Survived", type="INTEGER"
                        ),
                        quicksight.CfnDataSet.InputColumnProperty(
                            name="Name", type="STRING"
                        ),
                        quicksight.CfnDataSet.InputColumnProperty(
                            name="Sex", type="STRING"
                        ),
                        quicksight.CfnDataSet.InputColumnProperty(
                            name="Related", type="INTEGER"
                        ),
                    ],
                ),
            )
        )

        qs_dataset_santander_sql_name = "athena-santander-sql-ds"
        qs_athena_dataset_santander_sql = quicksight.CfnDataSet(
            self,
            f"Dataset-athena-santander-sql",
            import_mode=qs_import_mode,
            name=qs_dataset_santander_sql_name,
            aws_account_id=self.account,
            data_set_id=qs_dataset_santander_sql_name,
            physical_table_map={
                "athena-santander-table-sql": qs_athena_dataset_santander_physical_table_sql
            },
            permissions=qs_dataset_permissions,
        )

        ### Set tags
        if tags:
            for key, value in tags.items():
                self.tags.set_tag(key, value)


# Athena Wg -> QS-DS -> QS-Dset -> QS-Template -> QS-Dashboard
### input 


### Process


### Output







