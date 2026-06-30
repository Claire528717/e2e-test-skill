#!/usr/bin/env python3
"""Validate post-run E2E evidence without making the skill heavy.

The check is intentionally small:
- passed UI cases must have at least one screenshot file under the evidence dir;
- P0 passed cases must also have at least one independent evidence file.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


CASE_ID_PATTERN = re.compile(r"\b[A-Z][A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3,}\b")
SHORT_ID_PATTERN = re.compile(r"^\d{3}$")
CASE_HEADING_PATTERN = re.compile(r"^###\s+(?P<heading>.+)$", re.M)
EVIDENCE_DIR_PATTERN = re.compile(
    r"(?:Evidence directory|证据目录)\s*[:：]\s*`?(?P<path>[^`\n]+)`?", re.I
)
TABLE_ROW_PATTERN = re.compile(r"^\|(?P<row>.*)\|\s*$", re.M)

PASSED_TERMS = ("passed", "pass", "通过", "修复后通过", "✅")
NON_FINAL_TERMS = (
    "草稿",
    "draft",
    "blocked",
    "阻塞",
    "skipped",
    "跳过",
    "failed",
    "失败",
    "not run",
    "未执行",
)
SCREENSHOT_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
INDEPENDENT_EXTENSIONS = {".txt", ".json", ".log", ".csv", ".xml", ".har"}


@dataclass(frozen=True)
class PassedCase:
    case_id: str
    title: str
    priority: str


def strip_fenced_blocks(markdown: str) -> str:
    lines: list[str] = []
    in_fence = False
    for line in markdown.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            lines.append("")
            continue
        lines.append("" if in_fence else line)
    return "\n".join(lines)


def case_metadata(markdown: str) -> tuple[dict[str, str], dict[str, str]]:
    priorities: dict[str, str] = {}
    by_suffix: dict[str, str] = {}
    for match in CASE_HEADING_PATTERN.finditer(strip_fenced_blocks(markdown)):
        heading = match.group("heading")
        case_match = CASE_ID_PATTERN.search(heading)
        if not case_match:
            continue
        case_id = case_match.group(0)
        priority_match = re.search(r"\bP[0-2]\b", heading, re.I)
        priorities[case_id] = priority_match.group(0).upper() if priority_match else ""
        suffix = case_id.rsplit("-", 1)[-1]
        by_suffix[suffix] = case_id
    return priorities, by_suffix


def is_separator_row(row: str) -> bool:
    stripped = row.replace("|", "").strip()
    return bool(stripped) and set(stripped) <= {"-", ":"}


def is_passed_status(cells: list[str]) -> bool:
    status_cells = cells[2:5] if len(cells) >= 5 else cells
    status_text = " ".join(status_cells).lower()
    if any(term.lower() in status_text for term in NON_FINAL_TERMS):
        return False
    return any(term.lower() in status_text for term in PASSED_TERMS)


def row_case_id(cells: list[str], row: str, by_suffix: dict[str, str]) -> str | None:
    ids = CASE_ID_PATTERN.findall(row)
    if ids:
        return ids[0]
    if cells:
        short_id = cells[0].strip()
        if SHORT_ID_PATTERN.match(short_id):
            return by_suffix.get(short_id)
    return None


def extract_passed_cases(markdown: str) -> list[PassedCase]:
    priorities, by_suffix = case_metadata(markdown)
    passed: dict[str, PassedCase] = {}
    for match in TABLE_ROW_PATTERN.finditer(strip_fenced_blocks(markdown)):
        row = match.group("row")
        if is_separator_row(row):
            continue
        cells = [cell.strip() for cell in row.split("|")]
        case_id = row_case_id(cells, row, by_suffix)
        if not case_id or not is_passed_status(cells):
            continue
        title = cells[1] if len(cells) > 1 else ""
        passed[case_id] = PassedCase(case_id, title, priorities.get(case_id, ""))
    return sorted(passed.values(), key=lambda item: item.case_id)


def find_evidence_dir(markdown: str, plan_path: Path, override: str | None) -> Path | None:
    if override:
        return Path(override)
    match = EVIDENCE_DIR_PATTERN.search(markdown)
    if not match:
        return None
    raw_path = match.group("path").strip()
    evidence_dir = Path(raw_path)
    if evidence_dir.is_absolute():
        return evidence_dir
    return (plan_path.parent.parent / evidence_dir).resolve()


def files_for_case(evidence_dir: Path, case_id: str) -> list[Path]:
    suffix = case_id.rsplit("-", 1)[-1].lower()
    tokens = {case_id.lower(), suffix}
    return [
        path
        for path in evidence_dir.rglob("*")
        if path.is_file() and any(token in path.name.lower() for token in tokens)
    ]


def validate_evidence(plan_path: Path, evidence_dir_override: str | None = None) -> list[str]:
    markdown = plan_path.read_text(encoding="utf-8-sig")
    evidence_dir = find_evidence_dir(markdown, plan_path, evidence_dir_override)
    passed_cases = extract_passed_cases(markdown)

    if not passed_cases:
        return ["No passed executed cases found; evidence completeness cannot be checked."]
    if evidence_dir is None:
        return ["No evidence directory found. Add 'Evidence directory:' or '证据目录：' to the plan."]
    if not evidence_dir.exists():
        return [f"Evidence directory does not exist: {evidence_dir}"]

    issues: list[str] = []
    for case in passed_cases:
        case_files = files_for_case(evidence_dir, case.case_id)
        screenshots = [path for path in case_files if path.suffix.lower() in SCREENSHOT_EXTENSIONS]
        independent = [path for path in case_files if path.suffix.lower() in INDEPENDENT_EXTENSIONS]

        if not screenshots:
            issues.append(f"{case.case_id} is passed but has no screenshot evidence in {evidence_dir}.")
        if case.priority == "P0" and not independent:
            issues.append(f"{case.case_id} is P0 passed but has no independent evidence file in {evidence_dir}.")

    return issues


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate post-run E2E evidence files.")
    parser.add_argument("plan", type=Path, help="Path to the Markdown test plan.")
    parser.add_argument("--evidence-dir", help="Override the evidence directory declared in the plan.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    issues = validate_evidence(args.plan, args.evidence_dir)
    if not issues:
        print(f"OK: {args.plan} has screenshot evidence for passed UI cases.")
        return 0

    print(f"FAILED: {args.plan} has {len(issues)} evidence issue(s).")
    for issue in issues:
        print(f"- {issue}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
