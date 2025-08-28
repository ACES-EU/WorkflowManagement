import asyncio
import os
from prefect.client.orchestration import get_client
from prefect.client.schemas.actions import WorkPoolCreate, WorkPoolUpdate

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


async def create_or_update_work_pool():
    """
    Create or update the Kubernetes work pool using the server's default base job template
    and modify only required variables (no local JSON file).
    """
    print(f"Using Prefect API URL: {PREFECT_API_URL}")
    async with get_client() as client:
        # Fetch default base job template for kubernetes
        resp = await client._client.get(
            "/work_pools/default-base-job-template", params={"type": "kubernetes"}
        )
        resp.raise_for_status()
        base_job_template = resp.json()

        # Apply minimal defaults to variables
        props = base_job_template.get("variables", {}).get("properties", {})
        if isinstance(props.get("namespace"), dict):
            props["namespace"]["default"] = "prefect"
        if isinstance(props.get("service_account_name"), dict):
            props["service_account_name"]["default"] = "prefect-worker"
        if isinstance(props.get("env"), dict):
            env_default = props["env"].get("default")
            if not isinstance(env_default, dict):
                env_default = {}
            env_default["EXTRA_PIP_PACKAGES"] = "prefect-aws boto3"
            props["env"]["default"] = env_default

        try:
            wp = await client.create_work_pool(
                WorkPoolCreate(
                    name=WORK_POOL_NAME,
                    type="kubernetes",
                    description="ACES Kubernetes work pool for edge computing workflows",
                    is_paused=False,
                    base_job_template=base_job_template,
                )
            )
            print(f"Work pool '{wp.name}' created successfully!")
            return wp
        except Exception as e:
            msg = str(e)
            if _is_already_exists_error(msg) or type(e).__name__ == "ObjectAlreadyExists":
                print("Work pool already exists; updating base job template...")
                await client.update_work_pool(
                    work_pool_name=WORK_POOL_NAME,
                    work_pool=WorkPoolUpdate(base_job_template=base_job_template),
                )
                print("Work pool updated successfully.")
                return await client.read_work_pool(WORK_POOL_NAME)
            raise


def main():
    """Run the work pool creation."""
    try:
        print("Creating/updating work pool using server default base job template...")
        result = asyncio.run(create_or_update_work_pool())
        if result is None:
            print("Work pool is ready (created previously).")
        else:
            print("Work pool created/updated successfully!")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        print(f"Unexpected error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
