# netboot.xyz

Network-boot (PXE/iPXE) menu server ([upstream](https://netboot.xyz)).

## Contents

| File | Mode | Services |
| ---- | ---- | -------- |
| `netbootxyz.yaml` | Compose standalone | `netbootxyz` (web UI `:3003`, TFTP `:69/udp`, optional `:8082`) |

## Deploy

```bash
docker compose -f netbootxyz.yaml up -d
```

Config in `/opt/netbootxyz/config`, boot assets in `/opt/netbootxyz/assets`.
Point your DHCP server's next-server/filename (or an iPXE chain) at this host.
