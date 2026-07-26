# docker-compose-portainer

Public collection of **Docker Compose** and **Docker Swarm** stack files for self-hosted applications, designed to deploy via [Portainer](https://www.portainer.io/) or the Docker CLI.

This repository is the **public, reusable** counterpart to a private homelab knowledge base. It contains generic manifests and documentation only — no hostnames, internal IPs, or personal paths.

## Relationship with private homelab docs

| Aspect | This repo (public) | Private homelab repo |
|--------|-------------------|----------------------|
| Purpose | Shareable stacks for anyone | Architecture, hosts, runbooks, secrets |
| Paths / IPs | Environment variables with neutral defaults | Real host paths and network layout |
| Secrets | `.env.example` / Portainer env vars | Local `.env` files (never committed) |
| Runtime | Docker Compose / Swarm | K3s (primary) + Compose on dedicated hosts |

If you maintain a private homelab repo, treat this one as the **source of truth for stack YAML** that third parties can fork. Keep operational details (SSH, DNS, backups, VLANs) in your private documentation.

## Prerequisites

- Docker Engine with the [Compose plugin](https://docs.docker.com/compose/install/)
- (Optional) Docker Swarm initialized for `*-swarm.yaml` stacks
- (Recommended) [Portainer CE](https://docs.portainer.io/) for web-based deployment

## Installing Portainer CE 2.42.0 STS

We pin **Portainer CE STS 2.42.0** for consistency with current Short Term Support releases.

### Portainer Server

```bash
docker volume create portainer_data

docker run -d \
  -p 8000:8000 \
  -p 9443:9443 \
  --name portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:2.42.0
```

Open `https://<your-host>:9443`, create the admin user, and connect to the local Docker environment.

### Portainer Agent (optional)

Install on remote Docker hosts you want to manage from a central Portainer instance:

```bash
docker run -d \
  -p 9001:9001 \
  --name portainer_agent \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /var/lib/docker/volumes:/var/lib/docker/volumes \
  -v /:/host \
  portainer/agent:2.42.0
```

Then add the environment in Portainer → **Environments** → **Add environment** → **Agent**.

> **Note:** `:sts` tracks the latest STS release; `:2.42.0` pins this exact version. See [Portainer CE on Docker](https://docs.portainer.io/sts/start/install-ce/server/docker/linux).

## Deploying a stack

### Via Portainer

1. **Stacks → Add stack**
2. Paste the YAML from the service folder (or connect a Git repository)
3. Set **Environment variables** — **do not wrap values in quotes**
4. Create host directories referenced by `${...}` variables before deploying
5. Deploy

### Via CLI

```bash
# Standalone Compose
docker compose -f <service>/<file>.yaml --env-file <service>/.env.example up -d

# Swarm
docker stack deploy -c <service>/<file>-swarm.yaml <stack-name>
```

## Conventions

All stacks follow these rules so they work for third parties:

| Rule | Example |
|------|---------|
| **No hardcoded user home paths** | `${APP_DATA_PATH:-/opt/appname}` |
| **No internal IPs** | `${OLLAMA_BASE_URL:-http://ollama-host:11434}` |
| **Secrets via env vars** | Set in Portainer or a local `.env` (gitignored) |
| **Neutral storage defaults** | `/opt/<service>/…` or named volumes |
| **Comments document variables** | Each YAML header lists required env vars |

Copy the matching `.env.example` (when present) to `.env` and adjust paths for your host.

## Stack catalog

See **[STACKS.md](STACKS.md)** for the full list of services, variants (standalone vs Swarm), and links to service-specific READMEs.

## Repository structure

```text
docker-compose-portainer/
├── README.md              ← This file
├── STACKS.md              ← Service catalog
├── <service-name>/
│   ├── *.yaml             ← Compose or Swarm manifest
│   ├── .env.example       ← Optional template (no secrets)
│   └── README.md          ← Optional service notes
└── .gitignore
```

## Installing Docker (Ubuntu / Debian)

<details>
<summary>Ubuntu</summary>

```bash
sudo apt update
sudo apt install lsb-release gnupg2 apt-transport-https ca-certificates curl software-properties-common -y
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/docker.gpg
sudo add-apt-repository "deb [arch=$(dpkg --print-architecture)] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y
```

</details>

<details>
<summary>Debian</summary>

```bash
sudo apt update
sudo apt install lsb-release gnupg2 apt-transport-https ca-certificates curl software-properties-common -y
sudo curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/docker.gpg
sudo add-apt-repository "deb [arch=$(dpkg --print-architecture)] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y
```

</details>

## References

- [Docker documentation](https://docs.docker.com)
- [Portainer documentation](https://docs.portainer.io)
- [Docker Compose specification](https://docs.docker.com/compose/compose-file/)

## License

MIT — see individual stack upstream licenses for application-specific terms.
