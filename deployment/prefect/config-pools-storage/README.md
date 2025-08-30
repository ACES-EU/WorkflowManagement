# Set up Prefect Storage Blocks and Work Pool

To configure the Prefect Storage Blocks and Work Pool, you need to collect the
deployed Prefect's API URL and the MinIO storage endpoint, and then run

```shell
pip install -r requirements.txt
./run.sh <PREFECT_API_URL> <MINIO_STORAGE_URL>
```

Where, 
- `<PREFECT_API_URL>` is the URL of the deployed Prefect API and the service 
  will be contacted from the script. 
- `<MINIO_STORAGE_URL>` is the public URL of the Cloud MinIO storage service;
  it will be configured in Prefect; it will not be contacted from the script.

For example:

```shell
pip install -r requirements.txt
./run.sh http://159.100.254.17:4200/api https://159.100.254.17:3443
```

This will create:

- Work pool named `aces` for Kubernetes jobs.
- MinIO storage blocks for flow code, data, results, and cache.
