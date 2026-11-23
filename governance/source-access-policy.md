# Source Access Policy — ILJO v1.0

## 1. Primary Source
- **Name:** Direktori Putusan Mahkamah Agung Republik Indonesia
- **URL:** `https://putusan3.mahkamahagung.go.id`

## 2. Access Rules & Pre-Collection Protocol
Before any automated collection runs:
1. Inspect `robots.txt` and published Terms of Use (`crawler/robots_check.py`).
2. Identify whether official APIs, bulk exports, or authorized research access channels exist.
3. Perform a minimal access test (single-page or small-batch) with conservative rate limits (`>= 3.0s` delay, `1` concurrent worker) and exponential backoff on HTTP 429/5xx.
4. Immediately halt collection if CAPTCHA, login walls, IP blocks, or site instability appear.
5. Never treat public web visibility as blanket permission for unrestricted scraping or raw PDF redistribution.

## 3. Verified Workstation Access Check (2026-11-23)
- **Status:** `PERMITTED (robots.txt HTTP 200)` from authorized workstation (`ai-Precision-7540`).
- **Checked At:** `2026-11-23T03:56:06.961185+00:00`
- **Result:** `reachable = true`, `can_fetch_target = true`, `crawl_delay_seconds = 3.0` (`HTTP 200; robots.txt parsed successfully.`).
- **Governance Note:** Even with `can_fetch_target = true`, collection must remain strictly rate-limited (`>= 3.0s` delay, single worker), cached locally in `data/raw/` (git-ignored), and never redistribute raw PDFs.
