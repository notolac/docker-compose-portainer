# Helm

Standard Helm installs for cluster infrastructure. Each subfolder is one
release: a `README.md`, a values template (placeholders only — copy it,
set YOUR hosts/IPs/StorageClass, never commit the copy), and supporting
templates.

| Release | Folder | Chart |
|---------|--------|-------|
| Traefik (ingress) | [`traefik/`](traefik/) | `traefik/traefik` |
| Authentik (SSO) | [`authentik/`](authentik/) | `authentik/authentik` |
| Portainer (cluster UI) | [`portainer/`](portainer/) | `portainer/portainer` |

How apps are published (NPM vs Traefik, dual Ingress/file-provider model):
[`../docs/ingress-traefik.md`](../docs/ingress-traefik.md).

- No secrets here — reference Secret names, never secret values.
- Document the chart + version each values file targets.
