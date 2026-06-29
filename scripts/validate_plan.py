#!/usr/bin/env python3
"""Validate that an E2E test plan has executable case essentials and PRD coverage gates."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


REQUIRED_SECTIONS = {
    "UI Fidelity Requirement": "UI fidelity requirement",
    "Actor": "actor",
    "UI Operation Path": "UI path",
    "Independent Verification": "independent verification",
    "Evidence To Capture": "evidence",
    "Cleanup": "cleanup",
}

UI_FIDELITY_VIOLATIONS = {
    "setInputFiles": "low-level file injection is valid only after a visible user-triggered affordance; document the visible step instead",
    "hidden input": "hidden DOM controls are not visible user affordances",
    "input[type=file]": "direct file input selectors bypass visible user affordances",
    "dispatchEvent": "synthetic DOM events bypass visible user interaction",
    ".evaluate(": "page or component evaluation can bypass visible user interaction",
    "elementHandle": "low-level element handles can bypass visible user interaction",
    "locator('input": "direct input locators risk bypassing visible labels and controls",
    "locator(\"input": "direct input locators risk bypassing visible labels and controls",
    "localStorage": "storage seeding bypasses login, navigation, or product UI state changes",
    "sessionStorage": "session seeding bypasses login, navigation, or product UI state changes",
    "document.querySelector": "direct DOM selectors can bypass user-visible affordances",
    "style.display": "changing visibility can bypass the product UI path",
    "disabled = false": "forcing enabled state bypasses product validation and UI state",
}

LIST_PREFIX_PATTERN = re.compile(r"^\s*(?:[-*]\s+|\d+\.\s+)?")
PLACEHOLDER_TOKEN_PATTERN = re.compile(r"\{\{[^{}]+\}\}|\{[^{}]+\}")
CASE_ID_PATTERN = re.compile(r"\b[A-Z][A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3,}\b")
COVERAGE_SECTION_PATTERN = re.compile(
    r"^##\s+(?:PRD Coverage Audit|PRD 全量覆盖审计|Requirement Coverage Matrix|需求覆盖矩阵)\s*$",
    re.M,
)
COVERAGE_ROW_PATTERN = re.compile(r"^\|(?P<row>.*)\|\s*$", re.M)
PRD_SIGNAL_TERMS = (
    "prd",
    "需求",
    "验收口径",
    "acceptance",
    "must",
    "必须实现",
    "覆盖矩阵",
)
COVERED_STATUSES = {"covered", "已覆盖"}


@dataclass
class CaseBlock:
    heading: str
    body: str
    line: int


def strip_fenced_blocks(markdown: str) -> str:
    lines = []
    in_fence = False
    for line in markdown.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            lines.append("")
            continue
        lines.append("" if in_fence else line)
    return "\n".join(lines)


def find_cases(markdown: str) -> list[CaseBlock]:
    text = strip_fenced_blocks(markdown)
    heading_pattern = re.compile(r"^###\s+(.+)$", re.M)
    matches = list(heading_pattern.finditer(text))
    cases: list[CaseBlock] = []
    for index, match in enumerate(matches):
        heading = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        line = text[: match.start()].count("\n") + 1
        cases.append(CaseBlock(heading=heading, body=text[start:end], line=line))
    return cases


def section_content(body: str, section: str) -> str | None:
    pattern = re.compile(
        rf"^{re.escape(section)}:\s*$([\s\S]*?)(?=^[A-Z][A-Za-z /-]+:\s*$|\Z)",
        re.M,
    )
    match = pattern.search(body)
    if not match:
        return None
    return match.group(1).strip()


def section_status(value: str | None) -> tuple[bool, bool]:
    """Return (has_content, has_placeholder)."""
    if value is None:
        return False, False
    lines = [line.strip() for line in value.splitlines() if line.strip()]
    has_content = False
    has_placeholder = False
    for line in lines:
        text = LIST_PREFIX_PATTERN.sub("", line).strip()
        if PLACEHOLDER_TOKEN_PATTERN.search(text):
            has_placeholder = True
            continue
        if text.endswith(":"):
            continue
        if text.lower() in {"none", "n/a", "na", "todo", "tbd"}:
            has_placeholder = True
            continue
        if text:
            has_content = True
    return has_content, has_placeholder


def is_separator_row(row: str) -> bool:
    stripped = row.replace("|", "").strip()
    return bool(stripped) and set(stripped) <= {"-", ":"}


def validate_coverage(markdown: str, case_ids: set[str]) -> list[str]:
    issues: list[str] = []
    lowered = markdown.lower()
    has_prd_signal = any(term.lower() in lowered for term in PRD_SIGNAL_TERMS)
    has_coverage_section = bool(COVERAGE_SECTION_PATTERN.search(markdown))

    if has_prd_signal and not has_coverage_section:
        issues.append(
            "Missing PRD coverage audit. Add '## PRD Coverage Audit', '## PRD 全量覆盖审计', "
            "'## Requirement Coverage Matrix', or '## 需求覆盖矩阵' with requirement-to-case mapping."
        )
        return issues

    if not has_coverage_section:
        return issues

    covered_rows = 0
    for row_match in COVERAGE_ROW_PATTERN.finditer(strip_fenced_blocks(markdown)):
        row = row_match.group("row")
        cells = [cell.strip() for cell in row.split("|")]
        if len(cells) < 4 or is_separator_row(row):
            continue
        row_lower = row.lower()
        if "coverage" in row_lower and "case" in row_lower:
            continue
        covered_status = any(cell.lower() in COVERED_STATUSES for cell in cells)
        if not covered_status:
            continue
        covered_rows += 1
        ids = set(CASE_ID_PATTERN.findall(row))
        if not ids:
            issues.append(f"Coverage row marked covered has no case ID: {row.strip()}")
            continue
        missing_ids = sorted(ids - case_ids)
        if missing_ids:
            issues.append(f"Coverage row references missing case ID(s) {missing_ids}: {row.strip()}")

    if covered_rows == 0:
        issues.append("PRD coverage audit exists but has no rows marked Covered/已覆盖 with case IDs.")
    return issues


def validate_plan(path: Path) -> list[str]:
    markdown = path.read_text(encoding="utf-8")
    issues: list[str] = []
    cases = find_cases(markdown)
    if not cases:
        issues.append("No executable test cases found. Add at least one '### CASE-ID Priority Title' section.")
        return issues

    case_ids: set[str] = set()
    for case in cases:
        match = CASE_ID_PATTERN.search(case.heading)
        if match:
            case_ids.add(match.group(0))

    issues.extend(validate_coverage(markdown, case_ids))

    for case in cases:
        case_body_lower = case.body.lower()
        for shortcut, reason in UI_FIDELITY_VIOLATIONS.items():
            if shortcut.lower() in case_body_lower:
                issues.append(
                    f"Line {case.line}: {case.heading} mentions UI fidelity violation '{shortcut}' ({reason})."
                )
        for section, label in REQUIRED_SECTIONS.items():
            content = section_content(case.body, section)
            if content is None:
                issues.append(f"Line {case.line}: {case.heading} is missing {label} section '{section}:'")
                continue
            has_content, has_placeholder = section_status(content)
            if not has_content:
                issues.append(f"Line {case.line}: {case.heading} has empty or placeholder-only {label}.")
            if has_placeholder:
                issues.append(f"Line {case.line}: {case.heading} still has placeholder text in {label}.")
    return issues


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate that an E2E test plan has executable cases and PRD coverage gates.")
    parser.add_argument("plan", type=Path, help="Path to the Markdown test plan.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    issues = validate_plan(args.plan)
    if not issues:
        print(f"OK: {args.plan} contains required executable case sections and PRD coverage gates.")
        return 0

    print(f"FAILED: {args.plan} has {len(issues)} issue(s).")
    for issue in issues:
        print(f"- {issue}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())