# Portainer (K3s UI)

Cluster UI for the K3s cluster itself (plus optional Docker agents).
Traefik exposes it; Authentik can gate it (see
[`../traefik/`](../traefik/) and [`../../docs/ingress-traefik.md`](../../docs/ingress-traefik.md)).

- Chart: `portainer/portainer` (pin a version at install: `helm search repo portainer/portainer`)
- `portainer-values.yaml` — Helm values template (placeholders only, no secrets)

> **Portainer 3:** per the
> [3.0 announcement](https://www.portainer.io/blog/portainer-3-0-is-coming),
> 3.x starts as STS, is Kubernetes-first, and ships **no separate CE build**
> (free via 3 Nodes Free instead); CE stays on the 2.x codebase. The values
> below track 3.x via the floating `sts` image tag — pin an exact version
> once you validate one. Automation against the current API:
> [API docs (EE 2.45.1)](https://api-docs.portainer.io/?edition=ee&version=2.45.1).

## Install

```bash
helm repo add portainer https://portainer.github.io/k8s/
helm repo update

# Copy values first and set YOUR LoadBalancer IP + StorageClass
cp k3s/helm/portainer/portainer-values.yaml my-portainer-values.yaml
helm upgrade --install portainer portainer/portainer \
  -n portainer --create-namespace \
  -f my-portainer-values.yaml

# Reach the UI at YOUR LoadBalancer IP (or the Traefik router below),
# create the admin user, add the in-cluster Kubernetes environment.
kubectl get svc -n portainer
```

## Exposing via Traefik

Portainer serves HTTPS on `:9443` with its own certificate, so the
file-provider Service must use `https://` + `insecureSkipVerify`
(see `dynamic-app-example.yaml` in [`../traefik/`](../traefik/) and
[`../../docs/ingress-traefik.md`](../../docs/ingress-traefik.md)):

```yaml
services:
  portainer-svc:
    loadBalancer:
      passHostHeader: true
      servers:
        - url: "https://portainer.portainer.svc.cluster.local:9443"
      serversTransport: portainer-transport
serversTransports:
  portainer-transport:
    insecureSkipVerify: true
```

## Agents

The server tag and the `portainer/agent` tag on external Docker hosts
must match (see [upstream docs](https://docs.portainer.io/)). Keep them
pinned to the same version you install here.

## Secrets / state

The license and environments live in the Portainer PVC (`existingClaim`
in the values). Back it up before upgrades; never commit its contents.
No passwords or tokens belong in this folder.
