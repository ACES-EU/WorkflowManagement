"""Deploy hello_inout flow to Kubernetes pool using Prefect S3/MinIO storage block.

This script relies entirely on Prefect blocks and Work Pool defaults.
It does not hardcode any S3 endpoint or image; the S3 endpoint, credentials,
and other settings are taken from the storage block (e.g., 'saas-flows').
"""

from pathlib import Path
from prefect_aws.s3 import S3Bucket
from hello_flow_inout import hello_inout


if __name__ == "__main__":
    print("Deploying 'hello_inout' flow to Kubernetes work pool using S3 storage...")
    block_name = "saas-flows"
    s3 = S3Bucket.load(block_name)
    print(f"Loaded S3 block '{block_name}'")
    # Print basic info (non-secret)
    try:
        print(f"bucket='{getattr(s3, 'bucket_name', 'unknown')}', folder='{getattr(s3, 'bucket_folder', '')}'")
    except Exception as ex:
        print("  (failed to read bucket info from block)")
        raise ex

    # Upload the flow file to a subfolder
    local = str(Path(__file__).parent / "hello_flow_inout.py")
    remote = "hello-flow-inout/hello_flow_inout.py"  # relative to the 'flows' folder of the block
    s3.upload_from_path(from_path=local, to_path=remote)

    # Deploy the flow so workers pull code from S3
    hello_inout.from_source(
        source=s3,
        entrypoint="hello-flow-inout/hello_flow_inout.py:hello_inout",
    ).deploy(
        name="hello-flow-inout-s3",
        work_pool_name="aces",
    )
