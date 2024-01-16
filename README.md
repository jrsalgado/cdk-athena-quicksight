
# Welcome to your CDK Python project!

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!


# QuickSight Fetcher CLI
## Overview
This Python CLI script provides functionality to interact with Amazon QuickSight resources. It allows you to fetch QuickSight resources, clone dashboards, and clone all dashboards from a specified AWS account.

## Prerequisites
- Python 3.x
- AWS CLI & Profile configured with necessary permissions

## Installation
Clone the repository:
```bash
git clone https://github.com/jrsalgado/cdk-athena-quicksight
```

Create a virtual environment:
```bash
python3 -m venv .venv

source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```
## Usage
Fetch All QuickSight Resources, By default, --profile is "default"
```bash
./qscli.py fetchallquicksightresources --account-id <ACCOUNT_ID> --profile <PROFILE_NAME>
```

Clone Dashboard From Dashboard ID
```bash
./qscli.py clonefromdashboardid --account-id <ACCOUNT_ID> <DASHBOARD_ID>
```

Clone All Dashboards
```bash
./qscli.py clonealldashboards --account-id <ACCOUNT_ID>
```