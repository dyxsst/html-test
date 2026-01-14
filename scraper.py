#!/usr/bin/env python3
"""
Manga Chapter Scraper using Playwright

Downloads chapter images from manga sites by opening the chapter page
in a headless browser and saving the images. This bypasses hotlink
protection since images are fetched within a real browser context.

Usage:
    python scraper.py --slug "i-can-copy-talents" --chapter "chapter-1"

Environment variables (for GitHub Actions):
    SLUG, CHAPTER, START_PAGE, END_PAGE, OUT_DIR
"""

import os
import re
import sys
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright


def get_env(key: str, default: str = None) -> str:
    """Get environment variable or return default."""
    return os.getenv(key) or default


def parse_args():
    """Parse command-line arguments with env var fallbacks."""
    p = argparse.ArgumentParser(description="Download manga chapter images")
    p.add_argument("--slug", default=get_env("SLUG"),
                   help="Manga slug (e.g., i-can-copy-talents)")
    p.add_argument("--chapter", default=get_env("CHAPTER"),
                   help="Chapter (e.g., chapter-1)")
    p.add_argument("--start", type=int, default=int(get_env("START_PAGE", "1")),
                   help="Start page number (default: 1)")
    p.add_argument("--end", type=int, default=int(get_env("END_PAGE", "100")),
                   help="End page number (default: 100)")
    p.add_argument("--out", default=get_env("OUT_DIR", "images"),
                   help="Output directory (default: images)")
    p.add_argument("--site", default=get_env("SITE_URL", "https://manhuaus.com/manga"),
                   help="Base site URL for chapter pages")
    return p.parse_args()


def extract_page_number(filename: str) -> int | None:
    """Extract numeric page from filename like '001.jpg' or 'page-5.png'."""
    stem = Path(filename).stem
    # Try pure numeric first
    if stem.isdigit():
        return int(stem)
    # Try extracting trailing digits
    match = re.search(r"(\d+)$", stem)
    if match:
        return int(match.group(1))
    return None


def scrape_chapter(slug: str, chapter: str, start: int, end: int, out_dir: str, site_url: str):
    """
    Open chapter page, find images, and download them.
    Uses Playwright to handle hotlink protection via browser context.
    """
    chapter_url = f"{site_url.rstrip('/')}/{slug}/{chapter}/"
    output_path = Path(out_dir) / slug / chapter
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Opening: {chapter_url}")
    print(f"Saving to: {output_path}")
    print(f"Page range: {start} - {end}")
    print("-" * 50)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            # Use domcontentloaded instead of networkidle (ads never stop loading)
            page.goto(chapter_url, wait_until="domcontentloaded", timeout=30000)
            # Wait for images to appear (manga reader content)
            page.wait_for_selector("img", timeout=15000)
            # Give a moment for lazy-loaded images to register
            page.wait_for_timeout(3000)
        except Exception as e:
            print(f"Failed to load page: {e}")
            browser.close()
            sys.exit(1)

        # Find all images that look like manga pages
        # Common patterns: img.manhuaus.com, cdn paths, or slug/chapter in URL
        images = []
        for img in page.query_selector_all("img"):
            src = img.get_attribute("src") or img.get_attribute("data-src") or ""
            if not src:
                continue
            # Skip tiny images (icons, avatars, etc.)
            if "avatar" in src.lower() or "logo" in src.lower() or "icon" in src.lower():
                continue
            # Look for chapter content images
            if slug in src or chapter in src or "img." in src or "/uploads/" in src:
                images.append(src.split("?")[0])  # Remove query params

        # Deduplicate while preserving order
        seen = set()
        unique_images = []
        for url in images:
            if url not in seen:
                seen.add(url)
                unique_images.append(url)

        print(f"Found {len(unique_images)} candidate image(s)")

        # Filter by page range
        filtered = []
        for url in unique_images:
            filename = Path(url).name
            page_num = extract_page_number(filename)
            if page_num is not None and start <= page_num <= end:
                filtered.append((page_num, url, filename))

        # Sort by page number
        filtered.sort(key=lambda x: x[0])
        print(f"After filtering: {len(filtered)} image(s) in range [{start}-{end}]")
        print("-" * 50)

        # Download each image using browser context (keeps cookies/headers)
        success = 0
        for page_num, url, filename in filtered:
            dest = output_path / filename
            if dest.exists():
                print(f"[{page_num}] Skipping (exists): {filename}")
                success += 1
                continue

            print(f"[{page_num}] Downloading: {filename}")
            try:
                response = context.request.get(url, headers={"Referer": chapter_url})
                if response.status == 200:
                    dest.write_bytes(response.body())
                    success += 1
                else:
                    print(f"    Failed: HTTP {response.status}")
            except Exception as e:
                print(f"    Error: {e}")

        browser.close()

    print("-" * 50)
    print(f"Done: {success}/{len(filtered)} images downloaded")
    print(f"Saved to: {output_path}")
    return success


def main():
    args = parse_args()

    if not args.slug or not args.chapter:
        print("Error: --slug and --chapter are required")
        print("Example: python scraper.py --slug i-can-copy-talents --chapter chapter-1")
        sys.exit(1)

    success = scrape_chapter(
        slug=args.slug,
        chapter=args.chapter,
        start=args.start,
        end=args.end,
        out_dir=args.out,
        site_url=args.site,
    )

    # Exit with error code if nothing was downloaded
    if success == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
