#!/usr/bin/env python3
"""Download images from a host that serves images at
<base>/<slug>/<chapter>/<page>.<ext>

Usage: The script reads configuration from environment variables or CLI args.
Environment variables / CLI args (prefer env in Actions):
  BASE_HOST (default: https://img.manhuaus.com)
  SLUG
  CHAPTER
  START_PAGE (int)
  END_PAGE (int)
  PAD_WIDTH (int, default 3)
  EXT (jpg/png, default jpg)
  OUT_DIR (default images)

The script will save files to OUT_DIR/<slug>/<chapter>/001.jpg etc.
"""

import os
import sys
import time
import argparse
from pathlib import Path

import requests


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--slug", help="manga slug", default=os.getenv("SLUG"))
    p.add_argument("--chapter", help="chapter name", default=os.getenv("CHAPTER"))
    p.add_argument("--start", type=int, help="start page", default=int(os.getenv("START_PAGE" or 1)))
    p.add_argument("--end", type=int, help="end page", default=int(os.getenv("END_PAGE" or 1)))
    p.add_argument("--pad", type=int, help="pad width", default=int(os.getenv("PAD_WIDTH" or 3)))
    p.add_argument("--ext", help="file extension", default=os.getenv("EXT" or "jpg"))
    p.add_argument("--base", help="base host", default=os.getenv("BASE_HOST" or "https://img.manhuaus.com"))
    p.add_argument("--out", help="output dir", default=os.getenv("OUT_DIR" or "images"))
    p.add_argument("--delay", type=float, help="delay seconds between requests", default=float(os.getenv("DELAY" or 0.4)))
    p.add_argument("--timeout", type=float, help="request timeout seconds", default=float(os.getenv("TIMEOUT" or 15)))
    return p.parse_args()


def pad(num, width):
    s = str(num)
    return s if len(s) >= width else ("0" * (width - len(s)) + s)


def build_url(base, slug, chapter, page, pad_width, ext):
    filename = f"{pad(page, pad_width)}.{ext}"
    return f"{base.rstrip('/')}/{slug}/{chapter}/{filename}"


def download(url, dest_path, timeout=15, retries=3):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; scraper/1.0)"}
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            if resp.status_code == 200 and resp.content:
                dest_path.write_bytes(resp.content)
                return True
            else:
                print(f"[{attempt}] Bad response {resp.status_code} for {url}")
        except Exception as e:
            print(f"[{attempt}] Error fetching {url}: {e}")
        time.sleep(1 + attempt * 0.6)
    return False


def main():
    args = parse_args()

    if not args.slug or not args.chapter:
        print("Missing slug or chapter. Provide --slug and --chapter or set SLUG/CHAPTER env vars.")
        sys.exit(2)

    out_dir = Path(args.out) / args.slug / args.chapter
    out_dir.mkdir(parents=True, exist_ok=True)

    success_count = 0
    attempted = 0

    for p in range(args.start, args.end + 1):
        url = build_url(args.base, args.slug, args.chapter, p, args.pad, args.ext)
        filename = pad(p, args.pad) + "." + args.ext
        dest = out_dir / filename
        if dest.exists():
            print(f"Skipping existing {dest}")
            success_count += 1
            attempted += 1
            continue
        print(f"Downloading {url} -> {dest}")
        ok = download(url, dest, timeout=args.timeout)
        attempted += 1
        if ok:
            success_count += 1
        else:
            print(f"Failed to download {url}")
        time.sleep(args.delay)

    print(f"Done: {success_count}/{attempted} succeeded. Files saved to {out_dir}")


if __name__ == "__main__":
    main()
