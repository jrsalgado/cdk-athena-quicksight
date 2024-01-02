.PHONY: synth

synth-dev:
	cdk synth --context params=parameters.yaml > output.yaml

synth-prod:
	cdk synth --context params=parameters.yaml > output.yaml
