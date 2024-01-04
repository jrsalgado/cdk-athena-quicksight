# QuickSight Resource Description Fetcher

This Python project utilizes the Boto3 library to fetch descriptions of QuickSight resources such as Dashboards, DataSets, DataSources, and Analyses. Follow the instructions below to set up and run the project.

## Installation

Make sure you have Python installed on your machine. Then, use the following steps to set up the project:

#### 1. Clone the repository:

```bash
git clone https://github.com/jrsalgado/cdk-athena-quicksight
```

#### 2. Navigate to the project directory:

```bash
cd cdk-athena-quicksight/infra_base
```

#### 3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Copy the .env.example file to create a new .env file:

```bash
cp .env.example .env
```

Open the .env file and replace the placeholder values with your AWS credentials.

```
AWS_ACCESS_KEY_ID=XXXXXXXXXXX
AWS_SECRET_ACCESS_KEY=XXXXXXXXXXX
AWS_REGION=XXXXXXXXXXXX
AWS_ACCOUNT_ID=XXXXXXXXXXX

# Jaust in case you are connecting using a role
AWS_ROLE_TO_ASSUME=arn:aws:iam::account-id-with-role-to-assume:role/role-name
```

## Usage

### Fetch Descriptions

Execute the following command to run the Python script and fetch descriptions for QuickSight resources:

```bash
make run
# (Internamente hace esto) python3 main.py
```

This command will execute the Python script, and you will see a directory with the name of the account id with all the quicksight resource descriptions

### Zip Content

To zip the content with the account ID as the directory name, use the following command:

```bash
make zip ACCOUNT_ID=XXXXXXXXX
```

Replace XXXXXXXXX with your AWS account ID. This command will create a zip file containing the descriptions, and the zip file will be named with the AWS account ID.
