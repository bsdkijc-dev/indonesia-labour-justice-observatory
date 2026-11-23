"""Stage 2: Polite, rate-limited, idempotent HTTP collector with exponential backoff."""

from __future__ import annotations

import time
from pathlib import Path
import requests

from crawler.provenance import sha256_bytes
from crawler.robots_check import USER_AGENT, check_robots


class PoliteCollector:
    def __init__(self, cache_dir: Path, min_delay_sec: float = 3.0, max_retries: int = 3):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.min_delay_sec = max(min_delay_sec, 3.0)
        self.max_retries = max_retries
        self._last_request_ts = 0.0

    def _respect_rate_limit(self) -> None:
        elapsed = time.monotonic() - self._last_request_ts
        if elapsed < self.min_delay_sec:
            time.sleep(self.min_delay_sec - elapsed)

    def fetch_if_permitted(self, url: str, target_filename: str) -> dict:
        dest = self.cache_dir / target_filename
        if dest.exists():
            payload = dest.read_bytes()
            return {
                "url": url,
                "status": "cached",
                "path": str(dest),
                "sha256": sha256_bytes(payload),
            }

        robots = check_robots()
        if not robots.can_fetch_target:
            return {
                "url": url,
                "status": "halted_by_governance",
                "reason": robots.status_note,
            }

        for attempt in range(self.max_retries):
            self._respect_rate_limit()
            self._last_request_ts = time.monotonic()
            try:
                resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=15)
                if resp.status_code == 200:
                    dest.write_bytes(resp.content)
                    return {
                        "url": url,
                        "status": "fetched",
                        "path": str(dest),
                        "sha256": sha256_bytes(resp.content),
                    }
                if resp.status_code in (403, 429, 503):
                    time.sleep((2 ** attempt) * self.min_delay_sec)
                    continue
                return {"url": url, "status": "http_error", "code": resp.status_code}
            except requests.RequestException as exc:
                if attempt == self.max_retries - 1:
                    return {"url": url, "status": "network_error", "error": type(exc).__name__}
                time.sleep((2 ** attempt) * self.min_delay_sec)

        return {"url": url, "status": "max_retries_exceeded"}
