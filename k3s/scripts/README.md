# K3s scripts

Helper scripts for the `k3s/` tree (install, validate, sync).

Conventions (same as the rest of the repo):

- `set -euo pipefail`, `log()` / `die()` helpers.
- Destructive scripts require an explicit `<SOMETHING>_YES=yes` env gate
  **plus** user confirmation (see [`../../AGENTS.md`](../../AGENTS.md)).
- Validate with `bash -n <script>` before committing.
