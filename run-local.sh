#!/bin/bash

set -euo pipefail

# 1. clean up the old clusters
kind delete cluster --name learning

# 2. build our app
cd app && docker build -t k8s-hello:v1 . && cd ..

# 3. create the cluster
kind create cluster --name learning

# 4. load the image
kind load docker-image k8s-hello:v1 --name learning

# 5. deploy everything
kubectl apply -f k8s/

sleep 5
# 6. wait for it to be ready
echo "Waiting for our pods"
kubectl wait --for=condition=ready pod -l app=hello --timeout=90s

# 7. start our tunnel
echo "live at http://localhost:8081"
kubectl port-forward svc/hello-service 8081:80
