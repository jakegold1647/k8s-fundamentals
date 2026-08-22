# Local Kubernetes Lab

A Flask app running on a local Kubernetes cluster, built to learn how the pieces
actually behave rather than to ship anything. One script brings the whole
environment up from nothing.

## Stack

- Python 3.11 / Flask
- Docker Desktop
- Kubernetes v1.30
- kind (Kubernetes in Docker), running on WSL 2

## What's in here

Three manifests in `k8s/`:

| File | What it does |
|---|---|
| `deployment.yaml` | Holds 3 replicas and manages the pod lifecycle |
| `service.yaml` | ClusterIP — stable internal address, round-robins across healthy pods |
| `configmap.yaml` | Externalizes the greeting string so it changes without a rebuild |

The app (`app/main.py`) returns its own hostname on `/`, which is how you see the
Service load-balancing across pods, and answers `/health` for the readiness check.

## Running it

Docker Desktop and kind need to be installed and running under WSL 2.

```bash
./run-local.sh
```

Then hit `http://localhost:8081` a few times — the hostname in the response
changes as the Service distributes requests.

`run-local.sh` does seven things, in order:

1. **Cleanup** — deletes any existing cluster, so every run starts from the same state
2. **Build** — builds the image from `app/Dockerfile`
3. **Create** — starts a fresh kind cluster named `learning`
4. **Sideload** — loads the image straight into the kind nodes, skipping a registry
5. **Deploy** — applies the ConfigMap, Deployment, and Service manifests
6. **Wait** — `kubectl wait` blocks until pods pass their health check
7. **Forward** — opens a `port-forward` from port 8081 on the host to the Service

Step 6 matters more than it looks. Without it the port-forward races the pods and
fails intermittently, which is a confusing thing to debug the first time.

## What I took away from it

**Pods are immutable.** Editing the Python source changes nothing until you
rebuild the image and roll the deployment. Obvious in hindsight; not obvious when
you're wondering why your change didn't show up.

**Self-healing is fast.** Delete a pod with `kubectl delete pod` and the control
plane has a replacement running before you can check — the deployment holds at 3
replicas regardless.

**The Service is the stable thing, not the pods.** Pod IPs churn. The ClusterIP
doesn't, which is the whole point of the abstraction.

**`kubectl logs` is the first stop.** Every runtime error I hit in the Flask code
surfaced there before anywhere else.
