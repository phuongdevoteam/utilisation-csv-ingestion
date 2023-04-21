# utilisation-csv-ingestion
This repo uses the package composer-csv-ingestion to create a CSV Ingestion pipeline on Cloud Composer. The infra outlined (here)[https://devoteamgcloud.atlassian.net/wiki/spaces/NGC/pages/10873471058/Packaging+CSV+Ingestion]

#### Install the package locally
```
pip install --index-url https://europe-west4-python.pkg.dev/pj-composer-csv-ingestion/composer-csv-ingestion/simple/ composer-csv-ingestion
```

#### Install the package on Cloud Composer
Following the (guide)[https://cloud.google.com/composer/docs/how-to/using/installing-python-dependencies#install-ar-repo]. In the last step, run:
```
gcloud composer environments update csv-pipeline-test \
    --location europe-west4 \
    --update-pypi-package "composer-csv-ingestion"
```