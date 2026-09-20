# py-kms

KMS emulator for volume activation, with web UI ([upstream](https://github.com/Py-KMS-Organization/py-kms)).

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `kms.yaml` | Compose standalone | `py-kms` (KMS `:1688`, web UI `:8080`, DB under `/opt/kms-python/db`) |

## Deploy

```bash
docker compose -f kms.yaml up -d
```

Point clients at `<host>:1688`. Know your licensing position before using this
against machines you administer.
