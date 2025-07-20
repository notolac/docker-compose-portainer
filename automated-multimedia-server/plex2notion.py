#!/usr/bin/env python3
"""
plex2notion_rich.py (v8)
=======================
🚀 Re‑entrant, con exclusiones y **sin crash de timeout**

Cambios v8
-----------
* Eliminado el argumento `timeout` no soportado en `Client()`.
* Se crea un `httpx.Client(timeout=30)` y se pasa vía `client=<httpx.Client>` al SDK.
* Mismo resto de funcionalidad: barra Rich, retry, skip Music, cache de duplicados.

Variables clave
---------------
```
NOTION_TOKEN   # token de integración
NOTION_DB      # ID de la base de datos
SKIP_TOP       # p.e. "Music,Pomodoros-LoFi"  (opcional)
RATE_LIMIT     # peticiones/seg (def. 3)
TITLE_PROP …   # mapear columnas si difieren
```

Uso rápido
~~~~~~~~~~
```bash
pip install notion-client rich httpx
export NOTION_TOKEN=secret_xxx
export NOTION_DB=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
export SKIP_TOP="Music"
find /srv/Plex -type f -print0 | ./plex2notion_rich.py
```
"""

import os, sys, time, pathlib, re
from typing import Set

import httpx
from notion_client import Client, APIResponseError
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    TaskProgressColumn,
)

# ---------------- Config global ----------------
ROOT = pathlib.Path("/srv/Plex")
RATE_LIMIT = int(os.getenv("RATE_LIMIT", 3))
SKIP_TOP = {s.strip() for s in os.getenv("SKIP_TOP", "").split(",") if s.strip()}
TOKEN = os.getenv("NOTION_TOKEN")
DB_ID = os.getenv("NOTION_DB")
if not TOKEN or not DB_ID:
    sys.exit("ERROR: exporta NOTION_TOKEN y NOTION_DB primero.")

# ——— httpx client con timeout ———
_httpx = httpx.Client(timeout=30)
client = Client(auth=TOKEN, client=_httpx)

# ---------------- 1) Resolver nombres de columnas ----------------
user_cols = {
    "title": os.getenv("TITLE_PROP", "Título"),
    "path": os.getenv("PATH_PROP", "Ruta"),
    "top": os.getenv("TOP_PROP", "Top Folder"),
    "sub": os.getenv("SUB_PROP", "Subcarpeta"),
}

schema = client.databases.retrieve(database_id=DB_ID)["properties"]

fallbacks = {
    "title": ["Name", "Título"],
    "path": ["Path", "Ruta"],
    "top": ["Folder", "Top Folder", "Carpeta"],
    "sub": ["Subfolder", "Subcarpeta"],
}


def resolve_prop(key: str) -> str:
    cand = user_cols[key]
    if cand in schema:
        return cand
    for alt in fallbacks[key]:
        if alt in schema:
            return alt
    lower = {k.lower(): k for k in schema}
    for alt in [cand] + fallbacks[key]:
        if alt.lower() in lower:
            return lower[alt.lower()]
    sys.exit(
        f"ERROR: falta columna para '{key}'. Crea la propiedad o usa {key.upper()}_PROP."
    )


TITLE_PROP, PATH_PROP, TOP_PROP, SUB_PROP = (
    resolve_prop(k) for k in ("title", "path", "top", "sub")
)

# ---------------- 2) Sanitizador valor Select --------------------
invalid_re = re.compile(r"[,\n\r\"]+")


def clean_option(text: str) -> str:
    text = invalid_re.sub(" ", text).strip()
    return (text or "Unknown")[:100]


# ---------------- 3) Cache de paths existentes -------------------


def load_existing_paths() -> Set[str]:
    cache: Set[str] = set()
    cursor = None
    while True:
        resp = client.databases.query(
            database_id=DB_ID,
            start_cursor=cursor,
            page_size=100,
            filter={"property": PATH_PROP, "rich_text": {"is_not_empty": True}},
        )
        for page in resp["results"]:
            rich = page["properties"].get(PATH_PROP, {}).get("rich_text", [])
            if rich:
                cache.add(rich[0]["plain_text"])
        if not resp.get("has_more"):
            break
        cursor = resp["next_cursor"]
    return cache


existing_paths = load_existing_paths()

# ---------------- 4) Builder de payload --------------------------


def build_page(path: pathlib.Path):
    try:
        parts = path.relative_to(ROOT).parts
    except ValueError:
        parts = path.parts

    top = clean_option(parts[0]) if parts else "Unknown"
    subs = [clean_option(s) for s in parts[1:-1]]

    return {
        "parent": {"database_id": DB_ID},
        "properties": {
            TITLE_PROP: {"title": [{"text": {"content": path.stem}}]},
            PATH_PROP: {"rich_text": [{"text": {"content": str(path)}}]},
            TOP_PROP: {"select": {"name": top}},
            SUB_PROP: {"multi_select": [{"name": s} for s in subs]},
        },
    }


# ---------------- 5) Leer stdin y filtrar ------------------------
raw = sys.stdin.buffer.read().split(b"\0")
all_files = [pathlib.Path(b.decode()) for b in raw if b]

files = [
    f
    for f in all_files
    if (f.relative_to(ROOT).parts[0] if f.is_absolute() else f.parts[0]) not in SKIP_TOP
]

if not files:
    sys.exit("No hay archivos para procesar tras aplicar SKIP_TOP.")

# ---------------- 6) Función robusta de envío --------------------
MAX_RETRIES = 3


def create_page_with_retry(payload: dict):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            client.pages.create(**payload)
            return
        except (httpx.TimeoutException, httpx.HTTPStatusError) as net_err:
            if attempt == MAX_RETRIES:
                raise net_err
            time.sleep(2**attempt)
        except APIResponseError as api_err:
            if api_err.status in (502, 429):
                if attempt == MAX_RETRIES:
                    raise api_err
                time.sleep(2**attempt)
            else:
                raise api_err


# ---------------- 7) Progreso & subida ---------------------------
with Progress(
    SpinnerColumn(),
    TextColumn("[blue]Sincronizando"),
    BarColumn(),
    TaskProgressColumn(),
    TimeElapsedColumn(),
    TimeRemainingColumn(),
    transient=True,
) as prog:
    task = prog.add_task("Subiendo", total=len(files))

    for idx, p in enumerate(files, 1):
        p_str = str(p)
        if p_str in existing_paths:
            prog.update(task, advance=1)
            continue
        try:
            create_page_with_retry(build_page(p))
            existing_paths.add(p_str)
        except Exception as e:
            prog.console.print(f"[red]⚠️  {p}: {e}")
        finally:
            prog.update(task, advance=1)

        if idx % (RATE_LIMIT * MAX_RETRIES) == 0:
            time.sleep(1)

prog.console.print(
    f"[green]✅  Terminado. {len(files)} archivos procesados; {len(existing_paths)} únicos en la DB."
)
