# K3s apps

One folder per application. Each app has its own `README.md` (images, secrets,
deploy order), generic manifests, an `ingress.yaml` example (`*.example.com`
hosts — set yours), and a `*-k3s.env.example` template when it needs a Secret.

| App | Folder | Stack |
|-----|--------|-------|
| Firefly III | [firefly/](firefly/) | App + PostgreSQL + importer + cron |
| Homarr | [homarr/](homarr/) | App + PVC |
| Linkding | [linkding/](linkding/) | App + PVC |
| LiteLLM | [litellm/](litellm/) | Proxy + PostgreSQL + Redis |
| Mealie | [mealie/](mealie/) | App + PVC (SQLite) |
| n8n | [n8n/](n8n/) | App + runners sidecar + PostgreSQL |
| Odoo | [odoo/](odoo/) | App + PostgreSQL |
| Onyx | [onyx/](onyx/) | API + web + nginx + Postgres + Vespa + OpenSearch + MinIO + GPU model servers (+ optional code interpreter) |
| Vaultwarden | [vaultwarden/](vaultwarden/) | App + PVC |
| Wallos | [wallos/](wallos/) | App + PVCs |

Conventions: no personal hosts, IPs, or secrets (see [`../README.md`](../README.md)
and [`../../AGENTS.md`](../../AGENTS.md)). Default `storageClassName` is the
Rook-Ceph `ceph-block` — see [`../configs/rook/`](../configs/rook/) — change it
to yours. Validate with `kubectl apply --dry-run=client -k <app>/`.

Publishing: every app is exposed through Traefik — standard `ingress.yaml`
by default, file-provider router as the advanced path. Guide + shared
middleware catalog: [`../docs/ingress-traefik.md`](../docs/ingress-traefik.md).
