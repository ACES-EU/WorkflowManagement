# ACES Workflow Orchestrator
### Installation Process
1. `Minio Operator & Minio Tenant with Kustomize`
   - need to install kustomize (check homebrew installation)
   - cd /mlfo/minio
   - kubectl apply -f pv.yaml
   - kustomize build infra | kubectl apply -f -
   - cd /mc
   - kubectl apply -f .
   - Minio credentials admin/martel2024
2. `Install Prefect Server`
    - cd config/prefect
    - bash make_server.sh
    - kubectl port-forward svc/prefect-server 4200:4200 --address=0.0.0.0
3. `Set up Prefect Block K8SJob and Workpool`
    - cd config/prefect/set_prefect_scripts
    - kubectl apply -f deployment.yaml
4. `Install Prefect Agent`
    - helm install prefect-agent prefect/prefect-agent -f values.yaml

### Deploy IPTO flows in ACES Workflow Orchestrator
#### UC1 - Load Sensitivity Analysis
```
prefect deployment build uc1_prefect/flow.py:uc1_load_sens -n 'uc1_load_sens' -ib kubernetes-job/prod -sb 'remote-file-system/minio' --pool aces
prefect deployment apply uc1_load_sens-deployment.yaml
```