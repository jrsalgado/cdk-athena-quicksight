# Objetivo

Obtener información sobre las configuraciones de todos los recursos de QuickSight que ya estén creados en la cuenta que tiene acceso Joseph.

Tambien para probar en la cuenta de Javier

## Entregables

En formato YAML

- Lista, Descripción, Definición y Permisos de cada uno de los Dashboards
- Lista, Descripción y Permisos de cada uno de los Data Sets
- Lista, Descripción y Permisos de cada uno de los Data Sources
- Lista, Descripción, Definición y Permisos de cada uno de los Analysis

De preferencia subirlos al repositorio (cdk-athena-quicksight) y organizarlos como se menciona mas adelante, otra manera seria que nos mandaran los outputs organizados pero en un archivo .zip

## Requerimientos

- Credenciales para el CLI (con permisos de list y read en el servicio de QuickSight)
  - ACCESS KEY ID
  - SECRET ACCESS KEY
- ACCOUNT ID
- REGION

## Setup

- Configurar AWS CLI con el perfil de quicksight
- Ingresar datos solicitados ("Default output format" se puede dejar con el valor de "json" )

```bash
aws configure --profile quicksight
```

# Ejemplo de Exportación

Esto es un ejemplo de como exportariamos los datos de los recursos de quicksight y donde se van a guardar los archivos,
se haria lo mismo para datasets y datasources

```bash
#List Dashboards
WORKING_DIR="dashboards"; \
AWS_ACCOUNT_ID="448677535504"; \
AWS_PROFILE="quicksight"; \

aws quicksight list-dashboards \
  --profile ${AWS_PROFILE} \
  --region us-east-1 \
  --aws-account-id ${AWS_ACCOUNT_ID} \
  --output yaml > infra_base/${AWS_ACCOUNT_ID}/${WORKING_DIR}/list-dashboards.yaml

# FOR EACH DASHBOARD
DASHBOARD_ID="e6390395-4a03-4d80-b862-a4d3506173c8"; \
aws quicksight describe-dashboard \
  --profile ${AWS_PROFILE} \
  --region us-east-1 \
  --aws-account-id ${AWS_ACCOUNT_ID} \
  --dashboard-id ${DASHBOARD_ID} \
  --output yaml >> infra_base/${AWS_ACCOUNT_ID}/${WORKING_DIR}/${DASHBOARD_ID}.yaml && \

echo "\n" >> infra_base/${AWS_ACCOUNT_ID}/${WORKING_DIR}/${DASHBOARD_ID}.yaml && \

aws quicksight describe-dashboard-definition \
  --profile ${AWS_PROFILE} \
  --region us-east-1 \
  --aws-account-id ${AWS_ACCOUNT_ID} \
  --dashboard-id ${DASHBOARD_ID} \
  --output yaml >> infra_base/${AWS_ACCOUNT_ID}/${WORKING_DIR}/${DASHBOARD_ID}.yaml && \

echo "\n" >> infra_base/${AWS_ACCOUNT_ID}/${WORKING_DIR}/${DASHBOARD_ID}.yaml && \

aws quicksight describe-dashboard-permissions \
  --profile ${AWS_PROFILE} \
  --region us-east-1 \
  --aws-account-id ${AWS_ACCOUNT_ID} \
  --dashboard-id ${DASHBOARD_ID} \
  --output yaml >> infra_base/${AWS_ACCOUNT_ID}/${WORKING_DIR}/${DASHBOARD_ID}.yaml

echo "\n" >> infra_base/${AWS_ACCOUNT_ID}/${WORKING_DIR}/${DASHBOARD_ID}.yaml
```

# Organizar outputs

- Todos los outputs se almacenan en la carpeta **/infra_base/** en la raíz del repositorio **cdk-athena-quicksight**.
- Se crea una carpeta por cuenta en **/infra_base/\<ACCOUNT_ID>/**.
- Dentro de cada carpeta de cuenta, se crean carpetas para recursos (/dashboards, /data-sets, /data-sources, /analysis).
- Cada carpeta contiene outputs de sus respectivos recursos y a cada output se le cambiará el nombre al id que tenga asignado.
  - /dashboards
    - list-dashboards.yaml
    - /describe-dashboard
      - <dashboard_id>.yaml
    - /describe-dashboard-definition
      - <dashboard_id>.yaml
    - /describe-dashboard-permissions
      - <dashboard_id>.yaml
  - /data-sets
    - list-data-sets.yaml
    - /describe-data-sets
      - <data_set_id>.yaml
    - /describe-data-sets-permissions
      - <data_set_id>.yaml
  - /data-sources
    - list-data-sources.yaml
    - /describe-data-sources
      - <data_source_id>.yaml
    - /describe-data-sources-permissions
      - <data_source_id>.yaml
  - /analysis
    - list-analyses.yaml
    - /describe-analysis
      - <analysis_id>.yaml
    - /describe-analysis-definition
      - <analysis_id>.yaml
    - /describe-analysis-permissions
      - <analysis_id>.yaml

# Dashboards

### list-dashboards

```shell
aws quicksight list-dashboards --aws-account-id <ACCOUNT_ID> --output yaml --profile quicksight > list-dashboards.yaml
```

### describe-dashboard

```shell
aws quicksight describe-dashboard --aws-account-id <ACCOUNT_ID> --dashboard-id <DASHBOARD_ID> --output yaml --profile quicksight > describe-dashboard.yaml
```

### describe-dashboard-definition

```shell
aws quicksight describe-dashboard-definition --aws-account-id <ACCOUNT_ID> --dashboard-id <DASHBOARD_ID> --output yaml --profile quicksight > describe-dashboard-definition.yaml
```

### describe-dashboard-permissions

```shell
aws quicksight describe-dashboard-permissions --aws-account-id <ACCOUNT_ID> --dashboard-id <DASHBOARD_ID> --output yaml --profile quicksight > describe-dashboard-permissions.yaml
```

# Datasets

### list-data-sets

```shell
aws quicksight list-data-sets --aws-account-id <ACCOUNT_ID> --output yaml --profile quicksight > list-data-sets.yaml
```

### describe-data-set

```shell
aws quicksight describe-data-set --aws-account-id <ACCOUNT_ID> --data-set-id <DATA_SET_ID> --output yaml --profile quicksight > describe-data-set.yaml
```

### describe-data-set-permissions

```shell
aws quicksight describe-data-set-permissions --aws-account-id <ACCOUNT_ID> --data-set-id <DATA_SET_ID> --output yaml --profile quicksight > describe-data-set-permissions.yaml
```

# Data Sources

### list-data-sources

```shell
aws quicksight list-data-sources --aws-account-id <ACCOUNT_ID> --output yaml --profile quicksight > list-data-sources.yaml
```

### describe-data-source

```shell
aws quicksight describe-data-source --aws-account-id <ACCOUNT_ID> --data-source-id <DATA_SOURCE_ID> --output yaml --profile quicksight > describe-data-source.yaml
```

### describe-data-source-permissions

```shell
aws quicksight describe-data-source-permissions --aws-account-id <ACCOUNT_ID> --data-source-id <DATA_SOURCE_ID> --output yaml --profile quicksight > describe-data-source-permissions.yaml
```

# Analysis

### list-analyses

```shell
aws quicksight list-analyses --aws-account-id <ACCOUNT_ID> --output yaml --profile quicksight > list-analyses.yaml
```

### describe-analysis

```shell
aws quicksight describe-analysis --aws-account-id <ACCOUNT_ID> --analysis-id <ANALYSIS_ID> --output yaml --profile quicksight > describe-analysis.yaml
```

### describe-analysis-definition

```shell
aws quicksight describe-analysis-definition --aws-account-id <ACCOUNT_ID> --analysis-id <ANALYSIS_ID> --output yaml --profile quicksight > describe-analysis-definition.yaml
```

### describe-analysis-permissions

```shell
aws quicksight describe-analysis-permissions --aws-account-id <ACCOUNT_ID> --analysis-id <ANALYSIS_ID> --output yaml --profile quicksight > describe-analysis-permissions.yaml