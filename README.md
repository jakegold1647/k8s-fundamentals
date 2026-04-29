# Local Kubernetes Development Environment
A technical project documenting containerization of a Python application within a local Kubernetes cluster.

---

## Overview
This project demonstrates the workflow needed to move a local Python application into a managed, distributed environment. It focuses on the practical application of immutability.

---

## Tech Stack
- **Language:** Python 3.11 / Flask
- **Containerization:** Docker Desktop
- **Orchestration:** Kubernetes (v1.30)
- **Local Cluster:** 'kind' (Kubernetes thru Docker)

---

## System Components
The infrastructure is defined by three primary Kubernetes manfifests located inside of the '/k8s' directory:

1. **Deployment:** Configured to maintain a desired state of **3 replicas** It manages the lifecyle of the application pods.
2. **Service (ClusterIP):** Acts as a stable internal entry point. It performs round-robin load balancing across all healthy pods.
3. **ConfigMap:** Externalizes application configuration (the greeting), allowing for runtime updates without code changes.

---

## Automation Workflow
The project includes a 'run-local.sh' script to automate the environment bootstrap and ensure reprioducibility:

1. **Cleanup:** Deletes existing clusters to ensure a deterministic environment.
2. **Build:** Compiles the docker image into the local Dockerfile
3. **Sideloader:** Pushes the lcoal image directly into the 'kind' nodes to bypass external registry requirements.
4. **Synchronization:** Uses 'kubectl wait' to ensure all pods have passed health check before proceeding
5. **Networking:** Establishes a 'port-forward' bridge from the host machine to the internal service.

---


## Technical Observations
- **Immutability:** Verified the running pods are static artifacts. Code updates require a full rebuild a rolling deployment to take effect. 
- **Self-Healing:** Observed the Kubernetes Control Plane automatically detecting pod deletion and provisioning new instances to maintain the definwed 3-replica count.
- **Service Discovery:** Confirmed that the service succesfully abstracts pod IP addresses, providing a single stable DNS/IP for the application.
- **Troubleshooting:** Utilized 'kubectl logs' to identify and resolve runtime errors in Python code.

---

## How to run
1. Ensure **Docker Desktop and **kind** are installed and running on WSL 2.
2. Execute the boostrap script:
    ```bash
    ./run-local.sh