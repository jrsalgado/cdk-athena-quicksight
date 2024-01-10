.PHONY: synth

synth-just-data-source:
	cdk synth --context general_params=parameters/general.yaml --context params=parameters/just-data-source.yaml > ./outputs/output-just-data-source.yaml

synth-dev:
	cdk synth --context params=parameters.yaml > output.yaml

synth-prod:
	cdk synth --context params=parameters.yaml > output.yaml
