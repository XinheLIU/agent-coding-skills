#!/usr/bin/env python3
"""Validate the portable structure of a generated static report."""

from html.parser import HTMLParser
from pathlib import Path
import sys


class ReportParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.articles = 0
        self.before = 0
        self.after = 0
        self.top = 0
        self.source_links = 0
        self.svg = 0
        self.svg_titles = 0
        self.decorative_svgs = 0
        self._in_svg = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_map = dict(attrs)
        if tag == "article":
            self.articles += 1
        if tag == "svg":
            self.svg += 1
            self._in_svg = True
            tiny_decorative = attrs_map.get("width") == "24" and attrs_map.get("height") == "8"
            if attrs_map.get("aria-hidden") == "true" or tiny_decorative:
                self.decorative_svgs += 1
        if tag == "title" and self._in_svg:
            self.svg_titles += 1
        if tag == "a" and "source" in (attrs_map.get("href") or "").lower():
            self.source_links += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "svg":
            self._in_svg = False

    def handle_data(self, data: str) -> None:
        normalized = " ".join(data.lower().split())
        if "before" in normalized or "current" in normalized:
            self.before += 1
        if "after" in normalized or "target" in normalized:
            self.after += 1
        if "top recommendation" in normalized or "next decision" in normalized:
            self.top += 1


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} REPORT.html", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    parser = ReportParser()
    parser.feed(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    if parser.articles == 0:
        errors.append("no article cards found")
    if parser.before == 0 or parser.after == 0:
        errors.append("no current/before and target/after comparison found")
    html = path.read_text(encoding="utf-8")
    is_roadmap = "roadmap" in path.name.lower() or "dependency-ordered roadmap" in html.lower()
    if parser.top == 0 and not is_roadmap:
        errors.append("no top recommendation or next decision found")
    if parser.svg and parser.svg_titles + parser.decorative_svgs < parser.svg:
        errors.append("some SVG diagrams lack accessible title elements")
    if errors:
        print(f"{path}: " + "; ".join(errors), file=sys.stderr)
        return 1
    kind = "roadmap" if is_roadmap else "visual report"
    print(f"{path}: {kind} structure OK ({parser.articles} articles, {parser.svg} SVGs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
