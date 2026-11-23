"""Stage 1: Source Discovery for PHI Judgments."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from crawler.robots_check import check_robots


@dataclass
class SourceRoute:
    source_name: str
    base_url: str
    access_mode: str
    permitted: bool
    reason: str
    discovered_at: str

    def to_dict(self) -> dict:
        return asdict(self)


def discover_sources(offline_mode: bool = True) -> list[SourceRoute]:
    now = datetime.now(timezone.utc).isoformat()
    if offline_mode:
        return [
            SourceRoute(
                source_name="Direktori Putusan Mahkamah Agung RI",
                base_url="https://putusan3.mahkamahagung.go.id",
                access_mode="synthetic_fallback",
                permitted=False,
                reason="Sandbox offline mode; live collection deferred to authorized workstation.",
                discovered_at=now,
            )
        ]

    robots = check_robots()
    return [
        SourceRoute(
            source_name="Direktori Putusan Mahkamah Agung RI",
            base_url=robots.base_url,
            access_mode="polite_http" if robots.can_fetch_target else "manual_or_blocked",
            permitted=robots.can_fetch_target,
            reason=robots.status_note,
            discovered_at=now,
        )
    ]
