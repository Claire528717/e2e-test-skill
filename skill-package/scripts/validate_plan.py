#!/usr/bin/env python3
"""Validate that an E2E test plan has executable case essentials."""

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


def validate_plan(path: Path) -> list[str]:
    markdown = path.read_text(encoding="utf-8")
    issues: list[str] = []
    cases = find_cases(markdown)
    if not cases:
        issues.append("No executable test cases found. Add at least one '### CASE-ID Priority Title' section.")
        return issues

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
    parser = argparse.ArgumentParser(description="Validate an E2E test plan scaffold.")
    parser.add_argument("plan", type=Path, help="Path to the Markdown test plan.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    issues = validate_plan(args.plan)
    if not issues:
        print(f"OK: {args.plan} contains required executable case sections.")
        return 0

    print(f"FAILED: {args.plan} has {len(issues)} issue(s).")
    for issue in issues:
        print(f"- {issue}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
