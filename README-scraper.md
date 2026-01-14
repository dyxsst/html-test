Scraper and GitHub Actions
=========================

This repository includes `scraper.py` and a workflow `scrape-images-v2.yml` to download images hosted at URLs like:

  https://img.manhuaus.com/<slug>/<chapter>/001.jpg

Workflow inputs (via Actions > Scrape Images > Run workflow):

- `slug` (required)
- `chapter` (required)
- `start_page` (default 1)
- `end_page` (default 1)
- `pad_width` (default 3)
- `ext` (default jpg)
- `base_host` (default https://img.manhuaus.com)
- `commit_images` (true/false) — if `true`, the workflow will commit downloaded images back to the repo under `images/<slug>/<chapter>/`.

Notes
-----

- Use responsibly. Do not bypass paywalls or CSRF/CAPTCHA protections. This script does not circumvent geoblocks.
- Committing images to the repository can bloat the repo size; consider downloading artifacts or using external storage.
