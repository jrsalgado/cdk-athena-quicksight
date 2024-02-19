#!/bin/bash

ENVIRONMENT=${1:-"local"}
echo ${ENVIRONMENT}
parameter_overrides=""
while IFS='=' read -r key value; do
    parameter_overrides="$parameter_overrides $key=$value"
done < parameter-overrides/${ENVIRONMENT}.txt


echo $parameter_overrides
aws cloudformation deploy \
    --region <REPLACE> \
    --profile <REPLACE> \
    --stack-name <REPLACE> \
    --template-file <REPLACE> \
    --parameter-overrides $parameter_overrides
