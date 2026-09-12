#!/usr/bin/env python3
"""Validate product-memory HTML documents (discovery.html / product.html).

Checks the structural contract defined in
system/skills-src/craft/context/init-context/references/product-memory.md:

  - every <article> has a non-empty, document-unique id
  - every <article> has a data-kind from the closed list; an unknown kind
    is an error unless a data-kind-reason attribute records why (then a
    warning naming the closed list)
  - every record <article> sits inside a <section> whose id is one of the
    shared section ids (unknown section id -> warning)
  - every local href="#..." resolves to an id in the same document
  - a visible "Last updated" marker is present (warning if missing)
  - every roadmap-ticket <article> carries data-ticket-type="spec"|"prototype"
    (and only roadmap-tickets carry that attribute)
  - capability <article> commitment attributes: data-commitment from the
    closed list, data-depth tokens from the closed list, depth only on
    committed/reduced records, and a named depth on every reduced record
    (and only capabilities carry either attribute)

Usage:
    python3 scripts/validate-product-memory.py <file.html> [<file2.html> ...]

Exit codes: 0 clean (warnings allowed), 1 any error, 2 usage/parse failure.
Output lines: path:line: ERROR|WARNING: message
"""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path

RECORD_KINDS = {
    "mission",
    "roadmap-ticket",
    "research-coverage",
    "persona",
    "problem",
    "demand-assessment",
    "vision",
    "capability",
    "journey",
    "gap",
    "opportunity",
    "question",
    "assumption",
    "evidence",
    "decision",
    "constraint",
    "risk",
    "metric",
}

# Set by define-outcomes on capability records. Commitment says whether the
# product promises the capability; depth says how far it goes. The two are
# orthogonal -- a capability can ship narrower than it was shaped.
COMMITMENT_LEVELS = {
    "committed",
    "reduced",
    "deferred",
    "excluded",
    "open",
}

DEPTH_VALUES = {
    "full",
    "narrowed",
    "fixed",
    "manual",
}

# Depth is meaningful only where something is actually being promised.
DEPTH_BEARING_COMMITMENTS = {"committed", "reduced"}

SECTION_IDS = {
    "overview",
    "roadmap",
    "research",
    "users-problems",
    "capabilities-journeys",
    "gaps-opportunities",
    "questions-assumptions",
    "evidence",
    "scope-decisions",
    "risks-measures",
}


class MemoryDocParser(HTMLParser):
    """Collect ids, articles, sections, and local links with line numbers."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.all_ids: dict[str, int] = {}  # id -> first line seen
        self.duplicate_ids: list[tuple[str, int]] = []
        # (line, id, data-kind, data-kind-reason, enclosing section id,
        #  data-ticket-type, data-commitment, data-depth)
        self.articles: list[
            tuple[
                int,
                str | None,
                str | None,
                str | None,
                str | None,
                str | None,
                str | None,
                str | None,
            ]
        ] = []
        self.local_links: list[tuple[int, str]] = []  # (line, target id)
        self.text_chunks: list[str] = []
        self._section_stack: list[str | None] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {name: (value or "") for name, value in attrs}
        line = self.getpos()[0]

        element_id = attr_map.get("id")
        if element_id:
            if element_id in self.all_ids:
                self.duplicate_ids.append((element_id, line))
            else:
                self.all_ids[element_id] = line

        if tag == "section":
            self._section_stack.append(element_id)
        elif tag == "article":
            enclosing = next(
                (sid for sid in reversed(self._section_stack) if sid), None
            )
            self.articles.append(
                (
                    line,
                    element_id,
                    attr_map.get("data-kind"),
                    attr_map.get("data-kind-reason"),
                    enclosing,
                    attr_map.get("data-ticket-type"),
                    attr_map.get("data-commitment"),
                    attr_map.get("data-depth"),
                )
            )
        elif tag == "a":
            href = attr_map.get("href", "")
            if href.startswith("#") and len(href) > 1:
                self.local_links.append((line, href[1:]))

    def handle_endtag(self, tag: str) -> None:
        if tag == "section" and self._section_stack:
            self._section_stack.pop()

    def handle_data(self, data: str) -> None:
        self.text_chunks.append(data)


def validate_file(path: Path) -> tuple[int, int]:
    """Validate one file. Returns (error_count, warning_count)."""
    errors = 0
    warnings = 0

    def report(line: int, level: str, message: str) -> None:
        print(f"{path}:{line}: {level}: {message}")

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"{path}:0: ERROR: cannot read file: {exc}")
        return (1, 0)

    parser = MemoryDocParser()
    parser.feed(text)
    parser.close()

    for dup_id, line in parser.duplicate_ids:
        report(line, "ERROR", f'duplicate id "{dup_id}"')
        errors += 1

    kinds_sorted = ", ".join(sorted(RECORD_KINDS))
    commitments_sorted = ", ".join(sorted(COMMITMENT_LEVELS))
    depths_sorted = ", ".join(sorted(DEPTH_VALUES))
    for (
        line,
        article_id,
        kind,
        kind_reason,
        section_id,
        ticket_type,
        commitment,
        depth,
    ) in parser.articles:
        label = f'<article id="{article_id}">' if article_id else "<article> (no id)"
        if not article_id:
            report(line, "ERROR", "<article> without an id")
            errors += 1
        if kind is None or kind == "":
            report(line, "ERROR", f"{label} without data-kind")
            errors += 1
        elif kind not in RECORD_KINDS:
            if kind_reason:
                report(
                    line,
                    "WARNING",
                    f'unknown data-kind "{kind}" (reason recorded: "{kind_reason}"); '
                    f"closed list: {kinds_sorted}",
                )
                warnings += 1
            else:
                report(
                    line,
                    "ERROR",
                    f'unknown data-kind "{kind}" and no data-kind-reason attribute; '
                    f"closed list: {kinds_sorted}",
                )
                errors += 1
        if section_id is None:
            report(
                line,
                "WARNING",
                f"{label} is not inside a <section> with an id",
            )
            warnings += 1
        elif section_id not in SECTION_IDS:
            report(
                line,
                "WARNING",
                f"{label} is inside unknown section "
                f'"{section_id}"; shared sections: {", ".join(sorted(SECTION_IDS))}',
            )
            warnings += 1
        if kind == "roadmap-ticket":
            if ticket_type not in ("spec", "prototype"):
                report(
                    line,
                    "ERROR",
                    f'{label} roadmap-ticket needs data-ticket-type="spec" or "prototype"'
                    f' (got {ticket_type!r})',
                )
                errors += 1
        elif ticket_type is not None:
            report(
                line,
                "WARNING",
                f"{label} carries data-ticket-type but is not a roadmap-ticket",
            )
            warnings += 1

        if kind == "capability":
            if commitment is not None and commitment not in COMMITMENT_LEVELS:
                report(
                    line,
                    "ERROR",
                    f'{label} unknown data-commitment "{commitment}"; '
                    f"closed list: {commitments_sorted}",
                )
                errors += 1
            if depth is not None:
                depth_tokens = depth.split()
                unknown = [tok for tok in depth_tokens if tok not in DEPTH_VALUES]
                if not depth_tokens:
                    report(line, "ERROR", f"{label} empty data-depth")
                    errors += 1
                elif unknown:
                    report(
                        line,
                        "ERROR",
                        f'{label} unknown data-depth value(s) {", ".join(unknown)}; '
                        f"closed list: {depths_sorted}",
                    )
                    errors += 1
                if commitment not in DEPTH_BEARING_COMMITMENTS:
                    held = (
                        f'is "{commitment}"' if commitment else "is not set"
                    )
                    report(
                        line,
                        "ERROR",
                        f"{label} carries data-depth but data-commitment "
                        f"{held}; depth applies only to "
                        f'{" and ".join(sorted(DEPTH_BEARING_COMMITMENTS))}',
                    )
                    errors += 1
            elif commitment == "reduced":
                report(
                    line,
                    "ERROR",
                    f'{label} is data-commitment="reduced" without a data-depth; '
                    "a reduction must name the depth it ships at",
                )
                errors += 1
        else:
            for attr_name, attr_value in (
                ("data-commitment", commitment),
                ("data-depth", depth),
            ):
                if attr_value is not None:
                    report(
                        line,
                        "WARNING",
                        f"{label} carries {attr_name} but is not a capability",
                    )
                    warnings += 1

    for line, target in parser.local_links:
        if target not in parser.all_ids:
            report(line, "ERROR", f'local link "#{target}" does not resolve')
            errors += 1

    if "last updated" not in " ".join(parser.text_chunks).lower():
        report(1, "WARNING", 'no visible "Last updated" marker found')
        warnings += 1

    status = "FAIL" if errors else "OK"
    print(f"{path}: {status} — {errors} error(s), {warnings} warning(s)")
    return (errors, warnings)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2

    total_errors = 0
    for arg in argv[1:]:
        path = Path(arg)
        if not path.exists():
            print(f"{path}:0: ERROR: file not found")
            total_errors += 1
            continue
        errors, _ = validate_file(path)
        total_errors += errors

    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
