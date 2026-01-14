#!/usr/bin/env python3
"""Scrape chapter images using Playwright to avoid hotlink protections.

Usage: set env vars or pass CLI args. The script will open the chapter page
on manhuaus and download images referenced on the page into images/<slug>/<chapter>/
"""

import os
import sys
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--slug", required=False, default=os.getenv("SLUG"))
    p.add_argument("--chapter", required=False, default=os.getenv("CHAPTER"))
    p.add_argument("--base-host", default=os.getenv("BASE_HOST", "https://img.manhuaus.com"))
    p.add_argument("--page-base", default=os.getenv("PAGE_BASE", "https://manhuaus.com/manga"))
    p.add_argument("--out", default=os.getenv("OUT_DIR", "images"))
    p.add_argument("--start", type=int, default=None, help="Optional start page to filter images")
    p.add_argument("--end", type=int, default=None, help="Optional end page to filter images")
    p.add_argument("--pad", type=int, default=None, help="Optional zero-pad width to match filenames (e.g. 3)")
    p.add_argument("--ext", default=None, help="Optional extension filter (jpg/png)")
    return p.parse_args()


def ensure_out_dir(out_dir, slug, chapter):
    p = Path(out_dir) / slug / chapter
    p.mkdir(parents=True, exist_ok=True)
    return p


def main():
    args = parse_args()

    if not args.slug or not args.chapter:
        print("Provide --slug and --chapter")
        sys.exit(2)

    chapter_page = f"{args.page_base.rstrip('/')}/{args.slug}/{args.chapter}/"
    out_dir = ensure_out_dir(args.out, args.slug, args.chapter)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        print(f"Opening chapter page: {chapter_page}")
        page.goto(chapter_page, wait_until="networkidle")

        # Collect images that match the image host or slug/chapter pattern
        candidates = []
        for img in page.query_selector_all('img'):
            src = img.get_attribute('src')
            if not src:
                continue
            # normalize
            src = src.split('?')[0]
            if args.slug in src and args.chapter in src:
                candidates.append(src)
            elif args.base_host in src:
                candidates.append(src)

        # Deduplicate while preserving order
        seen = set()
        imgs = []
        for u in candidates:
            if u not in seen:
                seen.add(u)
                imgs.append(u)

        # Optional filtering by page range / pad / ext if provided
        def filename_to_page(name, pad_hint=None):
            stem = Path(name).stem
            if stem.isdigit():
                return int(stem)
            # try to extract trailing digits
            import re
            m = re.search(r"(\d+)$", stem)
            if m:
                return int(m.group(1))
            return None

        if args.start is not None or args.end is not None or args.pad is not None or args.ext is not None:
            filtered = []
            for u in imgs:
                fname = Path(u).name
                if args.ext and not fname.lower().endswith('.' + args.ext.lower()):
                    continue
                page_num = filename_to_page(fname, args.pad)
                if page_num is None:
                    continue
                if args.start is not None and page_num < args.start:
                    continue
                if args.end is not None and page_num > args.end:
                    continue
                filtered.append(u)
            imgs = filtered

        print(f"Found {len(imgs)} image(s)")

        for idx, src in enumerate(imgs, start=1):
            name = Path(src).name
            dest = out_dir / name
            print(f"Downloading {src} -> {dest}")
            # Use context.request to fetch with browser session headers
            try:
                resp = context.request.get(src, headers={"Referer": chapter_page})
                if resp.status == 200:
                    dest.write_bytes(resp.body())
                else:
                    print(f"Bad response {resp.status} for {src}")
            except Exception as e:
                print(f"Error fetching {src}: {e}")

        browser.close()

    print(f"Saved images to {out_dir}")


if __name__ == '__main__':
    main()
