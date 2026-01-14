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
