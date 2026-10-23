#!/usr/bin/env python3
"""Validate collected evidence against coordinator-supplied source identities.

This checks recorded bindings, not whether commands actually ran or criteria are
covered. The coordinator must resolve BASE and the current tree independently.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import sys


TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})")


def evidence_errors(evidence: object, *, base: str, revision: str) -> list[str]:
    if not isinstance(evidence, dict) or not isinstance(evidence.get("rows"), list) or not evidence["rows"]:
        return ["INVALID-EVIDENCE: expected an object with nonempty rows"]
    errors = []
    if evidence.get("base") != base:
        errors.append("BASE-MISMATCH: evidence does not match dispatch BASE")
    for index, row in enumerate(evidence["rows"], 1):
        prefix = f"row {index}: "
        if not isinstance(row, dict):
            errors.append(prefix + "INVALID-EVIDENCE: expected an evidence row object")
            continue
        missing = [field for field in ("criterion", "command", "revision", "timestamp", "result")
                   if not isinstance(row.get(field), str) or not row[field].strip()]
        if missing:
            errors.append(prefix + "INVALID-FIELD: " + ", ".join(missing))
            continue
        if row["revision"] != revision:
            errors.append(prefix + "STALE-REVISION: evidence does not match current completion source")
        try:
            if not TIMESTAMP.fullmatch(row["timestamp"]):
                raise ValueError("expected RFC 3339 timestamp with timezone")
            datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00"))
        except ValueError:
            errors.append(prefix + "INVALID-TIMESTAMP: expected RFC 3339 date-time with timezone")
        if row["result"] != "passed":
            errors.append(prefix + "CHECK-NOT-PASSED: " + row["result"])
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", type=Path, help="JSON evidence sidecar")
    parser.add_argument("--base", required=True, help="immutable dispatch source identity")
    parser.add_argument("--revision", required=True, help="independently resolved current completion identity")
    args = parser.parse_args()
    if not args.base.strip() or not args.revision.strip():
        parser.error("--base and --revision must be nonempty")
    try:
        evidence = json.loads(args.evidence.read_text())
    except (OSError, ValueError) as error:
        print(f"INVALID-EVIDENCE: {error}", file=sys.stderr)
        return 1
    errors = evidence_errors(evidence, base=args.base, revision=args.revision)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"PASS: {len(evidence['rows'])} evidence row(s) bound to {args.revision}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
