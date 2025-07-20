#!/usr/bin/env python3
"""
plex_dl.py  URL  DIR
→ Descarga vídeo (yt-dlp), transcodifica a HEVC + MKV si hace falta,
  registra en Notion y devuelve la ruta final por stdout.
Requiere: yt-dlp, ffmpeg, notion-client, requests
"""

import argparse, os, pathlib, subprocess, sys, json, re, time
from notion_client import Client

ROOT = pathlib.Path("/srv/Plex")  # raíz Plex
TOKEN = os.getenv("NOTION_TOKEN")  # ya lo usas
DB_ID = os.getenv("NOTION_DB")
NV_PRESET = os.getenv("NV_PRESET", "p5")
NV_CQ = os.getenv("NV_CQ", "22")

client = Client(auth=TOKEN)


# ---------- helpers ----------
def run(cmd):
    print("👉", " ".join(cmd))
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode:
        raise RuntimeError(res.stderr.strip() or res.stdout)
    return res.stdout.strip()


def title_from_url(url):
    return run(["yt-dlp", "--get-title", url])


def sanitizer(name):
    return re.sub(r"[/:\"\\<>|?*]", "_", name)


def video_codec(path):
    return run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=codec_name",
            "-of",
            "csv=p=0",
            path,
        ]
    )


def notion_exists(title):
    resp = client.databases.query(
        database_id=DB_ID,
        filter={"property": "Name", "title": {"equals": title}},
        page_size=1,
    )
    return bool(resp["results"])


def notion_create(title, final_path, folder):
    client.pages.create(
        parent={"database_id": DB_ID},
        properties={
            "Name": {"title": [{"text": {"content": title}}]},
            "Path": {"rich_text": [{"text": {"content": str(final_path)}}]},
            "Folder": {"select": {"name": folder}},
        },
    )


# ---------- main ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("dir")  # Cursos / CustomVideos / MTV / Pomodoros-LoFi
    args = ap.parse_args()

    title = title_from_url(args.url)
    if notion_exists(title):
        print("SKIP: already present")
        sys.exit(0)

    target_dir = ROOT / args.dir
    target_dir.mkdir(parents=True, exist_ok=True)

    tmp = target_dir / f"{int(time.time())}.src.mkv"
    run(
        [
            "yt-dlp",
            "-f",
            "bv*+ba/b",
            "--merge-output-format",
            "mkv",
            "-o",
            str(tmp),
            args.url,
        ]
    )

    if video_codec(tmp) in ("hevc", "h265"):
        final_path = target_dir / f"{sanitizer(title)}.mkv"
        tmp.rename(final_path)
    else:
        final_path = target_dir / f"{sanitizer(title)}.mkv"
        run(
            [
                "ffmpeg",
                "-hwaccel",
                "cuda",
                "-i",
                str(tmp),
                "-c:v",
                "hevc_nvenc",
                "-preset",
                NV_PRESET,
                "-cq",
                NV_CQ,
                "-b:v",
                "0",
                "-c:a",
                "copy",
                str(final_path),
            ]
        )
        tmp.unlink()

    notion_create(title, final_path, args.dir)
    print(final_path)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERROR:", e, file=sys.stderr)
        sys.exit(1)
