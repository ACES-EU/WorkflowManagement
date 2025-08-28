# hello-flow-inout

This Prefect flow reads the name from S3 and writes a greeting to S3 while also
printing to stdout.

## Behavior

- Reads `input/input.txt` from the S3 block named by `$PREFECT_INPUT_S3_BLOCK` (default: `saas-data`).
- Prints `Hello, {name}!` to stdout.
- Writes the same line to `output/output.txt` in the S3 block named by `$PREFECT_OUTPUT_S3_BLOCK` (default: `saas-results`).

## Assumptions

- MinIO-backed S3 blocks already exist (created by the repo's setup scripts):
  - AwsCredentials: `minio-credentials-cloud`
  - S3 bucket: `saas-data` (for inputs)
  - S3 bucket: `saas-results` (for outputs)

## Create deployment and run it, and download results

If using Prefect server, set `PREFECT_API_URL`.

Ensure S3 objects exist: upload `input/input.txt` under the `saas-data` block path.

```bash
$ cat >input.txt<<EOF
ACES
EOF
$ mc --insecure cp input.txt aces/prefect/input/input.txt
```

Run to deploy:

```bash
python deploy_hello_flow_inout.py
```

```bash
prefect deployment run 'hello-inout/hello-flow-inout-s3'
```

Download and view results:

```bash
$ mc --insecure cp aces/prefect/output/output.txt output.txt
$ cat output.txt
Hello, ACES!
```
