.PHONY: synth

ORIGIN_AWS_ACCOUNT_ID ?= 064855577434
ORIGIN_DATASOURCE_ID ?= 11e7f1b6-a92f-477e-95d9-dc36931443b2
ORIGIN_DATASET_ID ?= 2384dd87-5baa-4308-b2e4-1ec602bba012
ORIGIN_DASHBOARD_ID ?= 4cb1c2ee-b71f-4f25-985a-7668cb3c2ddd

export ORIGIN_AWS_ACCOUNT_ID

# TODO: Create top resource with dependencies from REF or PARAMS
#CFTemplate01 = dsource1(REF origin resource) -> dset1(REF origin resource) -> dashboard01(ORIGIN_DASHBOARD_ID)
#																			-> analysis01
#CFTemplate02 = dsource1(REF origin resource) -> dset1(ORIGIN_DATASET_ID)
#CFTemplate03 = dsource1(ORIGIN_DATASORCE_ID)

# TODO: Create top resource with dependencies from REF or PARAMS
#CFTemplate01 = dsource1(REF) -> dset1(REF) -> dashboard01
#CFTemplate02 = dsource1(param) -> dset1(param) -> dashboard02


clean-template-account:
	@rm -rf ./CFTemplates/${ORIGIN_AWS_ACCOUNT_ID}

synth-just-data-source:
	export ORIGIN_DATASOURCE
	cdk synth --context general_params=parameters/general.yaml --context params=parameters/just-data-source.yaml > ./outputs/output-just-data-source.yaml

synth-till-data-set:
	export ORIGIN_DATASOURCE_ID=${ORIGIN_DATASOURCE_ID}; \
	export ORIGIN_DATASET_ID=${ORIGIN_DATASET_ID}; \
	mkdir -p ./CFTemplates/${ORIGIN_AWS_ACCOUNT_ID}/dataset && \
	rm -rf ./CFTemplates/${ORIGIN_AWS_ACCOUNT_ID}/dataset/${ORIGIN_DATASET_ID}.yaml && \
	cdk synth \
		--context general_params=parameters/general.yaml \
		--context params=parameters/just-data-source.yaml \
		--context dataset_params=parameters/just-data-set.yaml > ./CFTemplates/${ORIGIN_AWS_ACCOUNT_ID}/dataset/${ORIGIN_DATASET_ID}.yaml

synth-till-dashboard:
	export ORIGIN_DATASOURCE_ID=${ORIGIN_DATASOURCE_ID}; \
	export ORIGIN_DATASET_ID=${ORIGIN_DATASET_ID}; \
	export ORIGIN_DASHBOARD_ID=${ORIGIN_DASHBOARD_ID}; \
	mkdir -p ./CFTemplates/${ORIGIN_AWS_ACCOUNT_ID}/dashboard && \
	rm -rf ./CFTemplates/${ORIGIN_AWS_ACCOUNT_ID}/dashboard/${ORIGIN_DASHBOARD_ID}.yaml && \
	cdk synth --context general_params=parameters/general.yaml --context params=parameters/just-data-source.yaml --context dataset_params=parameters/just-data-set.yaml --context dashboard_params=parameters/just-dashboard.yaml > ./CFTemplates/${ORIGIN_AWS_ACCOUNT_ID}/dashboard/${ORIGIN_DASHBOARD_ID}.yaml

synth-dev:
	cdk synth --context params=parameters.yaml > output.yaml

synth-prod:
	cdk synth --context params=parameters.yaml > output.yaml

cf-deploy:
	./deploy.sh


