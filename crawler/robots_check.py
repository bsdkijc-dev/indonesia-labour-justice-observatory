"""Robots.txt & Terms Inspection Utility for ILJO v1.0.

Always verifies robots.txt before any automated collection.
Never bypasses access controls, CAPTCHAs, or rate limits.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

import requests

logger = logging.getLogger(__name__)

USER_AGENT = "ILJO-Research-Observatory/1.0 (+https://github.com/bsdkijc-dev/indonesia-labour-justice-observatory)"


@dataclass
class RobotsCheckResult:
    base_url: str
    robots_url: str
    checked_at: str
    reachable: bool
    can_fetch_target: bool
    crawl_delay_seconds: float | None
    status_note: str

    def to_dict(self) -> dict:
        return asdict(self)


def check_robots(base_url: str = "https://putusan3.mahkamahagung.go.id", target_path: str = "/direktori/index/kategori/perselisihan-hubungan-industrial-1.html", timeout: int = 10) -> RobotsCheckResult:
    robots_url = urljoin(base_url, "/robots.txt")
    checked_at = datetime.now(timezone.utc).isoformat()
    rp = RobotFileParser()
    rp.set_url(robots_url)

    try:
        resp = requests.get(robots_url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
        if resp.status_code == 200:
            rp.parse(resp.text.splitlines())
            can_fetch = rp.can_fetch(USER_AGENT, urljoin(base_url, target_path))
            delay = rp.crawl_delay(USER_AGENT)
            return RobotsCheckResult(
                base_url=base_url,
                robots_url=robots_url,
                checked_at=checked_at,
                reachable=True,
                can_fetch_target=bool(can_fetch),
                crawl_delay_seconds=float(delay) if delay is not None else 3.0,
                status_note=f"HTTP 200; robots.txt parsed successfully.",
            )
        return RobotsCheckResult(
            base_url=base_url,
            robots_url=robots_url,
            checked_at=checked_at,
            reachable=True,
            can_fetch_target=False,
            crawl_delay_seconds=None,
            status_note=f"HTTP {resp.status_code}; halting automated collection pending manual terms review.",
        )
    except requests.RequestException as exc:
        logger.warning("robots.txt check failed cleanly: %s", exc)
        return RobotsCheckResult(
            base_url=base_url,
            robots_url=robots_url,
            checked_at=checked_at,
            reachable=False,
            can_fetch_target=False,
            crawl_delay_seconds=None,
            status_note=f"Network/access unavailable ({type(exc).__name__}); switch to offline synthetic/manual mode.",
        )


if __name__ == "__main__":
    import json
    print(json.dumps(check_robots().to_dict(), indent=2))
