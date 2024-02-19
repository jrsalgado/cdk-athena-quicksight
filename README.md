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
pip install --editable .
```

## Disaster Recovery
By fetching and storing resource descriptions, users can create backups of QuickSight configurations, dashboards, analyses, data sets, data sources, Athena workgroups, Athena data catalogs, and Glue databases.

1. **Fetch Resources**: Use qscli fetch all to store descriptions of all resources in the /infra_base directory.

2. **Generate Templates**: Use qscli build commands to create CloudFormation templates for each resource type.

3. **Deploy Templates**: Deploy CloudFormation templates with qscli deploy to recreate QuickSight environment and resources. Customize configurations using parameter override files.

This process ensures swift recovery of QuickSight, Athena and Glue resources in case of a disaster.

## CLI Commands

### Fetch Resource Descriptions
| Command | Description | Status |
| --- | --- | :---: |
| fetch all | Fetch all related resources from AWS Account | ✅ |
| fetch dashboard | Fetch a Dashboard from its ID | TODO |
| fetch dashboards | Fetch all Dashboards | ✅ |
| fetch analysis | Fetch an Analysis from its ID | TODO |
| fetch analyses | Fetch all Analyses | ✅ |
| fetch data-set| Fetch a Data Set from its ID | TODO |
| fetch data-sets | Fetch all Data Sets | ✅ |
| fetch data-source | Fetch a Data Source from its ID | TODO |
| fetch data-sources | Fetch all Data Sources | ✅ |
| fetch workgroup | Fetch an Athena Workgroups by name | TODO |
| fetch workgroups | Fetch all Athena Workgroups | ✅ |
| fetch data-catalog | Fetch an Athena Data Catalogs by name | TODO |
| fetch data-catalogs | Fetch all Athena Data Catalogs | ✅ |
| fetch glue | Fetch all Glue Databases | ✅ |
| fetch lambdas | Fetch all Lambdas descriptions | ✅ |

### Build CloudFormation Template
| Command | Description | Status |
| --- | --- | :---: |
| build dashboard | Build a template for a specific Dashboard by ID, and its dependencies. | ✅ |
| build dashboards | Build templates for all Dashboards. | TODO |
| build analysis | Build a template for a specific Analysis by ID. | ✅ |
| build analyses | Build templates for all Analyses. | TODO |
| build data-set | Build a template for a specific Data Set by ID. | ✅ |
| build data-sets | Build templates for all Data Sets.	 | TODO |
| build data-source | Build a template for a specific Data Source by ID. | ✅ |
| build data-sources | Build templates for all Data Sources.	 | TODO |
| build athena | Build a template for a specific Athena Workgroup and Data Catalogs.	 | ✅ |
| build glue | Build a template for a specific Glue Database	 | ✅ |

### Deploy CloudFormation Template
| Command | Description | Status |
| --- | --- | :---: |
| deploy dashboard | Deploy a single Dashboard template | ✅ |
| deploy dashboards | Deploy all dashboards templates | TODO |
| deploy analysis | Deploy a single Analysis template | ✅ |
| deploy analyses | Deploy all Analyses | TODO |
| deploy dataset | Deploy a single Data Set template | ✅ |
| deploy datasets | Deploy all Data Sets | TODO |
| deploy datasource | Deploy a single Data Source template | ✅ |
| deploy datasources | Deploy all Data Sources | TODO |
| deploy athena | Deploy Athena resources | ✅ |
| deploy glue | Deploy Glue Database | ✅ |

# Usage

### Fetch Resources
This command fetches and stores the descriptions of all the necessary resources of a specific AWS account on the `/infra_base` directory.
```bash
qscli fetch all --account-id <ACCOUNT_ID> --profile <PROFILE_NAME>
```
If already authenticated (Cloud9), the option --profile can be skipped

## Athena

### Build Athena Template

This command generates a CloudFormation template to clone an existing Athena Workgroup and Data Catalog.

Get the name of the desired athena resource from: 
- workgroup: /infra_base/XXXXXXXXXXX/athena/workgroups/
- data-catalog: /infra_base/XXXXXXXXXXX/athena/data-catalog/
```bash
qscli build athena --workgroup-name <WORKGROUP_NAME> --catalog-name <DATA_CATALOG_NAME> --account-id <ACCOUNT_ID>
```

### Deploy Athena Template

```bash
qscli deploy athena <RELATIVE_PATH_TO_TEMPLATE> --account-id <ACCOUNT_ID> --profile <AWS_PROFILE> --parameters-path <PARAMS_FILE_NAME>
```

The path to the template to deploy should be:
- ./CFTemplates/XXXXXXXXXXX/athena/athena_template.yaml

--parameters-path (default: athena.local.txt)
- Create a new file in /parameter-overrides with the following values

```
AthenaWorkgroupName=<REPLACE>             # Name for the new Workgroup
AthenaWorkgroupOutputLocation=<REPLACE>   # S3 bucket location to store query results
AthenaDataCatalogName=<REPLACE>           # Name for the new Data Catalog
```


## Glue

### Build Glue Template

This command generates a CloudFormation template to clone an existing Glue Database and its tables.

Get the name of the desired glue database name from: 
- /infra_base/XXXXXXXXXXX/glue/databases/

```bash
qscli build glue <DATABASE_NAME> --account-id <ACCOUNT_ID>
```

### Deploy Glue Template

```bash
qscli deploy glue <RELATIVE_PATH_TO_TEMPLATE> --account-id <ACCOUNT_ID> --profile <AWS_PROFILE> --parameters-path <PARAMS_FILE_NAME>
```

The path to the template to deploy should be:
- ./CFTemplates/XXXXXXXXXXX/glue/<DATABASE_NAME>.yaml

--parameters-path (default: glue.local.txt)
- Create a new file in /parameter-overrides with the following values

```
GlueDatabaseName=<REPLACE>
```

## Quicksight

For Quicksight resources to be cloned properly, Glue and Athena resources must be created first.

### Build Dashboard Template
This command generates a CloudFormation template to clone an existing dashboard from its ID.

Get the ID of the desired dashboard from /infra_base/XXXXXXXXXXX/dashboards/list-dashboards.yaml
```bash
qscli build dashboard <DASHBOARD_ID> --account-id <ACCOUNT_ID> --create-dependencies True
```
`--create-dependencies True` Finds and create all the quicksight resources that are needed to create a fully working Dashboard

### Deploy Dashboard Template
```bash
qscli deploy dashboard <RELATIVE_PATH_TO_TEMPLATE> --account-id <ACCOUNT_ID> --region <REGION> --profile <PROFILE_NAME> --parameters-path <PARAMS_FILE_NAME> 
```
The path to the template to deploy should be:
- ./CFTemplates/XXXXXXXXXXX/dashboards/<DASHBOARD_ID>.yaml

Command options
- --account-id [Required]

- --region (default: us-east-1)

- --profile (Optional if already authenticated)

- --parameters-path (default: dashboard.local.txt)

    - Create a new file in /parameter-overrides with the following values

```
DataSourceId01=<REPLACE>            # Has to be unique
DataSourceName01=<REPLACE>
DataSourceAthenaWorkGroup01=<REPLACE> # Name of the new workgroup from Athena

DataSetAthenaId01=<REPLACE>         # Has to be unique
DataSetAthenaName01=<REPLACE>
DataSetAthenaCatalog01=<REPLACE>    # Name of the new Athena Data Catalog
DataSetAthenaTableName01=<REPLACE>  # Name of the table inside Glue Database
DataSetAthenaSchema01=<REPLACE>     # Name of the Glue Database

DashboardId01=<REPLACE>             # Has to be unique
DashboardName01=<REPLACE>
DashboardDataSetIdentifier01=<REPLACE with Data Set name> # Has to be the dataset name

AnalysisId01=<REPLACE>              # Has to be unique
AnalysisName01=<REPLACE>

QuickSightUsername=<REPLACE from original> # Quicksight username with access
```

For building and deploying other Quicksight resources, the process is the same
- Fetch all resources.
- Generate a CF template using the build command and providing the id for the resource to clone, (with `--create-dependencies True` to automatically resolve all of the dependencies).
- Create the parameters override file with the desired values for the specific resource.
- And use the deploy command to create the stack on the desired AWS account.