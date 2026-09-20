# GitLab CE

Git forge + built-in CI/CD, self-hosted ([upstream](https://about.gitlab.com)).

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `gitlab-docker-ce.yaml` | Compose standalone | `gitlab/gitlab-ce` (web 8929/443, SSH 2424, volumes under `/opt/gitlab`) |

## Deploy

```bash
docker compose -f gitlab-docker-ce.yaml up -d
```

First boot takes several minutes. Heavy service — give the host plenty of RAM/CPU.

## Variables

Set in `GITLAB_OMNIBUS_CONFIG`: `external_url` (your domain), SSH port, SMTP
settings (`smtp_user_name`, `smtp_password`, `smtp_domain`, `gitlab_email_from`),
plus `GITLAB_HOSTNAME`. See the YAML header and inline comments.
