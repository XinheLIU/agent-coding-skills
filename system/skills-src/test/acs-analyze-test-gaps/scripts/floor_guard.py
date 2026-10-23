#!/usr/bin/env python3
"""Report possible check silencing in merge-base → working-tree changes; never fix."""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


class GuardError(Exception):
    """An incomplete scan must not look clean."""


def git(root: Path, *args: str) -> bytes:
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True)
    if result.returncode:
        raise GuardError("Git input unavailable; verify repository and base revision")
    return result.stdout


def is_test(path: str) -> bool:
    return bool(re.search(r"(^|/)(tests?|__tests__|specs?|e2e)/|(^|/)(test_|spec_)|[._](test|spec)[._]|Test\.[^/]+$", path))


SUPPRESSION = re.compile(
    r"@ts-(?:ignore|nocheck)|eslint-disable|biome-ignore|#\s*noqa|#\s*type:\s*ignore|"
    r"istanbul ignore|c8 ignore|nosemgrep|gitleaks:allow|Stryker disable|noinspection"
)
SKIP = re.compile(
    r"\.(?:skip|todo|Skip|Skipf|skipTest)\s*\(|\b(?:xit|xdescribe)\s*\(|"
    r"@(?:pytest\.mark\.(?:skip|skipif|xfail)|unittest\.(?:skip|skipIf|skipUnless)|Disabled|Ignore)\b"
)
ASSERTION = re.compile(r"\b(?:assert\w*|expect|should\w*)\s*(?:\(|\s)|\.should\b")
STUB = re.compile(
    r"\bcatch\s*(?:\([^)]*\))?\s*\{\s*(?:(?://[^\n]*\n|/\*.*?\*/)\s*)*\}|"
    r"\bexcept[^\n]*:\s*(?:#[^\n]*\n\s*)?(?:pass\b|\.\.\.)|"
    r"\braise\s+NotImplementedError\b|\bthrow\s+new\s+\w*Error\([^\n]*[Nn]ot implemented",
    re.DOTALL,
)
NUMBER = re.compile(r"(?<![\w.])-?\d+(?:\.\d+)?")
MINIMUM = re.compile(r"(?:>=|≥|>|at least|minimum|min|no less than|must not fall|must not drop)\s*$", re.I)
MAXIMUM = re.compile(r"(?:<=|≤|<|at most|maximum|max|no more than|under|below|must not grow|must not exceed)\s*$", re.I)


def thresholds(text: str) -> dict[str, list[float]]:
    result: dict[str, list[float]] = {"min": [], "max": [], "unknown": []}
    for match in NUMBER.finditer(text):
        prefix = text[:match.start()]
        suffix = text[match.end():]
        direction = "unknown"
        if MINIMUM.search(prefix) or re.match(r"\s*\S*\s*(?:or more|or higher|must not fall|must not drop)", suffix):
            direction = "min"
        elif MAXIMUM.search(prefix) or re.match(r"\s*\S*\s*(?:or less|or lower|must not grow|must not exceed)", suffix):
            direction = "max"
        result[direction].append(float(match.group()))
    return result


def rules(lines: list[str]) -> dict[tuple[str, str], tuple[int, str]]:
    result = {}
    section = ""
    for line, text in enumerate(lines, 1):
        stripped = text.strip()
        if stripped.startswith("#"):
            section = stripped.lstrip("# ").lower()
        elif stripped.startswith("|"):
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            if cells[0].lower() in {"id", "dimension", "metric", "rule"} or re.fullmatch(r"[-: ]+", cells[0]):
                continue
            key = (section, cells[0])
            if key in result:
                raise GuardError("Duplicate constraint rule IDs; scan cannot pair thresholds reliably")
            result[key] = (line, " | ".join(cells[1:]))
        elif re.match(r"[-*] ", stripped):
            key, _, value = stripped[2:].partition(":")
            result[(section, key)] = (line, value)
    return result


def inspect(path: str, before: str, after: str, deleted: bool) -> list[dict]:
    old, new = before.splitlines(), after.splitlines()
    removed, added, deletion_anchors = set(), set(), set()
    for tag, start, end, new_start, new_end in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
        if tag != "equal":
            removed.update(range(start + 1, end + 1))
            added.update(range(new_start + 1, new_end + 1))
            if end > start:
                deletion_anchors.add(new_start + 1)
    findings = []

    def flag(move: str, line: int, side: str = "new") -> None:
        finding = {"file": path, "line": line, "side": side, "move": move}
        if finding not in findings:
            findings.append(finding)

    if Path(path).name == "CONSTRAINTS.md":
        old_rules, new_rules = rules(old), rules(new)
        for key, (line, text) in new_rules.items():
            if key[0] == "exceptions" and old_rules.get(key, (0, None))[1] != text:
                flag("new-exception-row", line)
        for key, (line, text) in old_rules.items():
            if key[0] == "exceptions":
                continue  # Removing an exception tightens the floor.
            replacement = new_rules.get(key)
            if replacement is None:
                flag("lowered-threshold", line, "old")
                continue
            new_line, new_text = replacement
            if text == new_text:
                continue
            was, now = thresholds(text), thresholds(new_text)
            weakened = False
            for direction in was:
                if len(now[direction]) < len(was[direction]):
                    weakened = True
                for previous, current in zip(was[direction], now[direction]):
                    if (direction == "min" and current < previous or
                            direction == "max" and current > previous or
                            direction == "unknown" and current != previous):
                        weakened = True
            # Non-numeric changes (e.g. command or placement edits) need review too.
            if weakened or NUMBER.sub("#", text) != NUMBER.sub("#", new_text):
                flag("lowered-threshold", new_line)
        return findings

    # Markdown is guidance, not executable checks. Constraint tables are handled above.
    if Path(path).suffix.lower() == ".md":
        return findings
    for line in sorted(added):
        if SUPPRESSION.search(new[line - 1]):
            flag("suppression-comment", line)
        if SKIP.search(new[line - 1]):
            flag("skipped-or-weakened-test", line)
    if is_test(path):
        if deleted:
            flag("skipped-or-weakened-test", 1, "old")
        else:
            for line in sorted(removed):
                if ASSERTION.search(old[line - 1]):
                    flag("skipped-or-weakened-test", line, "old")
    for match in STUB.finditer(after):
        first = after.count("\n", 0, match.start()) + 1
        last = after.count("\n", 0, match.end()) + 1
        touched = added.intersection(range(first, last + 1))
        if touched or deletion_anchors.intersection(range(first, last + 1)):
            flag("stubbed-catch", min(touched) if touched else first)
    return findings


def scan(root: Path, base: str) -> dict:
    root = Path(git(root, "rev-parse", "--show-toplevel").decode().strip())
    base_commit = git(root, "rev-parse", "--verify", "--end-of-options", base + "^{commit}").decode().strip()
    merge_base = git(root, "merge-base", base_commit, "HEAD").decode().strip()
    tracked = git(root, "diff", "--name-only", "--no-renames", "-z", merge_base, "--")
    untracked = git(root, "ls-files", "--others", "--exclude-standard", "-z")
    names = sorted(set(tracked.split(b"\0") + untracked.split(b"\0")) - {b""})
    digest = hashlib.sha256()
    findings = []
    for raw_name in names:
        name = raw_name.decode("utf-8")
        entry = git(root, "ls-tree", "-z", merge_base, "--", ":(literal)" + name)
        before = b""
        if entry:
            mode, kind, oid = entry.split(b"\t", 1)[0].split()
            if kind != b"blob" or mode == b"120000":
                raise GuardError("Changed symlink or submodule is unsupported; review it separately")
            before = git(root, "cat-file", "blob", oid.decode())
        path = root / name
        if path.is_symlink() or (path.exists() and not path.is_file()):
            raise GuardError("Changed symlink or non-file is unsupported; review it separately")
        after = path.read_bytes() if path.exists() else b""
        for data in (raw_name, before, after):
            digest.update(len(data).to_bytes(8, "big"))
            digest.update(data)
        if b"\0" in before + after:
            raise GuardError("Changed binary input is unsupported; scan is incomplete")
        findings.extend(inspect(name, before.decode("utf-8"), after.decode("utf-8"), not path.exists()))
    return {"status": "blocked" if findings else "clean", "green_claim": False,
            "merge_base": merge_base, "diff_sha256": digest.hexdigest(),
            "files_scanned": len(names), "findings": findings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="Accepted branch point/ref; compared through its merge base with HEAD")
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        report = scan(args.repo, args.base)
    except (GuardError, OSError, UnicodeError) as error:
        # Never echo source, subprocess stderr, or filesystem error contents.
        message = str(error) if isinstance(error, GuardError) else "Input unreadable; scan is incomplete"
        print(json.dumps({"status": "unavailable", "green_claim": False, "error": message}))
        return 2
    print(json.dumps(report, sort_keys=True))
    return 1 if report["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
