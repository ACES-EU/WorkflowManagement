from prefect import flow

@flow
def hello():
    print("Hello from Prefect!")

if __name__ == "__main__":
    hello()
