# Stack catalog

Index of all deployable stacks in this repository. Each folder contains one or more YAML manifests and optional documentation.

**Legend:** `standalone` = single-host Docker Compose · `swarm` = Docker Swarm stack · `gpu` = requires NVIDIA or AMD GPU passthrough

## Applications

| Service | Folder | Variants | Notes |
|---------|--------|----------|-------|
| Audiobookshelf | [audiobookshelf/](audiobookshelf/) | standalone | Audiobooks and podcasts |
| Authentik | [authentik/](authentik/) | standalone | Identity provider (SSO) |
| Calibre Web | [calibre-web/](calibre-web/) | standalone | E-book library |
| Checkmk | [checkmk/](checkmk/) | standalone | Monitoring |
| Cloudflare DDNS | [cloudflare-ddns/](cloudflare-ddns/) | standalone | Dynamic DNS updater |
| Coolify | [coolify/](coolify/) | standalone | PaaS / app deployment |
| Dockge | [dockge/](dockge/) | standalone | Compose stack manager |
| Firefly III | [firefly-III/](firefly-III/) | standalone, swarm | Personal finance |
| Ghost | [ghost/](ghost/) | standalone | Blog CMS (legacy; consider upstream alternatives) |
| GitLab CE | [gitlab-docker-ce/](gitlab-docker-ce/) | standalone | Git + CI |
| Home Assistant | [home-assistant/](home-assistant/) | standalone | Home automation |
| Homarr | [homarr/](homarr/) | standalone, swarm | Dashboard |
| Jenkins | [jenkins/](jenkins/) | standalone | CI/CD |
| JDownloader 2 | [jdownloader-2/](jdownloader-2/) | standalone | Download manager |
| KMS (py-kms) | [kms-python/](kms-python/) | standalone | Volume activation |
| Linkding | [linkding_app/](linkding_app/) | standalone, swarm | Bookmark manager |
| Mealie | [mealie/](mealie/) | standalone, swarm | Recipe manager |
| n8n | [n8n/](n8n/) | standalone | Workflow automation |
| Netboot.xyz | [netbootxyz/](netbootxyz/) | standalone | Network boot |
| Netdata | [netdata-docker/](netdata-docker/) | standalone, gpu | Host monitoring |
| No-IP DDNS | [noip-ddns/](noip-ddns/) | standalone | Dynamic DNS |
| Odoo | [odoo/](odoo/) | standalone | ERP |
| OpenSpeedTest | [openspeedtest/](openspeedtest/) | standalone | Speed test |
| PhotoPrism | [photoprisma/](photoprisma/) | standalone, gpu | Photo management |
| RustDesk | [rustdesk/](rustdesk/) | standalone | Remote desktop |
| Semaphore | [ansible-semaphore/](ansible-semaphore/) | standalone | Ansible UI |
| Snipe-IT | [snipeit/](snipeit/) | standalone, swarm | Asset management |
| Speedtest Tracker | [speedtest-tracker/](speedtest-tracker/) | standalone | ISP speed history |
| Traefik | [traefik/](traefik/) | standalone | Reverse proxy |
| Uptime Kuma | [uptime-kuma/](uptime-kuma/) | standalone | Uptime monitoring |
| Vaultwarden | [vaultwarden/](vaultwarden/) | standalone, swarm | Password manager |
| Wallos | [wallos-app/](wallos-app/) | standalone, swarm | Subscription tracker |
| wg-easy | [wg-easy-vpn/](wg-easy-vpn/) | standalone | WireGuard VPN UI |
| WordPress | [wordpress/](wordpress/) | standalone, swarm | CMS |

## Media automation

| Service | Folder | Variants | Notes |
|---------|--------|----------|-------|
| *arr stack (Prowlarr, Radarr, Sonarr, Lidarr, qBittorrent) | [automated-multimedia-server/](automated-multimedia-server/) | standalone | See [README](automated-multimedia-server/README.md) |
| Tdarr | [automated-multimedia-server/](automated-multimedia-server/) | amd, nvidia | Transcoding |
| Python utilities | [automated-multimedia-server/](automated-multimedia-server/) | scripts | Plex helpers (optional) |

## AI / LLM

| Service | Folder | Variants | Notes |
|---------|--------|----------|-------|
| Onyx | [local_llm/](local_llm/) | standalone, swarm, amd | RAG / document Q&A — see [README-onyx-swarm.md](local_llm/README-onyx-swarm.md) |
| LiteLLM + Open WebUI | [local_llm/](local_llm/) | standalone, swarm | LLM proxy + chat UI |
| Bifrost | [local_llm/](local_llm/) | standalone | LLM gateway |

## Infrastructure / observability

| Service | Folder | Variants | Notes |
|---------|--------|----------|-------|
| Nginx Proxy Manager + GoAccess | [nginx-proxy-manager-goaccess/](nginx-proxy-manager-goaccess/) | standalone | Reverse proxy + log analytics |
| Node monitor (Prometheus + Grafana) | [node-monitor-grafana/](node-monitor-grafana/) | standalone | Basic metrics |
| rclone sync | [rclone/](rclone/) | standalone | Cloud backup — see [README](rclone/README.md) |

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
