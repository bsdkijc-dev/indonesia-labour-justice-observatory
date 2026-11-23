"""Minimal Polite Live Access Test (Index-Only, max 5 pages, >= 3.0s delay).

Caches HTML index pages to data/raw/index_pages/ and records provenance.
Halts immediately on CAPTCHA, HTTP 403/429, or robots.txt disallow.
"""

from __future__ import annotations

import json
from pathlib import Path

from bs4 import BeautifulSoup

from crawler.polite_collector import PoliteCollector
from crawler.provenance import record_provenance
from crawler.robots_check import check_robots

BASE_DIR = Path(__file__).resolve().parent.parent
PHI_CATEGORY_URL = "https://putusan3.mahkamahagung.go.id/direktori/index/kategori/perselisihan-hubungan-industrial-1.html"


def run_minimal_live_test(max_pages: int = 5) -> dict:
    robots = check_robots()
    if not robots.can_fetch_target:
        return {"status": "halted_by_robots", "details": robots.to_dict()}

    delay = max(robots.crawl_delay_seconds or 3.0, 3.0)
    raw_dir = BASE_DIR / "data" / "raw" / "index_pages"
    collector = PoliteCollector(cache_dir=raw_dir, min_delay_sec=delay)
    prov_log = BASE_DIR / "data" / "processed" / "logs" / "live_test_provenance.jsonl"

    results = []
    for page in range(1, max_pages + 1):
        url = (
            PHI_CATEGORY_URL
            if page == 1
            else f"https://putusan3.mahkamahagung.go.id/direktori/index/kategori/perselisihan-hubungan-industrial-1/page/{page}.html"
        )
        res = collector.fetch_if_permitted(url, f"phi_index_page_{page}.html")
        if res["status"] in ("fetched", "cached"):
            html = Path(res["path"]).read_text(encoding="utf-8", errors="ignore")
            soup = BeautifulSoup(html, "html.parser")
            decision_links = [
                a["href"]
                for a in soup.find_all("a", href=True)
                if "/direktori/putusan/" in a["href"]
            ]
            res["decision_links_found"] = len(set(decision_links))
        results.append(res)
        if res["status"] not in ("fetched", "cached"):
            break

    summary = {
        "status": "completed",
        "pages_attempted": len(results),
        "total_decision_links_seen": sum(r.get("decision_links_found", 0) for r in results),
        "results": results,
    }
    record_provenance(prov_log, "MINIMAL_LIVE_INDEX_TEST", 0, len(results), "COMPLETED", summary)
    return summary


if __name__ == "__main__":
    print(json.dumps(run_minimal_live_test(max_pages=5), indent=2))
