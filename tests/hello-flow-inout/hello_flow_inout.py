import os
from pathlib import Path
from prefect import flow, task
from prefect_aws.s3 import S3Bucket

# Contract
# Inputs: input.txt in S3 at prefix input/, containing a single name on the first line
# Outputs: prints "Hello, {name}!" to stdout and writes the same line to S3 at output/output.txt
# Assumptions: An S3 block exists pointing to MinIO (e.g., "saas-data" for input 
# and "saas-results" for output), created by setup scripts.

INPUT_BLOCK_NAME = os.getenv("PREFECT_INPUT_S3_BLOCK", "saas-data")
OUTPUT_BLOCK_NAME = os.getenv("PREFECT_OUTPUT_S3_BLOCK", "saas-results")
INPUT_KEY = os.getenv("HELLO_INPUT_KEY", "input/input.txt")
OUTPUT_KEY = os.getenv("HELLO_OUTPUT_KEY", "output/output.txt")


@task
def read_name_from_s3() -> str:
    s3: S3Bucket = S3Bucket.load(INPUT_BLOCK_NAME)
    # Download input file to a temp path
    tmp_path = Path("/tmp/input.txt")
    s3.download_object_to_path(from_path=INPUT_KEY, to_path=str(tmp_path))
    name = tmp_path.read_text().strip().splitlines()[0]
    return name


@task
def write_output_to_s3(line: str) -> None:
    s3: S3Bucket = S3Bucket.load(OUTPUT_BLOCK_NAME)
    tmp_path = Path("/tmp/output.txt")
    tmp_path.write_text(line + "\n", encoding="utf-8")
    # Upload
    s3.upload_from_path(from_path=str(tmp_path), to_path=OUTPUT_KEY)


@flow(log_prints=True)
def hello_inout() -> str:
    name = read_name_from_s3()
    message = f"Hello, {name}!"
    print(message)
    write_output_to_s3.submit(message)  # do upload asynchronously
    return message


if __name__ == "__main__":
    # Basic local run
    _ = hello_inout()
