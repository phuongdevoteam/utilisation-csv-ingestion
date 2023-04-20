# utilisation-csv-ingestion

#### Install the package locally
```
pip install --index-url https://europe-west4-python.pkg.dev/pj-composer-csv-ingestion/composer-csv-ingestion/simple/ composer-csv-ingestion
```

#### Install the package on Cloud Composer
```
gcloud composer environments update csv-pipeline-test \
    --location europe-west4 \
    --update-pypi-package "--index-url https://europe-west4-python.pkg.dev/pj-composer-csv-ingestion/composer-csv-ingestion/simple/ composer-csv-ingestion"
```