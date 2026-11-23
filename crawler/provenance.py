"""Cryptographic provenance and audit-trail utilities for ILJO v1.0."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def record_provenance(
    log_path: Path,
    stage: str,
    input_count: int,
    output_count: int,
    status: str,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    entry = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "stage": stage,
        "input_count": input_count,
        "output_count": output_count,
        "status": status,
        "details": details or {},
    }
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry
