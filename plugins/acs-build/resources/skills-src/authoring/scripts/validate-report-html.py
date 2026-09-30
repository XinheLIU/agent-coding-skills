#!/usr/bin/env python3
"""Validate a generated Presenter view against the visual report contract.

Checks each card, not just the page: a card without its own visual passes a
page-level "before/after appears somewhere" check, which is how prose-and-table
reports slipped through before.

--version-only checks just the date, revision, and internal links. Use it for
human-readable HTML that is not a finding report: canonical records, roadmaps,
delivery plans, prototypes, and design previews.
"""

from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATED_FILENAME = re.compile(r"-\d{4}-\d{2}-\d{2}\.html$")
RAW_HEX = re.compile(r"^#[0-9a-fA-F]{3,8}$")
COLOR_ATTRIBUTES = ("fill", "stroke", "stop-color")
VISUAL_MODES = ("compare", "single", "none")
# Calibrated on reference reports: schematic labels stay under 15 words each
# and under ~90 words per diagram; prose drawn as SVG text runs far above both.
MAX_WORDS_PER_LABEL = 14
MAX_WORDS_PER_SVG = 90


@dataclass
class Card:
    label: str
    visual_mode: str
    svgs: int = 0
    panes: int = 0


@dataclass
class Diagram:
    label: str
    has_title: bool = False
    decorative: bool = False
    words: int = 0
    longest_label: int = 0
    raw_hex_colors: set[str] = field(default_factory=set)


class ReportParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.meta: dict[str, str] = {}
        self.cards: list[Card] = []
        self.collapsed_cards: list[str] = []
        self.diagrams: list[Diagram] = []
        self.visible_text: list[str] = []
        self.top = 0
        self._card: Card | None = None
        self._diagram: Diagram | None = None
        self._in_svg_text = False
        self._label_words = 0
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_map = {name: value or "" for name, value in attrs}
        classes = attrs_map.get("class", "").split()
        label = attrs_map.get("id") or f"<{tag}> #{len(self.cards) + len(self.collapsed_cards) + 1}"
        if tag in ("style", "script"):
            self._skip_depth += 1
        if tag == "meta" and "name" in attrs_map:
            self.meta[attrs_map["name"]] = attrs_map.get("content", "").strip()
        if tag == "details" and "card" in classes:
            self.collapsed_cards.append(label)
        if tag == "article" and "card" in classes:
            self._card = Card(label, attrs_map.get("data-visual", "compare"))
            self.cards.append(self._card)
        if self._card and "pane" in classes:
            self._card.panes += 1
        if tag == "svg":
            if self._card:
                self._card.svgs += 1
            tiny_decorative = attrs_map.get("width") == "24" and attrs_map.get("height") == "8"
            self._diagram = Diagram(label=self._card.label if self._card else "page")
            self._diagram.decorative = attrs_map.get("aria-hidden") == "true" or tiny_decorative
            self.diagrams.append(self._diagram)
        if not self._diagram:
            return
        if tag == "title":
            self._diagram.has_title = True
        if tag == "text":
            self._in_svg_text = True
            self._label_words = 0
        for name in COLOR_ATTRIBUTES:
            value = attrs_map.get(name, "").strip()
            if RAW_HEX.match(value):
                self._diagram.raw_hex_colors.add(value)

    def handle_endtag(self, tag: str) -> None:
        if tag in ("style", "script") and self._skip_depth:
            self._skip_depth -= 1
        if tag == "article":
            self._card = None
        if tag == "svg":
            self._diagram = None
        if tag == "text" and self._diagram:
            self._in_svg_text = False
            self._diagram.longest_label = max(self._diagram.longest_label, self._label_words)

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        self.visible_text.append(data)
        normalized = " ".join(data.lower().split())
        if "top recommendation" in normalized or "next decision" in normalized:
            self.top += 1
        if self._diagram and self._in_svg_text:
            words = len(data.split())
            self._label_words += words
            self._diagram.words += words


def check_cards(parser: ReportParser) -> list[str]:
    errors: list[str] = []
    if not parser.cards:
        errors.append("no <article class=\"card\"> found")
    for label in parser.collapsed_cards:
        errors.append(f"card {label}: <details class=\"card\"> collapses the card; use <article class=\"card\"> and put only evidence in <details>")
    for card in parser.cards:
        if card.visual_mode not in VISUAL_MODES:
            errors.append(f"card {card.label}: data-visual must be one of {VISUAL_MODES}")
        elif card.visual_mode == "compare" and card.panes < 2:
            errors.append(f"card {card.label}: needs Before and After panes ({card.panes} found); set data-visual=\"single\" only for a non-structural card")
        elif card.visual_mode == "single" and card.svgs == 0:
            errors.append(f"card {card.label}: data-visual=\"single\" but no <svg>")
    return errors


def check_diagrams(parser: ReportParser) -> list[str]:
    errors: list[str] = []
    for diagram in parser.diagrams:
        if diagram.decorative:
            continue
        if not diagram.has_title:
            errors.append(f"diagram in {diagram.label}: missing accessible <title>")
        if diagram.longest_label > MAX_WORDS_PER_LABEL:
            errors.append(f"diagram in {diagram.label}: a label has {diagram.longest_label} words (max {MAX_WORDS_PER_LABEL}); move prose to the takeaway")
        if diagram.words > MAX_WORDS_PER_SVG:
            errors.append(f"diagram in {diagram.label}: {diagram.words} words of SVG text (max {MAX_WORDS_PER_SVG}); redraw as a schematic")
        if diagram.raw_hex_colors:
            colors = ", ".join(sorted(diagram.raw_hex_colors)[:4])
            errors.append(f"diagram in {diagram.label}: raw hex colors ({colors}) break dark mode; use var(--token)")
    return errors


def check_version(parser: ReportParser, path: Path) -> list[str]:
    errors: list[str] = []
    generated = parser.meta.get("generated", "")
    if not ISO_DATE.match(generated):
        errors.append("missing <meta name=\"generated\" content=\"YYYY-MM-DD\">")
    elif generated not in " ".join(parser.visible_text):
        errors.append(f"generated date {generated} is not shown on the visible meta line")
    if not parser.meta.get("source-revision"):
        errors.append("missing <meta name=\"source-revision\" content=\"...\">")
    is_living = parser.meta.get("view-kind") == "living"
    if not is_living and not DATED_FILENAME.search(path.name):
        errors.append("one-off report filename must end in -YYYY-MM-DD.html (or declare <meta name=\"view-kind\" content=\"living\">)")
    return errors


SCRIPT_BLOCK = re.compile(r"<script\b.*?</script>", re.DOTALL | re.IGNORECASE)


def check_links(html: str) -> list[str]:
    anchors = set(re.findall(r'id=["\']([^"\']+)', html))
    # Hrefs built inside scripts are templates, not static links.
    markup = SCRIPT_BLOCK.sub("", html)
    return [f"broken internal link #{target}" for target in re.findall(r'href=["\']#([^"\']+)', markup) if target not in anchors]


def validate(path: Path, *, version_only: bool = False) -> list[str]:
    html = path.read_text(encoding="utf-8")
    parser = ReportParser()
    parser.feed(html)
    if version_only:
        return check_version(parser, path) + check_links(html)
    is_roadmap = "roadmap" in path.name.lower() or "dependency-ordered roadmap" in html.lower()
    errors = check_version(parser, path) + check_diagrams(parser) + check_links(html)
    if is_roadmap:
        return errors
    if parser.top == 0:
        errors.append("no top recommendation or next decision found")
    return errors + check_cards(parser)


def main() -> int:
    arguments = sys.argv[1:]
    version_only = "--version-only" in arguments
    paths = [Path(argument) for argument in arguments if argument != "--version-only"]
    if not paths:
        print(f"usage: {Path(sys.argv[0]).name} [--version-only] FILE.html [FILE.html ...]", file=sys.stderr)
        return 2
    failed = False
    for path in paths:
        errors = validate(path, version_only=version_only)
        if errors:
            failed = True
            print(f"{path}:", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
            continue
        print(f"{path}: {'date and version' if version_only else 'visual report'} OK")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
