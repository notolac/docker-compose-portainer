# Speedtest Tracker

Scheduled ISP speed tests with history ([upstream](https://github.com/alexjustesen/speedtest-tracker)).

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `speedtest-tracker.yaml` | Compose standalone | `speedtest-tracker` (SQLite by default, optional external DB) |

## Deploy

```bash
docker compose -f speedtest-tracker.yaml up -d
```

Web UI on `${SPEEDTEST_TRACKER_PORT:-80}`, data in `${SPEEDTEST_TRACKER_DATA_PATH}`.

## Variables

`APP_KEY` (generate), `SPEEDTEST_SCHEDULE` (cron), optional external DB
(`DB_*`), optional Telegram notifications (`TELEGRAM_BOT_TOKEN`) — see the YAML.
