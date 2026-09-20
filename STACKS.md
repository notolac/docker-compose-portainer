# Stack catalog

Index of all deployable stacks in this repository. Docker stacks live under
[`docker/`](docker/) — each folder contains one or more YAML manifests and optional
documentation. Generic K3s manifests live under [`k3s/apps/`](k3s/apps/)
(see [`k3s/README.md`](k3s/README.md); apps are migrating gradually).

Each `docker/` service folder contains a `<service>.md` sheet describing the
service, its files, deploy steps and variables.

**Legend:** `standalone` = single-host Docker Compose · `swarm` = Docker Swarm stack · `gpu` = requires NVIDIA or AMD GPU passthrough

## Applications

| Service | Folder | Variants | Notes |
|---------|--------|----------|-------|
| Audiobookshelf | [audiobookshelf/](docker/audiobookshelf/) | standalone | Audiobooks and podcasts |
| Authentik | [authentik/](docker/authentik/) | standalone | Identity provider (SSO) |
| Calibre Web | [calibre-web/](docker/calibre-web/) | standalone | E-book library |
| Checkmk | [checkmk/](docker/checkmk/) | standalone | Monitoring |
| Cloudflare DDNS | [cloudflare-ddns/](docker/cloudflare-ddns/) | standalone | Dynamic DNS updater |
| Coolify | [coolify/](docker/coolify/) | standalone | PaaS / app deployment |
| Dockge | [dockge/](docker/dockge/) | standalone | Compose stack manager |
| Firefly III | [firefly-III/](docker/firefly-III/) | standalone, swarm | Personal finance |
| Ghost | [ghost/](docker/ghost/) | standalone | Blog CMS (legacy; consider upstream alternatives) |
| GitLab CE | [gitlab-docker-ce/](docker/gitlab-docker-ce/) | standalone | Git + CI |
| Home Assistant | [home-assistant/](docker/home-assistant/) | standalone | Home automation |
| Homarr | [homarr/](docker/homarr/) | standalone, swarm | Dashboard |
| Jenkins | [jenkins/](docker/jenkins/) | standalone | CI/CD |
| JDownloader 2 | [jdownloader-2/](docker/jdownloader-2/) | standalone | Download manager |
| KMS (py-kms) | [kms-python/](docker/kms-python/) | standalone | Volume activation |
| Linkding | [linkding_app/](docker/linkding_app/) | standalone, swarm | Bookmark manager |
| Mealie | [mealie/](docker/mealie/) | standalone, swarm | Recipe manager |
| n8n | [n8n/](docker/n8n/) | standalone | Workflow automation |
| Netboot.xyz | [netbootxyz/](docker/netbootxyz/) | standalone | Network boot |
| Netdata | [netdata-docker/](docker/netdata-docker/) | standalone, gpu | Host monitoring |
| No-IP DDNS | [noip-ddns/](docker/noip-ddns/) | standalone | Dynamic DNS |
| Odoo | [odoo/](docker/odoo/) | standalone | ERP |
| OpenSpeedTest | [openspeedtest/](docker/openspeedtest/) | standalone | Speed test |
| PhotoPrism | [photoprisma/](docker/photoprisma/) | standalone, gpu | Photo management |
| RustDesk | [rustdesk/](docker/rustdesk/) | standalone | Remote desktop |
| Semaphore | [ansible-semaphore/](docker/ansible-semaphore/) | standalone | Ansible UI |
| Snipe-IT | [snipeit/](docker/snipeit/) | standalone, swarm | Asset management |
| Speedtest Tracker | [speedtest-tracker/](docker/speedtest-tracker/) | standalone | ISP speed history |
| Traefik | [traefik/](docker/traefik/) | standalone | Reverse proxy |
| Uptime Kuma | [uptime-kuma/](docker/uptime-kuma/) | standalone | Uptime monitoring |
| Vaultwarden | [vaultwarden/](docker/vaultwarden/) | standalone, swarm | Password manager |
| Wallos | [wallos-app/](docker/wallos-app/) | standalone, swarm | Subscription tracker |
| wg-easy | [wg-easy-vpn/](docker/wg-easy-vpn/) | standalone | WireGuard VPN UI |
| WordPress | [wordpress/](docker/wordpress/) | standalone, swarm | CMS |

## Media automation

| Service | Folder | Variants | Notes |
|---------|--------|----------|-------|
| *arr stack (Prowlarr, Radarr, Sonarr, Lidarr, qBittorrent) | [automated-multimedia-server/](docker/automated-multimedia-server/) | standalone | See [README](docker/automated-multimedia-server/README.md) |
| Tdarr | [automated-multimedia-server/](docker/automated-multimedia-server/) | amd, nvidia | Transcoding |
| Python utilities | [automated-multimedia-server/](docker/automated-multimedia-server/) | scripts | Plex helpers (optional) |

## AI / LLM

| Service | Folder | Variants | Notes |
|---------|--------|----------|-------|
| Onyx | [local_llm/](docker/local_llm/) | standalone, swarm, nvidia, amd | RAG / document Q&A — see [local_llm.md](docker/local_llm/local_llm.md) |
| LiteLLM | [local_llm/](docker/local_llm/) | standalone, swarm | LLM proxy (OpenAI-compatible) |
| Bifrost | [local_llm/](docker/local_llm/) | standalone | LLM gateway (concept only, untested) |

## Infrastructure / observability

| Service | Folder | Variants | Notes |
|---------|--------|----------|-------|
| Nginx Proxy Manager + GoAccess | [nginx-proxy-manager-goaccess/](docker/nginx-proxy-manager-goaccess/) | standalone | Reverse proxy + log analytics |
| Node monitor (Prometheus + Grafana) | [node-monitor-grafana/](docker/node-monitor-grafana/) | standalone | Basic metrics |
| rclone sync | [rclone/](docker/rclone/) | standalone | Cloud backup via Portainer env (`RCLONE_*` / path vars) — see [README](docker/rclone/README.md) |

## K3s

Generic Kubernetes manifests under [`k3s/apps/`](k3s/apps/) (see [`k3s/README.md`](k3s/README.md)).
Shared cluster examples (placement, Rook StorageClass, MetalLB pool, NVIDIA plugin)
live under [`k3s/configs/`](k3s/configs/).

| Service | Folder | Stack |
|---------|--------|-------|
| Firefly III | [firefly/](k3s/apps/firefly/) | App + PostgreSQL + importer + cron |
| Homarr | [homarr/](k3s/apps/homarr/) | App + PVC |
| Linkding | [linkding/](k3s/apps/linkding/) | App + PVC |
| LiteLLM | [litellm/](k3s/apps/litellm/) | Proxy + PostgreSQL + Redis |
| Mealie | [mealie/](k3s/apps/mealie/) | App + PVC (SQLite) |
| n8n | [n8n/](k3s/apps/n8n/) | App + runners sidecar + PostgreSQL |
| Odoo | [odoo/](k3s/apps/odoo/) | App + PostgreSQL |
| Onyx | [onyx/](k3s/apps/onyx/) | API + web + nginx + Postgres + Vespa + OpenSearch + MinIO + GPU model servers |
| Vaultwarden | [vaultwarden/](k3s/apps/vaultwarden/) | App + PVC |
| Wallos | [wallos/](k3s/apps/wallos/) | App + PVCs |

Cluster infrastructure (Helm releases under [`k3s/helm/`](k3s/helm/)).
Publishing guide: [`k3s/docs/ingress-traefik.md`](k3s/docs/ingress-traefik.md).

| Release | Folder | Chart |
|---------|--------|-------|
| Traefik (ingress) | [traefik/](k3s/helm/traefik/) | `traefik/traefik` |
| Authentik (SSO) | [authentik/](k3s/helm/authentik/) | `authentik/authentik` |
| Portainer (cluster UI) | [portainer/](k3s/helm/portainer/) | `portainer/portainer` |

## Choosing standalone vs Swarm

| Use standalone when… | Use Swarm when… |
|----------------------|-----------------|
| Single Docker host | Multi-node cluster with shared storage |
| Simple bind mounts under `/opt/…` | Need replicated services across nodes |
| Learning / homelab on one machine | Production-like HA on several nodes |

Swarm stacks use `${SHARED_DATA_ROOT:-/opt}` or per-service path variables instead of cluster-specific mount points. Set the same paths on every Swarm node that runs the service.

## Environment files

| Pattern | Purpose |
|---------|---------|
| `.env.example` | Committed template — copy to `.env` locally |
| Portainer env vars | Same keys as `.env.example`, set in the stack UI |
| Docker Swarm secrets | Used by some stacks (Firefly III swarm, etc.) |

Never commit files containing real passwords, API keys, or personal domains.
