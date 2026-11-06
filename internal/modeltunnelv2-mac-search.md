---
cursor:
  subagentId: "bc-70ddd2f7-703d-56c6-bb6e-69d6ad5baa7e"
---

# modeltunnelv2 Mac search (read-only)

## Environment

This worker runs on a **Linux Cursor Cloud VM** (`bc-70ddd2f7-703d-56c6-bb6e-69d6ad5baa7e`), not on Varun’s Mac. There is **no** `/Users` tree and **no** `/Users/varundaiya`.

## Commands run

```bash
# Primary search (maxdepth 5, prune Library/node_modules/.venv/site-packages)
find /Users/varundaiya -maxdepth 5 \
  \( -path '*/Library/*' -o -path '*/node_modules/*' -o -path '*/.venv/*' -o -path '*/site-packages/*' \) -prune -o \
  -type d \( -iname 'modeltunnelv2' -o -iname 'model_tunnel_v2' -o -iname 'ModelTunnelV2' -o -iname 'modeltunnel' \) -print

# Expected flagship path
test -d /Users/varundaiya/terminus-flagship-150m-30btokens

# Broader host search (maxdepth 6)
find / -maxdepth 6 -type d \( -iname '*modeltunnel*' -o -iname '*terminus-flagship*' \) 2>/dev/null

find /home /mnt /media /opt -maxdepth 5 -type d \( -iname '*modeltunnel*' -o -iname '*terminus-flagship*' \) 2>/dev/null
```

All searches returned **empty**. `/Users/varundaiya` and `/Users/varundaiya/terminus-flagship-150m-30btokens` do not exist on this host.

## Outcome for coordinator

- **Exact directory path:** not found (Mac filesystem not mounted here).
- **Tokenizer inspection:** not performed — no target folder.
- **terminus-flagship under `/Users/varundaiya`:** directory absent on this VM; no top-level training-code siblings to list.

## Unrelated local context (Project store, not modeltunnelv2)

Project docs under `docs/` contain a separate 65k BPE tokenizer effort (`tokenizer-65k.json`, `tokenizer-explained.md`, `internal/build-65k.py`). That is **not** a substitute for inspecting `terminus modeltunnelv2` on the Mac unless the coordinator explicitly repoints the task.
