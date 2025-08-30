#!/usr/bin/env python3
"""
Script to setup MinIO storage for Prefect workflows.

This script provides a complete setup for MinIO integration with Prefect:
1. Creates all MinIO storage blocks
2. Configures work pool storage
3. Sets up default result storage
4. Provides validation and testing utilities

Run this script to get a fully configured MinIO + Prefect environment.
"""

import os
import subprocess
import sys
from pathlib import Path

from prefect_aws import S3Bucket, AwsCredentials, AwsClientParameters


# Configure Prefect API URL from environment or use default
PREFECT_API_URL = os.getenv("PREFECT_API_URL", "http://localhost:4200/api")

# MinIO configuration
MINIO_KEY = 'admin'
MINIO_SECRET = 'martel2024'

MINIO_PREFECT_BUCKET = 'prefect'

CLOUD_MINIO_ENDPOINT = os.environ['CLOUD_MINIO_ENDPOINT']

EDGE_MINIO_HOST = 'minio.minio-operator.svc.cluster.local'
EDGE_MINIO_PORT = 80
EDGE_MINIO_ENDPOINT = f"https://{EDGE_MINIO_HOST}:{EDGE_MINIO_PORT}"

def create_aws_credentials_cloud():
    """Create AWS credentials block for MinIO on Cloud"""
    print("Creating AWS credentials for MinIO on Cloud...")
    try:
        client_params = AwsClientParameters(
            endpoint_url=CLOUD_MINIO_ENDPOINT,
            use_ssl=CLOUD_MINIO_ENDPOINT.startswith("https://"),
            verify=False,
        )
        credentials = AwsCredentials(
            aws_access_key_id=MINIO_KEY,
            aws_secret_access_key=MINIO_SECRET,
            region_name="us-east-1",  # Required by AWS SDK
            aws_client_parameters=client_params,
        )
        credentials.save("minio-credentials-cloud", overwrite=True)
        print("AWS credentials block for MinIO on Cloud created successfully")
        return credentials
    except Exception as e:
        print(f"Failed to create AWS credentials block: {e}")
        print("Please ensure:")
        print(f"1. Prefect server is running at {PREFECT_API_URL}")
        print("2. Network connectivity is available")
        raise

def create_aws_credentials_edge():
    """Create AWS credentials block for MinIO on Edge"""
    print("Creating AWS credentials for MinIO on Edge...")
    try:
        client_params = AwsClientParameters(
            endpoint_url=EDGE_MINIO_ENDPOINT,
            use_ssl=EDGE_MINIO_ENDPOINT.startswith("https://"),
            verify=False,
        )
        credentials = AwsCredentials(
            aws_access_key_id=MINIO_KEY,
            aws_secret_access_key=MINIO_SECRET,
            region_name="us-east-1",  # Required by AWS SDK
            aws_client_parameters=client_params,
        )
        credentials.save("minio-credentials-edge", overwrite=True)
        print("AWS credentials block for MinIO on Edge created successfully")
        return credentials
    except Exception as e:
        print(f"Failed to create AWS credentials block: {e}")
        print("Please ensure:")
        print(f"1. Prefect server is running at {PREFECT_API_URL}")
        print("2. Network connectivity is available")
        raise

def create_storage_blocks():
    """Create storage blocks for different purposes"""
    credentials_cloud = create_aws_credentials_cloud()
    credentials_edge = create_aws_credentials_edge()

    # 1. Flow code storage (replaces deployment configs in /param)
    print("Creating flow storage block...")
    flow_storage = S3Bucket(
        bucket_name=MINIO_PREFECT_BUCKET,
        folder="flows",
        credentials=credentials_cloud,
    )
    flow_storage.save("saas-flows", overwrite=True)
    print("Flow storage block created: s3://prefect/flows/")
    
    # 2. Data storage (for input datasets)
    print("Creating data storage block...")
    data_storage = S3Bucket(
        bucket_name=MINIO_PREFECT_BUCKET,
        folder="data",
        credentials=credentials_cloud,
    )
    data_storage.save("saas-data", overwrite=True)
    print("Data storage block created: s3://prefect/data/")
    
    # 3. Results storage (for outputs, figures, CSVs)
    print("Creating results storage block...")
    results_storage = S3Bucket(
        bucket_name=MINIO_PREFECT_BUCKET,
        folder="results",
        credentials=credentials_cloud,
    )
    results_storage.save("saas-results", overwrite=True)
    print("Results storage block created: s3://prefect/results/")

    # 4. Cache storage (for intermediate results)
    print("Creating cache storage block...")
    cache_storage = S3Bucket(
        bucket_name=MINIO_PREFECT_BUCKET,
        folder="cache",
        credentials=credentials_edge,
    )
    cache_storage.save("edge-cache", overwrite=True)
    print("Cache storage block created: s3://prefect/cache/")

    print("-" * 60)
    print("All MinIO storage blocks created successfully!")
    print("\nAvailable storage blocks:")
    print("  - minio-credentials  - AWS credentials for MinIO")
    print("  - saas-flows        - Flow code and deployments (s3://prefect/flows/)")
    print("  - saas-data         - Input data files (s3://prefect/data/)")
    print("  - saas-results      - Output files and results (s3://prefect/results/)")
    print("  - edge-cache        - Cache files (s3://prefect/cache/)")
    
    print("\nRecommended directory structure:")
    print("  s3://prefect/")
    print("  ├── flows/           # Deployment YAML files, flow scripts")
    print("  ├── data/            # Input datasets, CSV files")
    print("  │   └── uc1/         # UC1 specific data")
    print("  ├── results/         # Generated outputs, figures")
    print("  │   └── uc1/         # UC1 specific results")
    print("  └── cache/           # intermediate results")

    return flow_storage, data_storage, results_storage, cache_storage


def configure_work_pool_storage():
    """Configure work pool to use MinIO storage"""
    print("\nConfiguring work pool storage...")
    
    try:
        # Use subprocess to run the prefect CLI command
        cmd = [
            "prefect", "work-pool", "storage", "configure", "s3", "aces",
            "--bucket", MINIO_PREFECT_BUCKET,
            "--aws-credentials-block-name", "minio-credentials"
        ]
        
        print(f"Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Work pool storage configured successfully")
        if result.stdout:
            print(f"Output: {result.stdout}")
            
    except subprocess.CalledProcessError as e:
        print(f"Work pool storage configuration failed: {e}")
        print("You can configure it manually later with:")
        print("  prefect work-pool storage configure s3 aces \\")
        print(f"    --bucket {MINIO_PREFECT_BUCKET} \\")
        print("    --aws-credentials-block-name minio-credentials")
    except FileNotFoundError:
        print("Prefect CLI not found. Install Prefect or configure work pool manually.")

def set_default_result_storage():
    """Set MinIO as default result storage"""
    print("\nSetting default result storage...")
    
    # Set environment variable for default result storage
    os.environ["PREFECT_RESULTS_DEFAULT_STORAGE_BLOCK"] = "prefect/minio-results"
    print("Default result storage set to MinIO")
    
    # Optionally write to a .env file for persistence
    env_file = Path(".env")
    env_content = "PREFECT_RESULTS_DEFAULT_STORAGE_BLOCK=prefect/minio-results\n"
    
    try:
        if env_file.exists():
            # Check if already set
            content = env_file.read_text()
            if "PREFECT_RESULTS_DEFAULT_STORAGE_BLOCK" not in content:
                with open(env_file, "a") as f:
                    f.write(env_content)
                print("Added to .env file for persistence")
        else:
            env_file.write_text(env_content)
            print("Created .env file with default storage setting")
    except Exception as e:
        print(f"Could not write to .env file: {e}")

def validate_setup():
    """Validate that all storage blocks are created and accessible"""
    print("\nValidating MinIO setup...")
    
    try:
        # Test loading each storage block
        blocks_to_test = [
            "minio-credentials",
            "saas-flows", 
            "saas-data",
            "saas-results",
            "edge-cache"
        ]
        
        for block_name in blocks_to_test:
            try:
                if block_name == "minio-credentials":
                    from prefect_aws import AwsCredentials
                    AwsCredentials.load(block_name)
                else:
                    S3Bucket.load(block_name)
                print(f"{block_name} block is accessible")
            except Exception as e:
                print(f"{block_name} block failed: {e}")
                
    except ImportError:
        print("prefect-aws not available for validation")

def print_usage_examples():
    """Print usage examples for the configured storage"""
    print("\nUsage examples in your flows:")
    print("""
# Load storage blocks
from prefect_aws import S3Bucket

# For input data
data_storage = S3Bucket.load('saas-data')
data_path = data_storage.upload_from_path('input.csv', 'uc1/input.csv')

# For results
results_storage = S3Bucket.load('saas-results') 
results_storage.upload_from_path('output.png', 'uc1/analysis.png')

# For flow code
flow_storage = S3Bucket.load('saas-flows')
flow_storage.upload_from_path('my_flow.py', 'uc1/my_flow.py')

# In flow deployment
@flow(result_storage='prefect/saas-results')
def my_flow():
    pass
""")

def main():
    """Complete MinIO setup and configuration"""
    print("Setup MinIO storage for Prefect workflows")
    print("=" * 60)
    print(f"Using Prefect API URL: {PREFECT_API_URL}")
    print(f"Cloud MinIO Endpoint: {CLOUD_MINIO_ENDPOINT}")
    print(f"Edge MinIO Endpoint: {EDGE_MINIO_ENDPOINT}")
    print(f"Bucket: {MINIO_PREFECT_BUCKET}")
    print("=" * 60)
    
    try:
        # Step 1: Create all storage blocks
        print("Step 1: Creating MinIO storage blocks...")
        create_storage_blocks()
        
        # Step 2: Configure work pool storage  
        configure_work_pool_storage()
        
        # Step 3: Set default result storage
        set_default_result_storage()
        
        # Step 4: Validate setup
        validate_setup()
        
        # Step 5: Show usage examples
        print_usage_examples()
        
        print("=" * 60)
        print("Complete MinIO setup finished successfully!")
        print("\n  What was configured:")
        print("  - MinIO storage blocks (flows, data, results, cache)")
        print("  - AWS credentials for MinIO")
        print("  - Work pool storage (if possible)")
        print("  - Default result storage")
 
        print("\n  Next steps:")
        print("  1. Create and run your Prefect flows")
        print("  2. Deploy flows with: flow.deploy(work_pool_name='aces')")
        print("  3. Monitor flows in Prefect UI")
 
    except Exception as e:
        print(f"Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
