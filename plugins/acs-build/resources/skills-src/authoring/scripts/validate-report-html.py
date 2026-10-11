#!/usr/bin/env python3
"""Validate a generated Presenter view against the visual report contract.

Checks each card, not just the page: a card without its own visual passes a
page-level "before/after appears somewhere" check, which is how prose-and-table
reports slipped through before.

--version-only checks just the date, revision, and internal links. Use it for
human-readable HTML that is not a finding report: canonical records, roadmaps,
delivery plans, prototypes, and design previews.

Both modes also print wording warnings (the visual contract's Writing rules).
Warnings never change the exit code.
"""

from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
from urllib.parse import unquote

ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATED_FILENAME = re.compile(r"-\d{4}-\d{2}-\d{2}\.html$")
RAW_HEX = re.compile(r"^#[0-9a-fA-F]{3,8}$")
COLOR_ATTRIBUTES = ("fill", "stroke", "stop-color")
VISUAL_MODES = ("compare", "single", "none")
# Calibrated on reference reports: schematic labels stay under 15 words each
# and under ~90 words per diagram; prose drawn as SVG text runs far above both.
MAX_WORDS_PER_LABEL = 14
MAX_WORDS_PER_SVG = 90
# ASD-STE100 limits: a step (an <ol> item) at most 20 words, a description at
# most 25, a paragraph at most 6 sentences. Chinese uses the character limits of
# Simplified Technical Chinese. A card at its sentence limits (title, 1-sentence
# problem, solution and takeaway, 4 short wins, 1 callout) is about 120 words.
MAX_WORDS_PER_STEP = 20
MAX_WORDS_PER_SENTENCE = 25
MAX_CJK_CHARS_PER_STEP = 35
MAX_CJK_CHARS_PER_SENTENCE = 45
MAX_SENTENCES_PER_PARAGRAPH = 6
MAX_WORDS_PER_CARD_PROSE = 120
MAX_DE_PER_CLAUSE = 3
PLAIN_WORDS = (
    (r"\butili[sz](e|es|ed|ing|ation)\b", "use"),
    (r"\bcommence[sd]?\b", "start"),
    (r"\bprior to\b", "before"),
    (r"\bin order to\b", "to"),
    # Verb only: "leverage" the noun is an architecture lens term.
    (r"\bleverag(es|ed|ing)\b|\bto leverage\b", "use"),
    (r"\bfacilitat(e|es|ed|ing)\b", "help"),
    (r"\ba number of\b", "the actual count"),
    (r"\bit(?:'s| is) worth noting\b", "delete it"),
    (r"\bbasically\b", "delete it"),
    (r"\bwith regard to\b", "about"),
    (r"\bvarious\b", "name them"),
    (r"\brobust\b", "say what it withstands"),
    (r"进行(?!中)", "use the verb alone: 进行优化 → 优化"),
    (r"加以", "use the verb alone: 加以说明 → 说明"),
    (r"赋能|闭环|至关重要", "say the concrete effect"),
)
CJK_CHAR = re.compile(r"[぀-ヿ一-鿿]")
SENTENCE_END = re.compile(r"(?<=[.!?])\s+|(?<=[。！？；])")
CLAUSE_END = re.compile(r"[，、,。！？；]")
WORDING_BLOCKS = {"p", "li", "td", "th", "dd", "summary", "caption", "figcaption", "h1", "h2", "h3", "h4", "h5", "h6"}
# Code, diagrams, and struck-out counter-examples are not prose.
WORDING_SKIPPED = {"script", "style", "svg", "pre", "code", "s", "del"}


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
    # A browser percent-decodes the fragment before matching it against an id,
    # so "#ticket-a%2Fb" resolves to id="ticket-a/b". Compare what it resolves to.
    return [f"broken internal link #{target}" for target in re.findall(r'href=["\']#([^"\']+)', markup) if unquote(target) not in anchors]


@dataclass
class Block:
    tag: str
    location: str
    is_step: bool
    text: list[str] = field(default_factory=list)


class WordingParser(HTMLParser):
    """Collect visible prose per block element, and per card outside <details>."""

    def __init__(self) -> None:
        super().__init__()
        self.blocks: list[Block] = []
        self.card_words: dict[str, int] = {}
        self._open_blocks: list[Block] = []
        self._lists: list[str] = []
        self._skipped: list[str] = []
        self._card: str | None = None
        self._details_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self._skipped:
            if tag == self._skipped[-1]:
                self._skipped.append(tag)
            return
        if tag in WORDING_SKIPPED:
            self._skipped.append(tag)
            return
        attrs_map = {name: value or "" for name, value in attrs}
        if tag == "article" and "card" in attrs_map.get("class", "").split():
            self._card = attrs_map.get("id") or f"<article> #{len(self.card_words) + 1}"
            self.card_words[self._card] = 0
        if tag == "details":
            self._details_depth += 1
        if tag in ("ol", "ul"):
            self._lists.append(tag)
        if tag in WORDING_BLOCKS:
            is_step = tag == "li" and bool(self._lists) and self._lists[-1] == "ol"
            self._open_blocks.append(Block(tag, self._card or "page", is_step))

    def handle_endtag(self, tag: str) -> None:
        if self._skipped:
            if tag == self._skipped[-1]:
                self._skipped.pop()
            return
        if tag == "article":
            self._card = None
        if tag == "details" and self._details_depth:
            self._details_depth -= 1
        if tag in ("ol", "ul") and self._lists:
            self._lists.pop()
        # Close the matching block and any block the HTML left implicitly open.
        if any(block.tag == tag for block in self._open_blocks):
            while self._open_blocks:
                block = self._open_blocks.pop()
                self.blocks.append(block)
                if block.tag == tag:
                    break

    def handle_data(self, data: str) -> None:
        if self._skipped:
            return
        if self._open_blocks:
            self._open_blocks[-1].text.append(data)
        if self._card and not self._details_depth:
            self.card_words[self._card] += len(data.split())


def sentence_length(sentence: str) -> tuple[int, bool]:
    """Return (length, counted_in_cjk_chars). CJK-dominant text counts characters."""
    cjk_chars = len(CJK_CHAR.findall(sentence))
    latin_words = len(CJK_CHAR.sub(" ", sentence).split())
    if cjk_chars > latin_words:
        return cjk_chars + latin_words, True
    return len(sentence.split()), False


def excerpt(text: str) -> str:
    return text if len(text) <= 60 else text[:57] + "..."


def check_sentences(block: Block) -> list[str]:
    warnings: list[str] = []
    text = " ".join("".join(block.text).split())
    sentences = [sentence for sentence in SENTENCE_END.split(text) if sentence.strip()]
    for sentence in sentences:
        length, in_chars = sentence_length(sentence)
        if in_chars:
            limit, unit = (MAX_CJK_CHARS_PER_STEP if block.is_step else MAX_CJK_CHARS_PER_SENTENCE), "characters"
        else:
            limit, unit = (MAX_WORDS_PER_STEP if block.is_step else MAX_WORDS_PER_SENTENCE), "words"
        if length > limit:
            kind = "step" if block.is_step else "sentence"
            warnings.append(f"{block.location}: {kind} has {length} {unit} (max {limit}); split it: \"{excerpt(sentence)}\"")
        for clause in CLAUSE_END.split(sentence):
            if clause.count("的") > MAX_DE_PER_CLAUSE:
                warnings.append(f"{block.location}: more than {MAX_DE_PER_CLAUSE} 的 in one clause: \"{excerpt(clause)}\"")
    if block.tag == "p" and len(sentences) > MAX_SENTENCES_PER_PARAGRAPH:
        warnings.append(f"{block.location}: paragraph has {len(sentences)} sentences (max {MAX_SENTENCES_PER_PARAGRAPH}); use a list: \"{excerpt(text)}\"")
    for pattern, replacement in PLAIN_WORDS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            warnings.append(f"{block.location}: \"{match.group(0)}\" → {replacement}")
    return warnings


def lint_wording(path: Path) -> list[str]:
    """Warn where visible prose breaks the Writing rules. Never an error."""
    parser = WordingParser()
    parser.feed(path.read_text(encoding="utf-8"))
    warnings = [warning for block in parser.blocks for warning in check_sentences(block)]
    for card, words in parser.card_words.items():
        if words > MAX_WORDS_PER_CARD_PROSE:
            warnings.append(f"card {card}: {words} words of prose outside <details> (max {MAX_WORDS_PER_CARD_PROSE}); move evidence into <details>")
    return warnings


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
        warnings = lint_wording(path)
        if errors:
            failed = True
            print(f"{path}:", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
        else:
            print(f"{path}: {'date and version' if version_only else 'visual report'} OK")
        for warning in warnings:
            print(f"  warning: {warning}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
