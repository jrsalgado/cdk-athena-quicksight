from aws_cdk import (
    aws_quicksight as quicksight,
    core as cdk
)

class MyStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        quicksightdatasource = quicksight.CfnDataSource(
            self,
            "QuickSightDataSource",
            data_source_id="fb2b417e-7e9c-4095-8b49-0da454bd8ee5",
            name="Web and Social Media Analytics",
            aws_account_id="064855577434",
            type="S3",
            data_source_parameters={
                "s3_parameters": {
                    "manifest_file_location": {
                        "bucket": "spaceneedle-samplefiles.prod.us-east-1",
                        "key": "marketing/manifest.json"
                    }
                }
            }
        )

        quicksightdatasource2 = quicksight.CfnDataSource(
            self,
            "QuickSightDataSource2",
            data_source_id="b8cd5dce-827f-4e7e-a25b-7fa22223b15a",
            name="Business Review",
            aws_account_id="064855577434",
            type="S3",
            data_source_parameters={
                "s3_parameters": {
                    "manifest_file_location": {
                        "bucket": "spaceneedle-samplefiles.prod.us-east-1",
                        "key": "revenue/manifest.json"
                    }
                }
            }
        )

        quicksightdatasource3 = quicksight.CfnDataSource(
            self,
            "QuickSightDataSource3",
            data_source_id="d203fefb-99ab-4c9b-bd68-4f2af9be9bdc",
            name="Business Review",
            aws_account_id="064855577434",
            type="S3",
            data_source_parameters={
                "s3_parameters": {
                    "manifest_file_location": {
                        "bucket": "spaceneedle-samplefiles.prod.us-east-1",
                        "key": "revenue/manifest.json"
                    }
                }
            }
        )

        quicksightdatasource4 = quicksight.CfnDataSource(
            self,
            "QuickSightDataSource4",
            data_source_id="27cd8539-c183-4c99-b842-dd91c8d1e250",
            name="Sales Pipeline",
            aws_account_id="064855577434",
            type="S3",
            data_source_parameters={
                "s3_parameters": {
                    "manifest_file_location": {
                        "bucket": "spaceneedle-samplefiles.prod.us-east-1",
                        "key": "sales/manifest.json"
                    }
                }
            }
        )

        quicksightdatasource5 = quicksight.CfnDataSource(
            self,
            "QuickSightDataSource5",
            data_source_id="d7fe19c1-ff47-4b26-a860-c353a6f57ca2",
            name="People Overview",
            aws_account_id="064855577434",
            type="S3",
            data_source_parameters={
                "s3_parameters": {
                    "manifest_file_location": {
                        "bucket": "spaceneedle-samplefiles.prod.us-east-1",
                        "key": "hr/manifest.json"
                    }
                }
            }
        )

        quicksightdatasource6 = quicksight.CfnDataSource(
            self,
            "QuickSightDataSource6",
            data_source_id="f8147bfc-3e26-4f21-93bb-83fc5bca18ea",
            name="Sales Pipeline",
            aws_account_id="064855577434",
            type="S3",
            data_source_parameters={
                "s3_parameters": {
                    "manifest_file_location": {
                        "bucket": "spaceneedle-samplefiles.prod.us-east-1",
                        "key": "sales/manifest.json"
                    }
                }
            }
        )

        quicksightdatasource7 = quicksight.CfnDataSource(
            self,
            "QuickSightDataSource7",
            data_source_id="be540765-f31a-4088-9e3b-d035ae333b48",
            name="Web and Social Media Analytics",
            aws_account_id="064855577434",
            type="S3",
            data_source_parameters={
                "s3_parameters": {
                    "manifest_file_location": {
                        "bucket": "spaceneedle-samplefiles.prod.us-east-1",
                        "key": "marketing/manifest.json"
                    }
                }
            }
        )

        quicksightdatasource8 = quicksight.CfnDataSource(
            self,
            "QuickSightDataSource8",
            data_source_id="04d67882-9620-4501-99c9-ce83f25bf1df",
            name="People Overview",
            aws_account_id="064855577434",
            type="S3",
            data_source_parameters={
                "s3_parameters": {
                    "manifest_file_location": {
                        "bucket": "spaceneedle-samplefiles.prod.us-east-1",
                        "key": "hr/manifest.json"
                    }
                }
            }
        )

        quicksightdataset = quicksight.CfnDataSet(
            self,
            "QuickSightDataSet",
            data_set_id="0da2b670-2b26-4a92-9c85-f0ba478995c5",
            name="Business Review",
            aws_account_id="064855577434",
            physical_table_map={
                "s3_physical_table": {
                    "s3_source": {
                        "data_source_arn": quicksightdatasource2.attr_arn,
                        "upload_settings": {
                            "format": "CSV",
                            "start_from_row": 1,
                            "contains_header": True,
                            "text_qualifier": "DOUBLE_QUOTE",
                            "delimiter": ","
                        },
                        "input_columns": [
                            {
                                "name": "ColumnId-1",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-2",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-3",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-4",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-5",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-6",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-7",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-8",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-9",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-10",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-11",
                                "type": "STRING"
                            }
                        ]
                    }
                }
            },
            logical_table_map={
                "s3_physical_table": {
                    "alias": "Group 1",
                    "data_transforms": [
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-2",
                                "new_column_name": "Customer ID"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-3",
                                "new_column_name": "Customer Name"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-1",
                                "new_column_name": "Date"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-6",
                                "new_column_name": "Service Line"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-11",
                                "new_column_name": "Distinct ID"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-7",
                                "new_column_name": "Revenue Goal"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-4",
                                "new_column_name": "Customer Region"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-5",
                                "new_column_name": "Segment"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-10",
                                "new_column_name": "Channel"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-8",
                                "new_column_name": "Billed Amount"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-9",
                                "new_column_name": "Cost"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Cost",
                                "new_column_type": "DECIMAL",
                                "sub_type": "FLOAT"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Billed Amount",
                                "new_column_type": "DECIMAL",
                                "sub_type": "FLOAT"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Revenue Goal",
                                "new_column_type": "DECIMAL",
                                "sub_type": "FLOAT"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Distinct ID",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Date",
                                "new_column_type": "DATETIME",
                                "format": "M/d/yyyy"
                            }
                        },
                        {
                            "tag_column_operation": {
                                "column_name": "Customer Region",
                                "tags": [
                                    {
                                        "column_geographic_role": "STATE"
                                    }
                                ]
                            }
                        }
                    ],
                    "source": {
                        "physical_table_id": "s3PhysicalTable"
                    }
                }
            },
            import_mode="SPICE",
            permissions=[
                {
                    "principal": "arn:aws:quicksight:us-east-1:064855577434:user/default/boss",
                    "actions": [
                        "quicksight:DeleteDataSet",
                        "quicksight:UpdateDataSetPermissions",
                        "quicksight:PutDataSetRefreshProperties",
                        "quicksight:CreateRefreshSchedule",
                        "quicksight:CancelIngestion",
                        "quicksight:UpdateRefreshSchedule",
                        "quicksight:DeleteRefreshSchedule",
                        "quicksight:PassDataSet",
                        "quicksight:ListRefreshSchedules",
                        "quicksight:DescribeDataSetRefreshProperties",
                        "quicksight:DescribeDataSet",
                        "quicksight:CreateIngestion",
                        "quicksight:DescribeRefreshSchedule",
                        "quicksight:ListIngestions",
                        "quicksight:DescribeDataSetPermissions",
                        "quicksight:UpdateDataSet",
                        "quicksight:DeleteDataSetRefreshProperties",
                        "quicksight:DescribeIngestion"
                    ]
                }
            ]
        )

        quicksightdataset2 = quicksight.CfnDataSet(
            self,
            "QuickSightDataSet2",
            data_set_id="44eca1ec-3c9d-4ffe-8ad9-e31e8f9cca4e",
            name="People Overview",
            aws_account_id="064855577434",
            physical_table_map={
                "s3_physical_table": {
                    "s3_source": {
                        "data_source_arn": quicksightdatasource5.attr_arn,
                        "upload_settings": {
                            "format": "CSV",
                            "start_from_row": 1,
                            "contains_header": True,
                            "text_qualifier": "DOUBLE_QUOTE",
                            "delimiter": ","
                        },
                        "input_columns": [
                            {
                                "name": "ColumnId-1",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-2",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-3",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-4",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-5",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-6",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-7",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-8",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-9",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-10",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-11",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-12",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-13",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-14",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-15",
                                "type": "STRING"
                            }
                        ]
                    }
                }
            },
            logical_table_map={
                "s3_physical_table": {
                    "alias": "Group 1",
                    "data_transforms": [
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-2",
                                "new_column_name": "Employee Name"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-3",
                                "new_column_name": "Employee ID"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-1",
                                "new_column_name": "Date"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-12",
                                "new_column_name": "Job Family"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-6",
                                "new_column_name": "Date of Birth"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-11",
                                "new_column_name": "Business Function"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-7",
                                "new_column_name": "Gender"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-14",
                                "new_column_name": "Notes"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-4",
                                "new_column_name": "Tenure"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-13",
                                "new_column_name": "Job Level"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-5",
                                "new_column_name": "Monthly Compensation"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-10",
                                "new_column_name": "Region"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-8",
                                "new_column_name": "Education"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-9",
                                "new_column_name": "Event Type"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-15",
                                "new_column_name": "isUnique"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Monthly Compensation",
                                "new_column_type": "DECIMAL",
                                "sub_type": "FLOAT"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Tenure",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Date of Birth",
                                "new_column_type": "DATETIME",
                                "format": "yyyy-MM-dd"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Date",
                                "new_column_type": "DATETIME",
                                "format": "yyyy-MM-dd"
                            }
                        },
                        {
                            "tag_column_operation": {
                                "column_name": "Region",
                                "tags": [
                                    {
                                        "column_geographic_role": "STATE"
                                    }
                                ]
                            }
                        }
                    ],
                    "source": {
                        "physical_table_id": "s3PhysicalTable"
                    }
                }
            },
            import_mode="SPICE",
            permissions=[
                {
                    "principal": "arn:aws:quicksight:us-east-1:064855577434:user/default/boss",
                    "actions": [
                        "quicksight:DeleteDataSet",
                        "quicksight:UpdateDataSetPermissions",
                        "quicksight:PutDataSetRefreshProperties",
                        "quicksight:CreateRefreshSchedule",
                        "quicksight:CancelIngestion",
                        "quicksight:PassDataSet",
                        "quicksight:ListRefreshSchedules",
                        "quicksight:DeleteRefreshSchedule",
                        "quicksight:UpdateRefreshSchedule",
                        "quicksight:DescribeDataSetRefreshProperties",
                        "quicksight:DescribeDataSet",
                        "quicksight:CreateIngestion",
                        "quicksight:DescribeRefreshSchedule",
                        "quicksight:ListIngestions",
                        "quicksight:DescribeDataSetPermissions",
                        "quicksight:UpdateDataSet",
                        "quicksight:DeleteDataSetRefreshProperties",
                        "quicksight:DescribeIngestion"
                    ]
                }
            ]
        )

        quicksightdataset3 = quicksight.CfnDataSet(
            self,
            "QuickSightDataSet3",
            data_set_id="a4aeea4c-2d90-466f-a4ec-758679ece587",
            name="Sales Pipeline",
            aws_account_id="064855577434",
            physical_table_map={
                "s3_physical_table": {
                    "s3_source": {
                        "data_source_arn": quicksightdatasource4.attr_arn,
                        "upload_settings": {
                            "format": "CSV",
                            "start_from_row": 1,
                            "contains_header": True,
                            "text_qualifier": "DOUBLE_QUOTE",
                            "delimiter": ","
                        },
                        "input_columns": [
                            {
                                "name": "ColumnId-1",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-2",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-3",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-4",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-5",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-6",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-7",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-8",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-9",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-10",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-11",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-12",
                                "type": "STRING"
                            }
                        ]
                    }
                }
            },
            logical_table_map={
                "s3_physical_table": {
                    "alias": "Group 1",
                    "data_transforms": [
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-2",
                                "new_column_name": "Salesperson"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-3",
                                "new_column_name": "Lead Name"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-1",
                                "new_column_name": "Date"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-12",
                                "new_column_name": "IsLatest"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-6",
                                "new_column_name": "Target Close"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-11",
                                "new_column_name": "ActiveItem"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-7",
                                "new_column_name": "Forecasted Monthly Revenue"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-4",
                                "new_column_name": "Segment"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-5",
                                "new_column_name": "Region"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-10",
                                "new_column_name": "Is Closed"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-8",
                                "new_column_name": "Opportunity Stage"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-9",
                                "new_column_name": "Weighted Revenue"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Weighted Revenue",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Forecasted Monthly Revenue",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Target Close",
                                "new_column_type": "DATETIME",
                                "format": "M/d/yyyy"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "IsLatest",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Date",
                                "new_column_type": "DATETIME",
                                "format": "M/d/yyyy"
                            }
                        },
                        {
                            "tag_column_operation": {
                                "column_name": "Region",
                                "tags": [
                                    {
                                        "column_geographic_role": "STATE"
                                    }
                                ]
                            }
                        }
                    ],
                    "source": {
                        "physical_table_id": "s3PhysicalTable"
                    }
                }
            },
            import_mode="SPICE",
            permissions=[
                {
                    "principal": "arn:aws:quicksight:us-east-1:064855577434:user/default/boss",
                    "actions": [
                        "quicksight:DeleteDataSet",
                        "quicksight:UpdateDataSetPermissions",
                        "quicksight:PutDataSetRefreshProperties",
                        "quicksight:CreateRefreshSchedule",
                        "quicksight:CancelIngestion",
                        "quicksight:ListRefreshSchedules",
                        "quicksight:PassDataSet",
                        "quicksight:DeleteRefreshSchedule",
                        "quicksight:UpdateRefreshSchedule",
                        "quicksight:DescribeDataSetRefreshProperties",
                        "quicksight:DescribeDataSet",
                        "quicksight:CreateIngestion",
                        "quicksight:DescribeRefreshSchedule",
                        "quicksight:ListIngestions",
                        "quicksight:DescribeDataSetPermissions",
                        "quicksight:UpdateDataSet",
                        "quicksight:DeleteDataSetRefreshProperties",
                        "quicksight:DescribeIngestion"
                    ]
                }
            ]
        )

        quicksightdataset4 = quicksight.CfnDataSet(
            self,
            "QuickSightDataSet4",
            data_set_id="180e00b8-a755-427c-a1c7-0951780cdf70",
            name="Web and Social Media Analytics",
            aws_account_id="064855577434",
            physical_table_map={
                "s3_physical_table": {
                    "s3_source": {
                        "data_source_arn": quicksightdatasource7.attr_arn,
                        "upload_settings": {
                            "format": "CSV",
                            "start_from_row": 1,
                            "contains_header": True,
                            "text_qualifier": "DOUBLE_QUOTE",
                            "delimiter": ","
                        },
                        "input_columns": [
                            {
                                "name": "ColumnId-1",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-2",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-3",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-4",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-5",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-6",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-7",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-8",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-9",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-10",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-11",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-12",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-13",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-14",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-15",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-16",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-17",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-18",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-19",
                                "type": "STRING"
                            }
                        ]
                    }
                }
            },
            logical_table_map={
                "s3_physical_table": {
                    "alias": "Group 1",
                    "data_transforms": [
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-2",
                                "new_column_name": "New visitors SEO"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-3",
                                "new_column_name": "New visitors CPC"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-1",
                                "new_column_name": "Date"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-12",
                                "new_column_name": "Website Visits"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-6",
                                "new_column_name": "Twitter mentions"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-11",
                                "new_column_name": "Website Pageviews"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-7",
                                "new_column_name": "Twitter followers adds"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-14",
                                "new_column_name": "Mobile uniques"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-4",
                                "new_column_name": "New visitors Social Media"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-13",
                                "new_column_name": "Website Unique Visits"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-5",
                                "new_column_name": "Return visitors"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-10",
                                "new_column_name": "Mailing list cumulative"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-8",
                                "new_column_name": "Twitter followers cumulative"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-9",
                                "new_column_name": "Mailing list adds "
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-19",
                                "new_column_name": "Events"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-16",
                                "new_column_name": "Desktop uniques"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-15",
                                "new_column_name": "Tablet uniques"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-18",
                                "new_column_name": "Paid conversion"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-17",
                                "new_column_name": "Free sign up"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Free sign up",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Paid conversion",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Tablet uniques",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Desktop uniques",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Mailing list adds ",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Twitter followers cumulative",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Mailing list cumulative",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Return visitors",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Website Unique Visits",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "New visitors Social Media",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Mobile uniques",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Twitter followers adds",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Website Pageviews",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Twitter mentions",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Website Visits",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Date",
                                "new_column_type": "DATETIME",
                                "format": "M/d/yyyy"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "New visitors CPC",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "New visitors SEO",
                                "new_column_type": "INTEGER"
                            }
                        }
                    ],
                    "source": {
                        "physical_table_id": "s3PhysicalTable"
                    }
                }
            },
            import_mode="SPICE",
            permissions=[
                {
                    "principal": "arn:aws:quicksight:us-east-1:064855577434:user/default/boss",
                    "actions": [
                        "quicksight:DeleteDataSet",
                        "quicksight:UpdateDataSetPermissions",
                        "quicksight:PutDataSetRefreshProperties",
                        "quicksight:CreateRefreshSchedule",
                        "quicksight:CancelIngestion",
                        "quicksight:PassDataSet",
                        "quicksight:DeleteRefreshSchedule",
                        "quicksight:UpdateRefreshSchedule",
                        "quicksight:ListRefreshSchedules",
                        "quicksight:DescribeDataSetRefreshProperties",
                        "quicksight:DescribeDataSet",
                        "quicksight:CreateIngestion",
                        "quicksight:DescribeRefreshSchedule",
                        "quicksight:ListIngestions",
                        "quicksight:UpdateDataSet",
                        "quicksight:DescribeDataSetPermissions",
                        "quicksight:DeleteDataSetRefreshProperties",
                        "quicksight:DescribeIngestion"
                    ]
                }
            ]
        )

        quicksightdataset5 = quicksight.CfnDataSet(
            self,
            "QuickSightDataSet5",
            data_set_id="f66f2dea-7000-4d37-8bbb-da6b33329c33",
            name="People",
            aws_account_id="064855577434",
            physical_table_map={
                "s3_physical_table": {
                    "s3_source": {
                        "data_source_arn": quicksightdatasource5.attr_arn,
                        "upload_settings": {
                            "format": "CSV",
                            "start_from_row": 1,
                            "contains_header": True,
                            "text_qualifier": "DOUBLE_QUOTE",
                            "delimiter": ","
                        },
                        "input_columns": [
                            {
                                "name": "ColumnId-1",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-2",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-3",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-4",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-5",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-6",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-7",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-8",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-9",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-10",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-11",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-12",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-13",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-14",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-15",
                                "type": "STRING"
                            }
                        ]
                    }
                }
            },
            logical_table_map={
                "s3_physical_table": {
                    "alias": "Group 1",
                    "data_transforms": [
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-2",
                                "new_column_name": "Employee Name"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-3",
                                "new_column_name": "Employee ID"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-1",
                                "new_column_name": "Date"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-12",
                                "new_column_name": "Job Family"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-6",
                                "new_column_name": "Date of Birth"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-11",
                                "new_column_name": "Business Function"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-7",
                                "new_column_name": "Gender"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-14",
                                "new_column_name": "Notes"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-4",
                                "new_column_name": "Tenure"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-13",
                                "new_column_name": "Job Level"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-5",
                                "new_column_name": "Monthly Compensation"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-10",
                                "new_column_name": "Region"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-8",
                                "new_column_name": "Education"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-9",
                                "new_column_name": "Event Type"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-15",
                                "new_column_name": "isUnique"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Monthly Compensation",
                                "new_column_type": "DECIMAL",
                                "sub_type": "FLOAT"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Tenure",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Date of Birth",
                                "new_column_type": "DATETIME",
                                "format": "yyyy-MM-dd"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Date",
                                "new_column_type": "DATETIME",
                                "format": "yyyy-MM-dd"
                            }
                        },
                        {
                            "tag_column_operation": {
                                "column_name": "Region",
                                "tags": [
                                    {
                                        "column_geographic_role": "STATE"
                                    }
                                ]
                            }
                        }
                    ],
                    "source": {
                        "physical_table_id": "s3PhysicalTable"
                    }
                }
            },
            import_mode="SPICE",
            permissions=[
                {
                    "principal": "arn:aws:quicksight:us-east-1:064855577434:user/default/boss",
                    "actions": [
                        "quicksight:DeleteDataSet",
                        "quicksight:UpdateDataSetPermissions",
                        "quicksight:PutDataSetRefreshProperties",
                        "quicksight:CreateRefreshSchedule",
                        "quicksight:CancelIngestion",
                        "quicksight:ListRefreshSchedules",
                        "quicksight:PassDataSet",
                        "quicksight:UpdateRefreshSchedule",
                        "quicksight:DeleteRefreshSchedule",
                        "quicksight:DescribeDataSetRefreshProperties",
                        "quicksight:DescribeDataSet",
                        "quicksight:CreateIngestion",
                        "quicksight:DescribeRefreshSchedule",
                        "quicksight:ListIngestions",
                        "quicksight:DescribeDataSetPermissions",
                        "quicksight:UpdateDataSet",
                        "quicksight:DeleteDataSetRefreshProperties",
                        "quicksight:DescribeIngestion"
                    ]
                }
            ]
        )

        quicksightdataset6 = quicksight.CfnDataSet(
            self,
            "QuickSightDataSet6",
            data_set_id="92b5a28d-6baa-4a23-8503-ccd9fc6004a0",
            name="Web and Social Media Analytics",
            aws_account_id="064855577434",
            physical_table_map={
                "s3_physical_table": {
                    "s3_source": {
                        "data_source_arn": quicksightdatasource.attr_arn,
                        "upload_settings": {
                            "format": "CSV",
                            "start_from_row": 1,
                            "contains_header": True,
                            "text_qualifier": "DOUBLE_QUOTE",
                            "delimiter": ","
                        },
                        "input_columns": [
                            {
                                "name": "ColumnId-1",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-2",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-3",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-4",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-5",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-6",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-7",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-8",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-9",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-10",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-11",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-12",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-13",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-14",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-15",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-16",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-17",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-18",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-19",
                                "type": "STRING"
                            }
                        ]
                    }
                }
            },
            logical_table_map={
                "s3_physical_table": {
                    "alias": "Group 1",
                    "data_transforms": [
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-2",
                                "new_column_name": "New visitors SEO"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-3",
                                "new_column_name": "New visitors CPC"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-1",
                                "new_column_name": "Date"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-12",
                                "new_column_name": "Website Visits"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-6",
                                "new_column_name": "Twitter mentions"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-11",
                                "new_column_name": "Website Pageviews"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-7",
                                "new_column_name": "Twitter followers adds"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-14",
                                "new_column_name": "Mobile uniques"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-4",
                                "new_column_name": "New visitors Social Media"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-13",
                                "new_column_name": "Website Unique Visits"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-5",
                                "new_column_name": "Return visitors"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-10",
                                "new_column_name": "Mailing list cumulative"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-8",
                                "new_column_name": "Twitter followers cumulative"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-9",
                                "new_column_name": "Mailing list adds "
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-19",
                                "new_column_name": "Events"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-16",
                                "new_column_name": "Desktop uniques"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-15",
                                "new_column_name": "Tablet uniques"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-18",
                                "new_column_name": "Paid conversion"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-17",
                                "new_column_name": "Free sign up"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Free sign up",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Paid conversion",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Tablet uniques",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Desktop uniques",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Mailing list adds ",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Twitter followers cumulative",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Mailing list cumulative",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Return visitors",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Website Unique Visits",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "New visitors Social Media",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Mobile uniques",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Twitter followers adds",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Website Pageviews",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Twitter mentions",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Website Visits",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Date",
                                "new_column_type": "DATETIME",
                                "format": "M/d/yyyy"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "New visitors CPC",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "New visitors SEO",
                                "new_column_type": "INTEGER"
                            }
                        }
                    ],
                    "source": {
                        "physical_table_id": "s3PhysicalTable"
                    }
                }
            },
            import_mode="SPICE",
            permissions=[
                {
                    "principal": "arn:aws:quicksight:us-east-1:064855577434:user/default/japo-write",
                    "actions": [
                        "quicksight:DeleteDataSet",
                        "quicksight:UpdateDataSetPermissions",
                        "quicksight:PutDataSetRefreshProperties",
                        "quicksight:CreateRefreshSchedule",
                        "quicksight:CancelIngestion",
                        "quicksight:ListRefreshSchedules",
                        "quicksight:PassDataSet",
                        "quicksight:DeleteRefreshSchedule",
                        "quicksight:UpdateRefreshSchedule",
                        "quicksight:DescribeDataSetRefreshProperties",
                        "quicksight:DescribeDataSet",
                        "quicksight:CreateIngestion",
                        "quicksight:DescribeRefreshSchedule",
                        "quicksight:ListIngestions",
                        "quicksight:UpdateDataSet",
                        "quicksight:DescribeDataSetPermissions",
                        "quicksight:DeleteDataSetRefreshProperties",
                        "quicksight:DescribeIngestion"
                    ]
                }
            ]
        )

        quicksightdataset7 = quicksight.CfnDataSet(
            self,
            "QuickSightDataSet7",
            data_set_id="6caf1b57-facc-4d0e-8ee8-7162cec9b3cb",
            name="Business Review",
            aws_account_id="064855577434",
            physical_table_map={
                "s3_physical_table": {
                    "s3_source": {
                        "data_source_arn": quicksightdatasource3.attr_arn,
                        "upload_settings": {
                            "format": "CSV",
                            "start_from_row": 1,
                            "contains_header": True,
                            "text_qualifier": "DOUBLE_QUOTE",
                            "delimiter": ","
                        },
                        "input_columns": [
                            {
                                "name": "ColumnId-1",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-2",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-3",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-4",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-5",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-6",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-7",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-8",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-9",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-10",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-11",
                                "type": "STRING"
                            }
                        ]
                    }
                }
            },
            logical_table_map={
                "s3_physical_table": {
                    "alias": "Group 1",
                    "data_transforms": [
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-2",
                                "new_column_name": "Customer ID"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-3",
                                "new_column_name": "Customer Name"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-1",
                                "new_column_name": "Date"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-6",
                                "new_column_name": "Service Line"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-11",
                                "new_column_name": "Distinct ID"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-7",
                                "new_column_name": "Revenue Goal"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-4",
                                "new_column_name": "Customer Region"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-5",
                                "new_column_name": "Segment"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-10",
                                "new_column_name": "Channel"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-8",
                                "new_column_name": "Billed Amount"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-9",
                                "new_column_name": "Cost"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Cost",
                                "new_column_type": "DECIMAL",
                                "sub_type": "FLOAT"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Billed Amount",
                                "new_column_type": "DECIMAL",
                                "sub_type": "FLOAT"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Revenue Goal",
                                "new_column_type": "DECIMAL",
                                "sub_type": "FLOAT"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Distinct ID",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Date",
                                "new_column_type": "DATETIME",
                                "format": "M/d/yyyy"
                            }
                        },
                        {
                            "tag_column_operation": {
                                "column_name": "Customer Region",
                                "tags": [
                                    {
                                        "column_geographic_role": "STATE"
                                    }
                                ]
                            }
                        }
                    ],
                    "source": {
                        "physical_table_id": "s3PhysicalTable"
                    }
                }
            },
            import_mode="SPICE",
            permissions=[
                {
                    "principal": "arn:aws:quicksight:us-east-1:064855577434:user/default/japo-write",
                    "actions": [
                        "quicksight:DeleteDataSet",
                        "quicksight:UpdateDataSetPermissions",
                        "quicksight:PutDataSetRefreshProperties",
                        "quicksight:CreateRefreshSchedule",
                        "quicksight:CancelIngestion",
                        "quicksight:PassDataSet",
                        "quicksight:UpdateRefreshSchedule",
                        "quicksight:DeleteRefreshSchedule",
                        "quicksight:ListRefreshSchedules",
                        "quicksight:DescribeDataSetRefreshProperties",
                        "quicksight:DescribeDataSet",
                        "quicksight:CreateIngestion",
                        "quicksight:DescribeRefreshSchedule",
                        "quicksight:ListIngestions",
                        "quicksight:DescribeDataSetPermissions",
                        "quicksight:UpdateDataSet",
                        "quicksight:DeleteDataSetRefreshProperties",
                        "quicksight:DescribeIngestion"
                    ]
                }
            ]
        )

        quicksightdataset8 = quicksight.CfnDataSet(
            self,
            "QuickSightDataSet8",
            data_set_id="1b5e0ce9-1c45-4617-8c62-936e47084640",
            name="People Overview",
            aws_account_id="064855577434",
            physical_table_map={
                "s3_physical_table": {
                    "s3_source": {
                        "data_source_arn": quicksightdatasource8.attr_arn,
                        "upload_settings": {
                            "format": "CSV",
                            "start_from_row": 1,
                            "contains_header": True,
                            "text_qualifier": "DOUBLE_QUOTE",
                            "delimiter": ","
                        },
                        "input_columns": [
                            {
                                "name": "ColumnId-1",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-2",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-3",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-4",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-5",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-6",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-7",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-8",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-9",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-10",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-11",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-12",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-13",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-14",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-15",
                                "type": "STRING"
                            }
                        ]
                    }
                }
            },
            logical_table_map={
                "s3_physical_table": {
                    "alias": "Group 1",
                    "data_transforms": [
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-2",
                                "new_column_name": "Employee Name"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-3",
                                "new_column_name": "Employee ID"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-1",
                                "new_column_name": "Date"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-12",
                                "new_column_name": "Job Family"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-6",
                                "new_column_name": "Date of Birth"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-11",
                                "new_column_name": "Business Function"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-7",
                                "new_column_name": "Gender"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-14",
                                "new_column_name": "Notes"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-4",
                                "new_column_name": "Tenure"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-13",
                                "new_column_name": "Job Level"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-5",
                                "new_column_name": "Monthly Compensation"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-10",
                                "new_column_name": "Region"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-8",
                                "new_column_name": "Education"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-9",
                                "new_column_name": "Event Type"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-15",
                                "new_column_name": "isUnique"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Monthly Compensation",
                                "new_column_type": "DECIMAL",
                                "sub_type": "FLOAT"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Tenure",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Date of Birth",
                                "new_column_type": "DATETIME",
                                "format": "yyyy-MM-dd"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Date",
                                "new_column_type": "DATETIME",
                                "format": "yyyy-MM-dd"
                            }
                        },
                        {
                            "tag_column_operation": {
                                "column_name": "Region",
                                "tags": [
                                    {
                                        "column_geographic_role": "STATE"
                                    }
                                ]
                            }
                        }
                    ],
                    "source": {
                        "physical_table_id": "s3PhysicalTable"
                    }
                }
            },
            import_mode="SPICE",
            permissions=[
                {
                    "principal": "arn:aws:quicksight:us-east-1:064855577434:user/default/japo-write",
                    "actions": [
                        "quicksight:DeleteDataSet",
                        "quicksight:UpdateDataSetPermissions",
                        "quicksight:PutDataSetRefreshProperties",
                        "quicksight:CreateRefreshSchedule",
                        "quicksight:CancelIngestion",
                        "quicksight:PassDataSet",
                        "quicksight:UpdateRefreshSchedule",
                        "quicksight:DeleteRefreshSchedule",
                        "quicksight:ListRefreshSchedules",
                        "quicksight:DescribeDataSetRefreshProperties",
                        "quicksight:DescribeDataSet",
                        "quicksight:CreateIngestion",
                        "quicksight:DescribeRefreshSchedule",
                        "quicksight:ListIngestions",
                        "quicksight:UpdateDataSet",
                        "quicksight:DescribeDataSetPermissions",
                        "quicksight:DeleteDataSetRefreshProperties",
                        "quicksight:DescribeIngestion"
                    ]
                }
            ]
        )

        quicksightdataset9 = quicksight.CfnDataSet(
            self,
            "QuickSightDataSet9",
            data_set_id="bea7f081-abae-4828-af44-6d1302e49843",
            name="Sales Pipeline",
            aws_account_id="064855577434",
            physical_table_map={
                "s3_physical_table": {
                    "s3_source": {
                        "data_source_arn": quicksightdatasource6.attr_arn,
                        "upload_settings": {
                            "format": "CSV",
                            "start_from_row": 1,
                            "contains_header": True,
                            "text_qualifier": "DOUBLE_QUOTE",
                            "delimiter": ","
                        },
                        "input_columns": [
                            {
                                "name": "ColumnId-1",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-2",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-3",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-4",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-5",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-6",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-7",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-8",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-9",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-10",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-11",
                                "type": "STRING"
                            },
                            {
                                "name": "ColumnId-12",
                                "type": "STRING"
                            }
                        ]
                    }
                }
            },
            logical_table_map={
                "s3_physical_table": {
                    "alias": "Group 1",
                    "data_transforms": [
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-2",
                                "new_column_name": "Salesperson"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-3",
                                "new_column_name": "Lead Name"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-1",
                                "new_column_name": "Date"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-12",
                                "new_column_name": "IsLatest"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-6",
                                "new_column_name": "Target Close"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-11",
                                "new_column_name": "ActiveItem"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-7",
                                "new_column_name": "Forecasted Monthly Revenue"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-4",
                                "new_column_name": "Segment"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-5",
                                "new_column_name": "Region"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-10",
                                "new_column_name": "Is Closed"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-8",
                                "new_column_name": "Opportunity Stage"
                            }
                        },
                        {
                            "rename_column_operation": {
                                "column_name": "ColumnId-9",
                                "new_column_name": "Weighted Revenue"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Weighted Revenue",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Forecasted Monthly Revenue",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Target Close",
                                "new_column_type": "DATETIME",
                                "format": "M/d/yyyy"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "IsLatest",
                                "new_column_type": "INTEGER"
                            }
                        },
                        {
                            "cast_column_type_operation": {
                                "column_name": "Date",
                                "new_column_type": "DATETIME",
                                "format": "M/d/yyyy"
                            }
                        },
                        {
                            "tag_column_operation": {
                                "column_name": "Region",
                                "tags": [
                                    {
                                        "column_geographic_role": "STATE"
                                    }
                                ]
                            }
                        }
                    ],
                    "source": {
                        "physical_table_id": "s3PhysicalTable"
                    }
                }
            },
            import_mode="SPICE",
            permissions=[
                {
                    "principal": "arn:aws:quicksight:us-east-1:064855577434:user/default/japo-write",
                    "actions": [
                        "quicksight:DeleteDataSet",
                        "quicksight:UpdateDataSetPermissions",
                        "quicksight:PutDataSetRefreshProperties",
                        "quicksight:CreateRefreshSchedule",
                        "quicksight:CancelIngestion",
                        "quicksight:PassDataSet",
                        "quicksight:UpdateRefreshSchedule",
                        "quicksight:DeleteRefreshSchedule",
                        "quicksight:ListRefreshSchedules",
                        "quicksight:DescribeDataSetRefreshProperties",
                        "quicksight:DescribeDataSet",
                        "quicksight:CreateIngestion",
                        "quicksight:DescribeRefreshSchedule",
                        "quicksight:ListIngestions",
                        "quicksight:DescribeDataSetPermissions",
                        "quicksight:UpdateDataSet",
                        "quicksight:DeleteDataSetRefreshProperties",
                        "quicksight:DescribeIngestion"
                    ]
                }
            ]
        )

        quicksightanalysis = quicksight.CfnAnalysis(
            self,
            "QuickSightAnalysis",
            analysis_id="3fdd72f6-76fe-482b-a276-fbc8f53f8176",
            name="Web and Social Media Analytics analysis",
            aws_account_id="064855577434",
            source_entity="REPLACEME",
            permissions=[
                {
                    "principal": "arn:aws:quicksight:us-east-1:064855577434:user/default/japo-write",
                    "actions": [
                        "quicksight:RestoreAnalysis",
                        "quicksight:UpdateAnalysisPermissions",
                        "quicksight:DeleteAnalysis",
                        "quicksight:DescribeAnalysisPermissions",
                        "quicksight:QueryAnalysis",
                        "quicksight:DescribeAnalysis",
                        "quicksight:UpdateAnalysis"
                    ]
                }
            ]
        )

        quicksightanalysis2 = quicksight.CfnAnalysis(
            self,
            "QuickSightAnalysis2",
            analysis_id="ef1471da-d860-4823-8ba2-61a61efae863",
            name="Sales Pipeline analysis",
            aws_account_id="064855577434",
            source_entity="REPLACEME",
            permissions=[
                {
                    "principal": "arn:aws:quicksight:us-east-1:064855577434:user/default/japo-write",
                    "actions": [
                        "quicksight:RestoreAnalysis",
                        "quicksight:UpdateAnalysisPermissions",
                        "quicksight:DeleteAnalysis",
                        "quicksight:DescribeAnalysisPermissions",
                        "quicksight:QueryAnalysis",
                        "quicksight:DescribeAnalysis",
                        "quicksight:UpdateAnalysis"
                    ]
                }
            ]
        )

        quicksightanalysis3 = quicksight.CfnAnalysis(
            self,
            "QuickSightAnalysis3",
            analysis_id="0a19feda-8b7c-464d-b1ea-111fa53ebdbc",
            name="People Overview analysis",
            aws_account_id="064855577434",
            source_entity="REPLACEME",
            permissions=[
                {
                    "principal": "arn:aws:quicksight:us-east-1:064855577434:user/default/japo-write",
                    "actions": [
                        "quicksight:RestoreAnalysis",
                        "quicksight:UpdateAnalysisPermissions",
                        "quicksight:DeleteAnalysis",
                        "quicksight:DescribeAnalysisPermissions",
                        "quicksight:QueryAnalysis",
                        "quicksight:DescribeAnalysis",
                        "quicksight:UpdateAnalysis"
                    ]
                }
            ]
        )

        quicksightanalysis4 = quicksight.CfnAnalysis(
            self,
            "QuickSightAnalysis4",
            analysis_id="d261b686-2447-4542-8d92-0b2227336e8b",
            name="Business Review analysis",
            aws_account_id="064855577434",
            source_entity="REPLACEME",
            permissions=[
                {
                    "principal": "arn:aws:quicksight:us-east-1:064855577434:user/default/japo-write",
                    "actions": [
                        "quicksight:RestoreAnalysis",
                        "quicksight:UpdateAnalysisPermissions",
                        "quicksight:DeleteAnalysis",
                        "quicksight:DescribeAnalysisPermissions",
                        "quicksight:QueryAnalysis",
                        "quicksight:DescribeAnalysis",
                        "quicksight:UpdateAnalysis"
                    ]
                }
            ]
        )

        quicksightanalysis5 = quicksight.CfnAnalysis(
            self,
            "QuickSightAnalysis5",
            analysis_id="fc5a12e3-9fe3-4093-9bc2-73bd10834d2a",
            name="Web and Social Media Analytics analysis",
            aws_account_id="064855577434",
            source_entity="REPLACEME",
            permissions=[
                {
                    "principal": "arn:aws:quicksight:us-east-1:064855577434:user/default/boss",
                    "actions": [
                        "quicksight:RestoreAnalysis",
                        "quicksight:UpdateAnalysisPermissions",
                        "quicksight:DeleteAnalysis",
                        "quicksight:DescribeAnalysisPermissions",
                        "quicksight:QueryAnalysis",
                        "quicksight:DescribeAnalysis",
                        "quicksight:UpdateAnalysis"
                    ]
                }
            ]
        )
        
        quicksightanalysis6 = quicksight.CfnAnalysis(
            self,
            "QuickSightAnalysis6",
            analysis_id="e3301c4c-e67b-400c-b36c-12edaacbc558",
            name="People analysis",
            aws_account_id="064855577434",
            source_entity={
                'sourceTemplate': {
                    'dataSetReferences': [
                        {
                            'dataSetPlaceholder': 'Placeholder',
                            'dataSetArn': dataset_arn
                        }
                    ]
                }
            },
            permissions=[
                {
                    "principal": "arn:aws:quicksight:us-east-1:064855577434:user/default/boss",
                    "actions": [
                        "quicksight:RestoreAnalysis",
                        "quicksight:UpdateAnalysisPermissions",
                        "quicksight:DeleteAnalysis",
                        "quicksight:DescribeAnalysisPermissions",
                        "quicksight:QueryAnalysis",
                        "quicksight:DescribeAnalysis",
                        "quicksight:UpdateAnalysis"
                    ]
                }
            ]
        )

        quicksightanalysis7 = quicksight.CfnAnalysis(
            self,
            "QuickSightAnalysis7",
            analysis_id="5cf45932-3d70-4c8d-8b88-ac910005292c",
            name="People Overview analysis",
            aws_account_id="064855577434",
            source_entity="REPLACEME",
            permissions=[
                {
                    "principal": "arn:aws:quicksight:us-east-1:064855577434:user/default/boss",
                    "actions": [
                        "quicksight:RestoreAnalysis",
                        "quicksight:UpdateAnalysisPermissions",
                        "quicksight:DeleteAnalysis",
                        "quicksight:DescribeAnalysisPermissions",
                        "quicksight:QueryAnalysis",
                        "quicksight:DescribeAnalysis",
                        "quicksight:UpdateAnalysis"
                    ]
                }
            ]
        )

        quicksightanalysis8 = quicksight.CfnAnalysis(
            self,
            "QuickSightAnalysis8",
            analysis_id="b8b76b7c-0004-4db7-8fed-491bc6d8a513",
            name="Business Review analysis",
            aws_account_id="064855577434",
            source_entity="REPLACEME",
            permissions=[
                {
                    "principal": "arn:aws:quicksight:us-east-1:064855577434:user/default/boss",
                    "actions": [
                        "quicksight:RestoreAnalysis",
                        "quicksight:UpdateAnalysisPermissions",
                        "quicksight:DeleteAnalysis",
                        "quicksight:DescribeAnalysisPermissions",
                        "quicksight:QueryAnalysis",
                        "quicksight:DescribeAnalysis",
                        "quicksight:UpdateAnalysis"
                    ]
                }
            ]
        )

        quicksightanalysis9 = quicksight.CfnAnalysis(
            self,
            "QuickSightAnalysis9",
            analysis_id="723deffa-11a7-479b-a341-9ed458669106",
            name="Sales Pipeline analysis",
            aws_account_id="064855577434",
            source_entity="REPLACEME",
            permissions=[
                {
                    "principal": "arn:aws:quicksight:us-east-1:064855577434:user/default/boss",
                    "actions": [
                        "quicksight:RestoreAnalysis",
                        "quicksight:UpdateAnalysisPermissions",
                        "quicksight:DeleteAnalysis",
                        "quicksight:DescribeAnalysisPermissions",
                        "quicksight:QueryAnalysis",
                        "quicksight:DescribeAnalysis",
                        "quicksight:UpdateAnalysis"
                    ]
                }
            ]
        )


app = cdk.App()
MyStack(app, "my-stack-name", env={'region': 'us-east-1'})
app.synth()
