# Netdata

Real-time host monitoring ([upstream](https://www.netdata.cloud)).

## Contents

| File | Mode | GPU | Services |
| ---- | ---- | --- | -------- |
| `netdata.yaml` | Compose standalone | — | `netdata/netdata` (host networking, host mounts, Docker socket) |
| `netdata-nvidia.yaml` | Compose standalone | NVIDIA | Same plus NVIDIA GPU metrics |

## Deploy

```bash
docker compose -f netdata.yaml up -d
# or, on NVIDIA hosts:
docker compose -f netdata-nvidia.yaml up -d
```

Dashboard on port `19999`. The container needs broad host access (`pid: host`,
`SYS_PTRACE`/`SYS_ADMIN`, host mounts) — that is expected for this agent.
