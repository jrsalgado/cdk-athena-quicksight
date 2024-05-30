#!/usr/bin/env python3
import aws_cdk as cdk
from os import getenv
from qs.qs_stack import QsStack
from qs.qs_dashboard_stack import QsDashboardStack

app = cdk.App()

if getenv('USE_QUICKSIGHT_DASHBOARD', None):
    common_kwargs = {
        "dashboard_id": getenv('ORIGIN_DASHBOARD_ID', None),
        "origin_account_id": getenv('ORIGIN_AWS_ACCOUNT_ID', None)
    }

    QsDashboardStack(app, 'QsStack', **common_kwargs)
else:
    QsStack(app, "QsStack",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=cdk.Environment(account='123456789012', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()
