# ACES Workflow Orchestrator

## Installation

### Prerequisites

- Kubernetes cluster
- `kubectl` configured to access the cluster
- `helm` installed and configured to access the cluster

### MinIO Operator & Minio Tenant with Kustomize

Install kustomize ([see](https://kubectl.docs.kubernetes.io/installation/kustomize/)).

```shell
cd deployment/minio
```

PV folder needs the right permissions. `1000` is the user ID
that minio runs as.  `pvs/aces-tenant` folder is part of this project.

```shell
chown -R 1000:1000 /path/to/pvs/aces-tenant
chmod -R 755  /path/to/pvs/aces-tenant
```

```shell
kubectl apply -f pv.yaml
```

We need to wait for the CRDs to be ready. Hence the two-phase approach:

Phase 1 - Apply operator and CRDs only:

```shell
kubectl apply -f infra/operator.yaml
# Wait for CRDs to be ready
kubectl wait --for condition=established --timeout=60s crd/tenants.minio.min.io
```

Phase 2 - Apply the tenant:

```shell
 kubectl apply -f infra/aces-tenant.yaml
```

Use `mc` to create the `prefect` bucket and set it to public.

```shell
cd mc/
kubectl apply -f job.yaml
```

MinIO credentials are set to `admin/martel2024`.

### Deploy Prefect Server

This deploys Prefect server and PostgreSQL.

```shell
cd deployment/prefect
./deploy-prefect-server.sh
```

Forward the port to access the Prefect from outside the cluster.

```shell
kubectl -n prefect port-forward svc/prefect-server 4200:4200 --address=0.0.0.0
```

To validate Prefect is avialable, run

```shell
export PREFECT_API_URL="http://<hostname|IP>:4200/api"
prefect version
```

To access UI create a tunnel to the Prefect server. From your local machine, run

```shell
ssh -L 4200:localhost:4200 root@<hostname|IP> -N

```

Then, from your local machine, access the Prefect UI at `http://localhost:4200`.

### Set up Prefect Block K8SJob and Workpool

```shell
cd deployment/prefect/set_prefect_scripts
kubectl apply -f deployment.yaml
```

### Install Prefect Agent

From `deployment/prefect`, run

```shell
helm install prefect-agent --namespace prefect prefect/prefect-agent -f values.yaml
```

## Deploy IPTO flows in ACES Workflow Orchestrator

### UC1 - Load Sensitivity Analysis

```shell
prefect deployment build uc1_prefect/flow.py:uc1_load_sens -n 'uc1_load_sens' -ib kubernetes-job/prod -sb 'remote-file-system/minio' --pool aces
prefect deployment apply uc1_load_sens-deployment.yaml
```
