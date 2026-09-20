# NVIDIA device plugin (K3s)

Exposes node GPUs to pods as `nvidia.com/gpu`. Used by `k3s/apps/onyx/model-server.yaml`.

## Prerequisites (on each GPU node)

- NVIDIA drivers + `nvidia-container-toolkit`
- containerd configured with the `nvidia` runtime (RuntimeClass `nvidia` below
  expects a handler named `nvidia`)
- Label the node: `kubectl label node <gpu-node> gpu=nvidia`

## Deploy

```bash
kubectl apply -f k3s/configs/nvidia-device-plugin/daemonset.yaml
kubectl get nodes -l gpu=nvidia -o jsonpath='{.items[*].status.allocatable.nvidia\.com/gpu}{"\n"}'
# smoke test (delete the pod afterwards):
kubectl apply -f k3s/configs/nvidia-device-plugin/smoke-nvidia-smi.yaml
kubectl logs -n kube-system nvidia-smi-smoke
kubectl delete pod -n kube-system nvidia-smi-smoke
```
