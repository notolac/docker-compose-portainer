# Prometheus + Grafana + Loki (node monitoring)

Metrics and logs stack for one monitored host, plus a lightweight client variant.

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `node-monitor.yaml` | Compose standalone | Prometheus + Grafana + Loki + node-exporter/cadvisor (see YAML header) |
| `client-minitor.yaml` | Compose standalone | Minimal Prometheus for a secondary host |
| `prometheus.yml` | Config sample | Example scrape config — **adjust targets/labels to your hosts** |

## Deploy

```bash
docker compose -f node-monitor.yaml up -d
```

Create the data directories and your `prometheus.yml` from the sample first
(required env: `PROMETHEUS_DATA_DIR`, `GRAFANA_DATA_DIR`, `LOKI_DATA_DIR`,
host ports — see the YAML header).

## Data directories: pin them before the first redeploy

Volume defaults live under `/opt/node-monitor-grafana/*` (`PROMETHEUS_DATA_DIR`,
`GRAFANA_DATA_DIR`, `LOKI_DATA_DIR`; config files via `PROMETHEUS_CONFIG_FILE`,
`LOKI_CONFIG_FILE`, `GRAFANA_DATASOURCES_FILE`). If the host already keeps data
in another path, set those variables in the stack Environment **before** the
first redeploy. If a bind source is missing, Docker creates it as an empty
root-owned directory and prometheus/loki/grafana exit with `permission denied`.
