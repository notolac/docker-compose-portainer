# Jenkins

CI/CD automation server (LTS) ([upstream](https://www.jenkins.io)). For new setups
also evaluate lighter runners — this stack is kept for classic Jenkins pipelines.

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `jenkins.yaml` | Compose standalone | `jenkins/jenkins:lts` + `jenkins/ssh-agent` build agent |

## Deploy

```bash
docker compose -f jenkins.yaml up -d
```

## Variables

| Variable | Default | Description |
| -------- | ------- | ----------- |
| `JENKINS_HTTP_PORT` | `8087` | Exposed web UI port |
| `JENKINS_HOME` | `/opt/jenkins` | Persistent home |
