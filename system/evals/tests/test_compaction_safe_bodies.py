"""B21 static truncation contracts, not model behavior or a host compaction run.

No tokenizer dependency: one token per UTF-8 byte is a conservative upper bound
for byte-fallback tokenizers, where every text token consumes at least one byte.
This is deliberately NOT the usual bytes/4 estimate. Count the entire SKILL.md,
including metadata, declarations, and injected shared semantics. Host wrappers
and the aggregate reattachment budget are outside this per-skill text check.
The integrated review core exceeds that byte proxy: measure it with an explicitly
configured local tokenizer via ACS_COMPACTION_PYTHON, ACS_COMPACTION_PYTHONPATH,
and ACS_COMPACTION_TOKENIZER. Missing configuration is an explicit skipped check,
not compaction proof. A cached tokenizer does not certify a current host version.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from functools import lru_cache
from pathlib import Path

from test_packages import builder, validator
from test_security_evidence import SECURITY_CORE_RULES

ROOT = Path(__file__).resolve().parents[3]
SUITE = ROOT / "system"
LIMIT = 5000
END = "<!-- compaction-core:end -->"
# Named source contracts: these checks assert authored text survives, not that
# an independently invoked model follows it. Review still checks semantic loss.
CONTRACTS = {
    "acs-design-interaction-flow": (
        "LOADING/EMPTY/ERROR/SUCCESS/PARTIAL", "structure approval/lock precedes visuals",
        "Explicitly reopen", "ONLY approved/reopened", "44×44px", "reduced motion",
        "Persistent", "acs-write-prd", "questioning.md", "--version-only",
        "live regions for dynamic state updates and error announcements",
    ),
    "acs-shape-solution": (
        "Yellow/Red/disputed/assumption-only", "Label", "Scope postures",
        "greenfield uses problem/demand context", "Existing-product work needing a missing/stale baseline",
        "**Expansion**", "**Selective expansion**", "**Hold**", "**Reduction**",
        "Every addition or removal requires explicit user opt-in",
        "skipped or unanswered choice is pending", "Pending additions outside/cuts inside",
        "NOT in scope:", "C/D forbid full depth", "Confirm scenario/experience/first value",
        "validate-product-memory.py", "--version-only",
    ),
    "acs-visual-design-variants": (
        "STOP if missing", "CANNOT change", "variant-{a,b,c}.html", "five states",
        "max 3 iterations", "Persistent Memory", 'data-fidelity="styled"',
        "no invented colors/fonts", "WCAG AA", "--version-only",
    ),
    "acs-design-system-create": (
        "validate/use (stop)", "On approval write", "≤3 iterations",
        "Papyrus, Comic Sans, Lobster, Impact, Jokerman", "system-ui need strong justification",
        "ONE decisive accent", "4.5:1", "44×44px", "3px focus",
        "Persistent Memory", "--version-only",
    ),
    "acs-review-code-quality": (
        "invalid/empty → stop", "Spec unassessed", "failures inline/unassessed",
        "Always inline", "If you cannot quote the motivating line, the finding is unverified",
        "Cap 5/10, never raise", "Code that handles a deliverable is not the deliverable",
        "`UNVERIFIABLE`, not `DONE`", "excluded from main findings, priorities, and blocking verdicts",
        "A static code review cannot stand in for executed acceptance evidence",
        "Standards and Spec separate", "HIGH/MEDIUM Critical → NOT-READY", "prompts need evals",
        *SECURITY_CORE_RULES,
    ),
    "acs-design-implement": (
        "STOP if missing", 'data-structure="locked"', "LOADING/EMPTY/ERROR/SUCCESS/PARTIAL",
        "no hardcoded colors/spacing", "EVERY fix/reason", 'data-fidelity="implemented"',
        "no second synchronized UI", "44×44px", "375px", "--version-only",
    ),
    "acs-analyze-test-gaps": (
        "Identify critical business paths", "Map existing tests statically",
        "Run standard tests once", "Compute focused gaps", "ALL four steps",
        "≤8 flows/20 gaps/10 P0s", "Source/tests/config/CI read-only", "no auto-fix",
        "code bug → test broken → environment", "accepted base", "final diff",
        "block green", "Unavailable = incomplete", "never alter checks/thresholds/exceptions/CI",
        "Missing criteria block readiness", "Last updated:",
    ),
}


def truncate_conservatively(text: str, budget: int = LIMIT) -> str:
    """Cut at at most budget UTF-8 bytes without retaining a partial character."""
    return text.encode("utf-8")[:budget].decode("utf-8", errors="ignore")


@lru_cache(maxsize=None)
def review_token_prefix(text: str) -> tuple[str, int]:
    """Use only an explicitly supplied local tokenizer; never fetch or install."""
    tokenizer = os.environ.get("ACS_COMPACTION_TOKENIZER")
    if not tokenizer:
        raise unittest.SkipTest("review compaction UNVERIFIED: set ACS_COMPACTION_TOKENIZER to a local tokenizer JSON")
    executable = os.environ.get("ACS_COMPACTION_PYTHON", sys.executable)
    environment = os.environ.copy()
    if "ACS_COMPACTION_PYTHONPATH" in environment:
        environment["PYTHONPATH"] = environment["ACS_COMPACTION_PYTHONPATH"]
    script = """
import json, sys
from tokenizers import Tokenizer
tokenizer = Tokenizer.from_file(sys.argv[1])
text = sys.stdin.read()
encoded = tokenizer.encode(text)
print(json.dumps([tokenizer.decode(encoded.ids[:5000], skip_special_tokens=False), len(encoded.ids)]))
"""
    result = subprocess.run([executable, "-c", script, tokenizer], input=text,
                            text=True, capture_output=True, env=environment, check=True)
    prefix, count = json.loads(result.stdout)
    digest = hashlib.sha256(Path(tokenizer).read_bytes()).hexdigest()
    print(f"Review compaction: {count} tokens; tokenizer SHA256 {digest}")
    return prefix, count


def core_errors(name: str, text: str, prefix: str | None = None) -> list[str]:
    if prefix is None:
        prefix = truncate_conservatively(text)
    required = ("## Context contract", "## Completion criteria and hard rules", END,
                *CONTRACTS[name])
    errors = [f"missing in prefix: {rule}" for rule in required if rule not in prefix]
    if END in text and text.split(END, 1)[1].strip():
        errors.append("content after core marker")
    return errors


class CompactionSafeBodiesTests(unittest.TestCase):
    def sources(self) -> dict[str, Path]:
        return {name: next((SUITE / "skills-src").glob(f"**/{name}/SKILL.md"))
                for name in CONTRACTS}

    def assert_core_bound(self, name: str, text: str) -> None:
        if name == "acs-review-code-quality":
            prefix, count = review_token_prefix(text)
            self.assertEqual(core_errors(name, text, prefix), [])
            self.assertLessEqual(count, LIMIT)
        else:
            self.assertEqual(core_errors(name, text), [])
            self.assertLessEqual(len(text.encode()), LIMIT)
            self.assertEqual(truncate_conservatively(text), text)

    def test_source_cores_survive_conservative_truncation(self) -> None:
        for name, source in self.sources().items():
            with self.subTest(skill=name):
                text = source.read_text()
                self.assertEqual(text.count("[Shared semantics]"), 1)
                self.assert_core_bound(name, text)

    def test_plugin_and_relocated_standalone_cores_include_shared_injection(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            sources = self.sources()
            plugin = root / "plugin"
            builder.build_package(SUITE, plugin, {n: p.parent for n, p in sources.items()},
                                  name="b21-fixture", description="B21 static check", version="0.0.0")
            self.assertEqual(validator.validate_package(plugin), [])
            for name, source in sources.items():
                exported = root / "export"
                builder.build_standalone_skill(SUITE, exported, source.parent)
                installed = root / name
                exported.rename(installed)
                self.assertEqual(validator.validate_package(installed), [])
                for path in (installed / "SKILL.md", plugin / "skills" / name / "SKILL.md"):
                    with self.subTest(skill=name, package=path.parent):
                        text = path.read_text()
                        self.assertNotIn("[Shared semantics]", text)
                        self.assertIn("existing authorization persists", text)
                        self.assertIn("save-before-handoff", text)
                        self.assert_core_bound(name, text)

    def test_overflow_and_removed_rules_fail_even_with_marker(self) -> None:
        for name, source in self.sources().items():
            text = source.read_text()
            with self.subTest(skill=name):
                self.assertIn(f"missing in prefix: {END}", core_errors(name, "x" * LIMIT + text))
                for rule in CONTRACTS[name]:
                    self.assertIn(f"missing in prefix: {rule}",
                                  core_errors(name, text, text.replace(rule, "REMOVED")))
                self.assertIn("content after core marker", core_errors(name, text + "Hidden hard rule"))

    def test_review_token_prefix_rejects_overflow(self) -> None:
        name = "acs-review-code-quality"
        text = self.sources()[name].read_text()
        overflow = "x " * LIMIT + text
        prefix, count = review_token_prefix(overflow)
        self.assertGreater(count, LIMIT)
        self.assertIn(f"missing in prefix: {END}", core_errors(name, overflow, prefix))
        self.assertIn("missing in prefix: " + SECURITY_CORE_RULES[-1],
                      core_errors(name, overflow, prefix))

    def test_cut_uses_bytes_and_drops_partial_unicode(self) -> None:
        self.assertEqual(truncate_conservatively("a" * 4999 + "→suffix"), "a" * 4999)
        self.assertEqual(truncate_conservatively("a" * 4997 + "→suffix"), "a" * 4997 + "→")
        self.assertEqual(len(truncate_conservatively("x" * 6000)), LIMIT)


if __name__ == "__main__":
    unittest.main()
