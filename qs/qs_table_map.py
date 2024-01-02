import yaml
from typing import List, Union
from aws_cdk import aws_quicksight as quicksight

def load_input_columns(file_path: str) -> List[quicksight.CfnDataSet.InputColumnProperty]:
    with open(file_path, 'r') as file:
        input_columns_data = yaml.safe_load(file)

        input_columns_list = []
        for column_data in input_columns_data['InputColumns']:
            input_column = quicksight.CfnDataSet.InputColumnProperty(
                name=column_data['Name'],
                type=column_data['Type']
            )
            input_columns_list.append(input_column)

    return input_columns_list


def load_data_transforms(file_path: str) -> List[Union[quicksight.CfnDataSet.RenameColumnOperationProperty, 
                                                      quicksight.CfnDataSet.CastColumnTypeOperationProperty,
                                                      quicksight.CfnDataSet.TagColumnOperationProperty]]:
    with open(file_path, 'r') as file:
        data_transforms_data = yaml.safe_load(file)

        data_transforms_list = []
        for operation_data in data_transforms_data['DataTransforms']:
            if 'RenameColumnOperation' in operation_data:
                rename_operation = quicksight.CfnDataSet.TransformOperationProperty(
                        rename_column_operation = quicksight.CfnDataSet.RenameColumnOperationProperty(
                            column_name= operation_data['RenameColumnOperation']['ColumnName'],
                            new_column_name= operation_data['RenameColumnOperation']['NewColumnName']
                        )
                    )
                data_transforms_list.append(rename_operation)
            elif 'CastColumnTypeOperation' in operation_data:
                cast_operation = quicksight.CfnDataSet.TransformOperationProperty(
                    cast_column_type_operation= quicksight.CfnDataSet.CastColumnTypeOperationProperty(
                        column_name= operation_data['CastColumnTypeOperation']['ColumnName'],
                        new_column_type= operation_data['CastColumnTypeOperation']['NewColumnType']
                    )
                )
                data_transforms_list.append(cast_operation)
            elif 'TagColumnOperation' in operation_data:
                tag_operation= quicksight.CfnDataSet.TransformOperationProperty(
                    tag_column_operation= quicksight.CfnDataSet.TagColumnOperationProperty(
                        column_name= operation_data['TagColumnOperation']['ColumnName'],
                        tags= [
                            quicksight.CfnDataSet.ColumnTagProperty(
                                column_geographic_role= operation_data['TagColumnOperation']['Tags'][0]['ColumnGeographicRole'],
                            ),
                        ]
                    )
                )
                data_transforms_list.append(tag_operation)

    return data_transforms_list
