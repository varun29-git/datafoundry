# modeltunnelv2 Mac search (read-only)

## Environment

This Linux cloud worker did not have the requester’s macOS filesystem mounted. The expected macOS home directory was unavailable.

## Commands run

The searches are shown with environment-variable placeholders instead of machine-local paths.

```bash
# Primary search (maxdepth 5, prune Library/node_modules/.venv/site-packages)
find "${MACOS_HOME}" -maxdepth 5 \
  \( -path '*/Library/*' -o -path '*/node_modules/*' -o -path '*/.venv/*' -o -path '*/site-packages/*' \) -prune -o \
  -type d \( -iname 'modeltunnelv2' -o -iname 'model_tunnel_v2' -o -iname 'ModelTunnelV2' -o -iname 'modeltunnel' \) -print

# Expected flagship path
test -d "${MACOS_HOME}/terminus-flagship-150m-30btokens"

# Broader host search (maxdepth 6)
find / -maxdepth 6 -type d \( -iname '*modeltunnel*' -o -iname '*terminus-flagship*' \) 2>/dev/null

find "${ADDITIONAL_SEARCH_ROOTS[@]}" -maxdepth 5 -type d \( -iname '*modeltunnel*' -o -iname '*terminus-flagship*' \) 2>/dev/null
```

All searches returned **empty**. Neither the expected macOS home nor the flagship checkout existed on this worker.

## Outcome for coordinator

- **Exact directory path:** not found (macOS filesystem not mounted here).
- **Tokenizer inspection:** not performed — no target folder.
- **terminus-flagship under the expected macOS home:** directory absent on this VM; no top-level training-code siblings to list.

## Unrelated local context (Project store, not modeltunnelv2)

Project docs under `docs/` contain a separate 65k BPE tokenizer effort (`tokenizer-65k.json`, `tokenizer-explained.md`, `internal/build-65k.py`). That is **not** a substitute for inspecting `terminus modeltunnelv2` on the Mac unless the coordinator explicitly repoints the task.
