
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
This Python CLI script provides functionality to interact with Amazon QuickSight. It allows you to fetch QuickSight resource descriptions and clone dashboards from a specified AWS account.

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
```
```bash
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## CLI Commands

### Fetch Resource Descriptions
| Command | Description | Status |
| --- | --- | :---: |
| fetch all | Fetch all QuickSight resources from AWS Account | ✅ |
| fetch dashboard | Fetch a Dashboard from its ID | TODO |
| fetch dashboards | Fetch all Dashboards | TODO |
| fetch analysis | Fetch an Analysis from its ID | TODO |
| fetch analyses | Fetch all Analyses | TODO |
| fetch dataset| Fetch a Data Set from its ID | TODO |
| fetch datasets | Fetch all Data Sets | TODO |
| fetch datasource | Fetch a Data Source from its ID | TODO |
| fetch datasources | Fetch all Data Sources | TODO |

### Build CloudFormation Template
| Command | Description | Status |
| --- | --- | :---: |
| build dashboard | Build a template for a specific Dashboard by ID, and its dependencies. | ✅ |
| build dashboards | Build templates for all Dashboards. | ✅ |
| build analysis | Build a template for a specific Analysis by ID. | TODO |
| build analyses | Build templates for all Analyses. | TODO |
| build dataset | Build a template for a specific Data Set by ID. | TODO |
| build datasets | Build templates for all Data Sets.	 | TODO |
| build datasource | Build a template for a specific Data Source by ID. | TODO |
| build datasources | Build templates for all Data Sources.	 | TODO |

### Deploy CloudFormation Template
| Command | Description | Status |
| --- | --- | --- |
| deploy dashboard | Deploy a single Dashboard template | ✅ |
| deploy dashboards | Deploy all dashboards templates | TODO |
| deploy analysis | Deploy a single Analysis template | TODO |
| deploy analyses | Deploy all Analyses | TODO |
| deploy dataset | Deploy a single Data Set template | TODO |
| deploy datasets | Deploy all Data Sets | TODO |
| deploy datasource | Deploy a single Data Source template | TODO |
| deploy datasources | Deploy all Data Sources | TODO |

## Usage
### Fetch QuickSight Resource Descriptions
This command fetches the descriptions of all the necessary QuickSight resources on a specific AWS account.
```bash
./qscli.py fetch all --account-id <ACCOUNT_ID> --profile <PROFILE_NAME>
```
If already authenticated (Cloud9), the option --profile can be skipped

### Build Dashboard Template
This command generates a CloudFormation template to clone an existing dashboard from its ID and all of the dependencies (Data Source, Data Set)

Get the dashboard ID from /infra_base/XXXXXXXXXXX/dashboards/list-dashboards.yaml
```bash
./qscli.py build dashboard --account-id <ACCOUNT_ID> <DASHBOARD_ID>
```

### Build All Dashboards
```bash
./qscli.py build dashboards --account-id <ACCOUNT_ID>
```

### Deploy Dashboard Template
When deploying a new dashboard template, a file is needed to override all the parameters values

Copy the parameters override file 
```bash
cp parameter-overrides/example.local.txt parameter-overrides/local.txt
```

And replace with the desired values
```
DataSourceId01=<Replace>      # Has to be unique
DataSourceName01=<Replace>
DataSourceAthenaWorkGroup01=primary

DataSetAthenaId01=<Replace>   # Has to be unique
DataSetAthenaName01=<Replace>
DataSetAthenaCatalog01=AwsDataCatalog   # Get from PhysicalTableMap of the dataset dependency
DataSetAthenaTableName01=<Replace>      # Get from PhysicalTableMap of the dataset dependency
DataSetAthenaSchema01=<Replace>         # Get from PhysicalTableMap of the dataset dependency

DashboardId01=<Replace>       # Has to be unique
DashboardName01=<Replace>
DashboardDataSetIdentifier01=<Replace with Data Set name> # Has to be the dataset name

QuickSightUsername=<Replace from original> # Quicksight username with access
```

#### Deploy Command
```bash
./qscli.py deploy dashboard ./CFTemplates/XXXXXXX/dashboards/<DASHBOARD_ID>.yaml --account-id <ACCOUNT_ID> --region <REGION> --profile <PROFILE_NAME> --parameters-path <PARAMS_FILE_NAME> 
```
This command needs:
- The path of the generated cloudformation template: 
    - ./CFTemplates/XXXXXXX/dashboards/<DASHBOARD_ID>.yaml
- --account-id
- --region (default: us-east-1)
- --profile (Optional if already authenticated)
- --parameters-path (name of the params override file: local.txt)