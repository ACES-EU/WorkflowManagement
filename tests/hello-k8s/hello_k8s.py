from prefect import flow

@flow(log_prints=True)
def hello(name: str = "world"):
    print(f"Hello {name} from Kubernetes!")
