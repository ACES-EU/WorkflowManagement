#!/usr/bin/env bash

helm repo add prefect https://prefecthq.github.io/prefect-helm

helm install prefect-server prefect/prefect-server \
  --namespace prefect --create-namespace \
  --set postgresql.auth.username=prefect \
  --set postgresql.auth.password=prefect

kubectl wait --namespace prefect \
  --for=condition=Ready pod \
  -l app.kubernetes.io/name=prefect-server \
  --timeout=300s
