"""Deploy hello flow to Kubernetes pool using Prefect S3/MinIO storage block.

This script relies entirely on your Prefect Blocks and Work Pool defaults.
It does not hardcode any S3 endpoint or image; the S3 endpoint, credentials,
and other settings are taken from the storage block (e.g., 'minio-flows').
"""

import os
from pathlib import Path
from prefect_aws import S3Bucket
from hello_k8s import hello


if __name__ == "__main__":
    print("Deploying 'hello' flow to Kubernetes work pool using S3 storage...")
    block_name = "saas-flows"
    s3 = S3Bucket.load("saas-flows")
    print(f"Loaded S3 block '{block_name}'")
    # Print basic info (non-secret)
    try:
        print(f"bucket='{s3.bucket_name}', folder='{s3.bucket_folder}'")
    except Exception as ex:
        print("  (failed to read bucket info from block)")
        raise ex

    # Upload the flow file to a subfolder
    local = Path(__file__).parent / "hello_k8s.py"
    remote = "hello-k8s/hello_k8s.py"  # relative to the 'flows' folder
    s3.upload_from_path(from_path=str(local), to_path=remote)

    # Deploy the flow so workers pull code from S3
    hello.from_source(
        source=s3,
        entrypoint="hello-k8s/hello_k8s.py:hello",
    ).deploy(
        name="hello-k8s-s3",
        work_pool_name="aces",
        # No image/env here; rely on Work Pool base job template
    )
