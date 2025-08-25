import asyncio
import os
import subprocess
from prefect.client.orchestration import get_client
from prefect.client.schemas.actions import WorkPoolCreate

# Configure Prefect API URL from environment or use default
PREFECT_API_URL = os.getenv("PREFECT_API_URL", "http://localhost:4200/api")

WORK_POOL_NAME = "aces"

def _is_already_exists_error(err_msg: str) -> bool:
    """Best-effort detection for 'already exists' errors across Prefect versions/CLI."""
    if not err_msg:
        return False
    msg = err_msg.lower()
    return (
        "already exists" in msg
        or "objectalreadyexists" in msg
        or "409" in msg  # HTTP 409 conflict often used for existing objects
    )


def create_work_pool_cli():
    """
    Create a Kubernetes work pool using Prefect CLI (fallback method).
    """
    print("Creating work pool using Prefect CLI...")
    try:
        cmd = ["prefect", "work-pool", "create", WORK_POOL_NAME, "--type", "kubernetes"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Work pool created successfully via CLI!")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        # Treat "already exists" as success
        stderr = e.stderr or ""
        stdout = e.stdout or ""
        if _is_already_exists_error(stderr) or _is_already_exists_error(stdout):
            print("Work pool already exists (CLI). Continuing...")
            if stdout:
                print(f"Output: {stdout}")
            if stderr and not stdout:
                print(f"CLI notice: {stderr.strip()}")
            return True
        print(f"CLI method failed: {e}")
        if stderr:
            print(f"Error output: {stderr}")
        return False
    except FileNotFoundError:
        print("Prefect CLI not found")
        return False


async def create_work_pool():
    """
    Create a Kubernetes work pool using Prefect 3.x client.
    """
    print(f"Using Prefect API URL: {PREFECT_API_URL}")
    
    try:
        async with get_client() as client:
            # Test connection first
            print("Testing connection to Prefect server...")
            health_check = await client.api_healthcheck()
            if health_check is None:
                print("Server connection successful")
            else:
                print(f"Server health check failed: {health_check}")
                raise health_check
            
            # Create work pool with simple configuration
            # Prefect will use the default Kubernetes job template
            work_pool = await client.create_work_pool(
                WorkPoolCreate(
                    name=WORK_POOL_NAME,
                    type="kubernetes",
                    description="ACES Kubernetes work pool for edge computing workflows",
                    is_paused=False,
                )
            )
            print(f"Work pool '{work_pool.name}' created successfully!")
            try:
                # Some Prefect versions may not expose these attributes; guard prints
                print(f"   Type: {getattr(work_pool, 'type', 'kubernetes')}")
                print(f"   ID: {getattr(work_pool, 'id', 'n/a')}")
            except Exception:
                pass
            return work_pool
    except Exception as e:
        # Treat "already exists" as success
        msg = str(e)
        if _is_already_exists_error(msg) or type(e).__name__ == "ObjectAlreadyExists":
            print("Work pool already exists (API). Continuing...")
            return None
        print(f"Failed to create work pool: {e}")
        print(f"Exception type: {type(e).__name__}")
        print(f"Exception args: {e.args}")
        print("Please ensure:")
        print(f"1. Prefect server is running at {PREFECT_API_URL}")
        print("2. The API URL is correct")
        print("3. Network connectivity is available")
        raise


def main():
    """Run the work pool creation."""
    try:
        # Try async API method first
        print("Attempting to create work pool using async API...")
        try:
            result = asyncio.run(create_work_pool())
            if result is None:
                print("Work pool is ready (created previously).")
            else:
                print("Work pool created successfully!")
        except Exception as e:
            print(f"API method failed: {e}")
            print("Falling back to CLI method...")
            # Try CLI method as fallback
            if create_work_pool_cli():
                print("Work pool created or already existed (CLI).")
            else:
                print("Both API and CLI methods failed")
                exit(1)
                
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Unexpected error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
