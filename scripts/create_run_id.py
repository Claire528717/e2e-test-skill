#!/usr/bin/env python3
"""Generate a standard E2E run ID."""

from __future__ import annotations

import argparse
import json
import random
import re
import string
from datetime import datetime


DEFAULT_PREFIX = "E2E"
RANDOM_ALPHABET = string.ascii_uppercase + string.digits


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "feature"


def random_suffix(length: int = 4) -> str:
    return "".join(random.SystemRandom().choice(RANDOM_ALPHABET) for _ in range(length))


def create_run_id(
    feature: str,
    *,
    prefix: str = DEFAULT_PREFIX,
    timestamp: str | None = None,
    suffix: str | None = None,
) -> str:
    feature_slug = slugify(feature)
    timestamp = timestamp or datetime.now().strftime("%Y%m%d%H%M")
    suffix = (suffix or random_suffix()).upper()
    return f"{prefix}-{feature_slug}-{timestamp}-{suffix}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate an E2E run ID.")
    parser.add_argument("feature", help="Feature or integration name.")
    parser.add_argument("--prefix", default=DEFAULT_PREFIX, help="Run ID prefix.")
    parser.add_argument(
        "--timestamp",
        help="Timestamp in yyyyMMddHHmm format. Defaults to current local time.",
    )
    parser.add_argument(
        "--suffix",
        help="Short random suffix. Defaults to 4 random uppercase letters/digits.",
    )
    parser.add_argument("--json", action="store_true", help="Print structured JSON.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    run_id = create_run_id(
        args.feature,
        prefix=args.prefix,
        timestamp=args.timestamp,
        suffix=args.suffix,
    )
    if args.json:
        print(json.dumps({"run_id": run_id, "feature_slug": slugify(args.feature)}))
    else:
        print(run_id)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
