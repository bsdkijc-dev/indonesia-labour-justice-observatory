"""Stage 3a: Document Parser — Extracts clean text from HTML judgment pages using BeautifulSoup."""

from __future__ import annotations

import re
from bs4 import BeautifulSoup


def parse_html_judgment(html_text: str) -> dict[str, str]:
    soup = BeautifulSoup(html_text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer"]):
        tag.decompose()
    text = re.sub(r"\s+", " ", soup.get_text(" ", strip=True)).strip()
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    return {"title": title, "clean_text": text}
