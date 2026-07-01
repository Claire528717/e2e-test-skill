#!/usr/bin/env python3
"""Validate that an E2E test plan has executable case essentials and PRD coverage gates."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


REQUIRED_SECTION_GROUPS = [
    (("UI Fidelity Requirement", "UI 保真要求"), "UI fidelity requirement"),
    (("Actor", "参与者"), "actor"),
    (("UI Operation Path", "UI 操作路径", "操作路径"), "UI path"),
    (("Independent Verification", "独立验证"), "independent verification"),
    (("Evidence To Capture", "需采集的证据"), "evidence"),
    (("Cleanup", "清理"), "cleanup"),
]

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
    "force: true": "forced actions can bypass visible product state unless clearly justified by an already visible affordance",
    "network request instead of UI": "backend calls cannot replace the UI action under test",
    "直接调用 API": "API calls cannot replace the UI action under test",
    "写数据库": "database writes cannot replace the UI action under test",
    "隐藏 DOM": "hidden DOM manipulation bypasses visible user interaction",
}

LIST_PREFIX_PATTERN = re.compile(r"^\s*(?:[-*]\s+|\d+\.\s+)?")
PLACEHOLDER_TOKEN_PATTERN = re.compile(r"\{\{[^{}]+\}\}|\{[A-Za-z0-9_ /-]+\}")
CASE_ID_PATTERN = re.compile(r"\b[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+\b")
CASE_HEADING_PATTERN = re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+\b")
COVERAGE_SECTION_PATTERN = re.compile(
    r"^##\s+(?:PRD Coverage Audit|PRD 全量覆盖审计|PRD 覆盖审计|Requirement Coverage Matrix|需求覆盖矩阵)\s*$",
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
PM_REVIEW_PACKET_MARKERS = ("PM Review Packet:", "PM 审核包：")
DECISION_DIGEST_MARKERS = ("Decision Digest:", "决策摘要：")
AUTOMATED_GATE_MARKERS = ("Automated Quality Gate:", "自动质量门禁：")
SECOND_REVIEW_MARKERS = ("Second Review:", "二轮复核：")
EXECUTION_REFRESH_MARKERS = (
    "Execution-Time Verification Refresh:",
    "## Execution-Time Verification Refresh",
    "执行时独立核验刷新：",
    "## 执行时独立核验刷新",
    "执行前独立核验刷新：",
    "## 执行前独立核验刷新",
)
EXECUTION_RESULT_MARKERS = (
    "## E2E Test Execution Results",
    "## E2E 测试执行结果",
)
SECOND_REVIEW_NOT_RUN_VALUES = {
    "",
    "not run",
    "not started",
    "未执行",
    "未开始",
    "待补充",
    "todo",
    "tbd",
}
SECOND_REVIEW_PLACEHOLDER_VALUES = {
    "not required",
    "不需要",
    "n/a",
    "na",
}
NEGATION_TERMS = (
    "must not",
    "cannot",
    "do not",
    "should not",
    "not allowed",
    "no ",
    "禁止",
    "不能",
    "不允许",
    "不得",
    "不要",
    "不能通过",
)

UI_ONLY_VERIFICATION_PHRASES = (
    "only verify ui",
    "ui only",
    "visual only",
    "visible only",
    "screenshot only",
    "查看页面显示",
    "仅查看页面",
    "只看页面",
    "只验证页面",
    "仅截图",
    "截图即可",
)
INDEPENDENT_VERIFICATION_SIGNALS = (
    "database",
    "db",
    "sql",
    "api",
    "log",
    "queue",
    "file",
    "curl",
    "http",
    "request",
    "response",
    "status code",
    "admin",
    "external",
    "table",
    "record id",
    "correlation id",
    "数据库",
    "表",
    "接口",
    "日志",
    "队列",
    "文件",
    "请求",
    "响应",
    "状态码",
    "后台",
    "外部系统",
    "原型数据快照",
    "数据快照",
    "审计",
    "记录",
    "凭证",
)


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
        if not is_case_heading(heading):
            continue
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        line = text[: match.start()].count("\n") + 1
        cases.append(CaseBlock(heading=heading, body=text[start:end], line=line))
    return cases


def is_case_id(value: str) -> bool:
    if value.startswith("PRD-"):
        return False
    last_segment = value.rsplit("-", 1)[-1]
    return any(char.isdigit() for char in last_segment)


def is_case_heading(heading: str) -> bool:
    match = CASE_HEADING_PATTERN.match(heading)
    return bool(match and is_case_id(match.group(0)))


def section_heading_regex(section: str) -> str:
    return rf"{re.escape(section)}(?:\s*[\(\（][^\)\）]*[\)\）])?"


def section_content(body: str, section: str) -> str | None:
    heading = section_heading_regex(section)
    pattern = re.compile(
        rf"^\s*{heading}[:：]\s*$([\s\S]*?)(?=^\s*(?:[A-Z][A-Za-z /-]+|[\u4e00-\u9fffA-Za-z /-]+)[:：]\s*$|\Z)",
        re.M,
    )
    match = pattern.search(body)
    if not match:
        return None
    return match.group(1).strip()


def first_section_content(body: str, sections: tuple[str, ...]) -> tuple[str | None, str | None]:
    for section in sections:
        content = section_content(body, section)
        if content is not None:
            return section, content
    return None, None


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
        if text.endswith((":", "：")):
            continue
        if text.lower() in {"none", "n/a", "na", "todo", "tbd"} or text in {"无", "待补充"}:
            has_placeholder = True
            continue
        if text:
            has_content = True
    return has_content, has_placeholder


def extract_case_ids(text: str) -> set[str]:
    return {case_id for case_id in CASE_ID_PATTERN.findall(text) if is_case_id(case_id)}

def is_separator_row(row: str) -> bool:
    stripped = row.replace("|", "").strip()
    return bool(stripped) and set(stripped) <= {"-", ":"}


def has_any_marker(markdown: str, markers: tuple[str, ...]) -> bool:
    return any(marker in markdown for marker in markers)


def marker_block(markdown: str, markers: tuple[str, ...]) -> str | None:
    text = strip_fenced_blocks(markdown)
    marker_pattern = "|".join(re.escape(marker) for marker in markers)
    pattern = re.compile(rf"^(?:##\s*)?(?:{marker_pattern})\s*$([\s\S]*?)(?=^##\s+|^[^\n]+[:：]\s*$|\Z)", re.M)
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return None


def field_value(block: str, names: tuple[str, ...]) -> str | None:
    for name in names:
        pattern = re.compile(rf"^\s*[-*]?\s*{re.escape(name)}\s*[:：]\s*(.*)$", re.M | re.I)
        match = pattern.search(block)
        if match:
            return match.group(1).strip()
    return None


def validate_second_review(markdown: str) -> list[str]:
    issues: list[str] = []
    block = marker_block(markdown, SECOND_REVIEW_MARKERS)
    if block is None:
        return issues

    verdict = field_value(block, ("Reviewer verdict", "reviewer 结论", "reviewer 状态"))
    if verdict is None:
        issues.append("Second review exists but has no reviewer verdict/status value.")
    else:
        normalized = verdict.strip().lower()
        if normalized in SECOND_REVIEW_NOT_RUN_VALUES:
            issues.append("Second review exists but reviewer verdict/status is not run or empty.")
        if PLACEHOLDER_TOKEN_PATTERN.search(verdict):
            issues.append("Second review verdict/status still has placeholder text.")

    main_response = field_value(block, ("Main-agent response", "主 agent 处理"))
    if main_response is None:
        issues.append("Second review exists but has no main-agent response.")
    else:
        normalized_response = main_response.strip().lower()
        if normalized_response in SECOND_REVIEW_NOT_RUN_VALUES or PLACEHOLDER_TOKEN_PATTERN.search(main_response):
            issues.append("Second review main-agent response is empty or placeholder-only.")

    if verdict and verdict.strip().lower() in SECOND_REVIEW_PLACEHOLDER_VALUES and not main_response:
        issues.append("Second review marked not required must still explain why in the main-agent response.")
    return issues


def validate_execution_refresh(markdown: str) -> list[str]:
    if not has_any_marker(markdown, EXECUTION_RESULT_MARKERS):
        return []
    block = marker_block(markdown, EXECUTION_REFRESH_MARKERS)
    if block is None:
        return ["Execution results exist but execution-time verification refresh section is missing."]
    status = field_value(block, ("Current status", "当前状态"))
    if status is None:
        return ["Execution results exist but execution-time verification refresh has no current status."]
    if any(value in status.lower() for value in ("not started", "未开始")):
        return ["Execution results exist but execution-time verification refresh is still marked not started."]
    return []


def is_prohibition_line(line: str) -> bool:
    lowered = line.lower()
    return any(term in lowered for term in NEGATION_TERMS)


def is_negated_shortcut(line: str, shortcut: str) -> bool:
    lowered = line.lower()
    needle = shortcut.lower()
    start = 0
    while True:
        index = lowered.find(needle, start)
        if index == -1:
            return False
        context = lowered[max(0, index - 24):index]
        if any(term in context for term in ("not ", "no ", "without ", "禁止", "不能", "不允许", "不得", "不要", "不直接", "不 ")):
            return True
        start = index + len(needle)


def validate_ui_fidelity_violations(case: CaseBlock) -> list[str]:
    issues: list[str] = []
    for offset, line in enumerate(case.body.splitlines(), start=case.line + 1):
        lowered = line.lower()
        if is_prohibition_line(line):
            continue
        for shortcut, reason in UI_FIDELITY_VIOLATIONS.items():
            if shortcut.lower() in lowered:
                if is_negated_shortcut(line, shortcut):
                    continue
                issues.append(
                    f"Line {offset}: {case.heading} mentions UI fidelity violation '{shortcut}' ({reason})."
                )
    return issues


def validate_independent_verification(case: CaseBlock) -> list[str]:
    _, content = first_section_content(case.body, ("Independent Verification", "独立验证"))
    if content is None:
        return []
    lowered = content.lower()
    issues: list[str] = []
    if any(phrase in lowered for phrase in UI_ONLY_VERIFICATION_PHRASES):
        issues.append(f"Line {case.line}: {case.heading} independent verification appears UI-only.")
    if not any(signal in lowered for signal in INDEPENDENT_VERIFICATION_SIGNALS):
        issues.append(
            f"Line {case.line}: {case.heading} independent verification lacks a database/API/log/file/admin/external-system source."
        )
    return issues


def validate_coverage(markdown: str, case_ids: set[str]) -> list[str]:
    issues: list[str] = []
    lowered = markdown.lower()
    has_prd_signal = any(term.lower() in lowered for term in PRD_SIGNAL_TERMS)
    has_coverage_section = bool(COVERAGE_SECTION_PATTERN.search(markdown))

    if has_prd_signal and not has_coverage_section:
        issues.append(
            "Missing PRD coverage audit. Add '## PRD Coverage Audit', '## PRD 覆盖审计', "
            "'## Requirement Coverage Matrix', or '## 需求覆盖矩阵' with requirement-to-case mapping."
        )
        return issues

    if not has_coverage_section:
        return issues

    if not has_any_marker(markdown, PM_REVIEW_PACKET_MARKERS):
        issues.append("Missing PM review packet. Add 'PM Review Packet:' or 'PM 审核包：' before asking for review.")
    if not has_any_marker(markdown, DECISION_DIGEST_MARKERS):
        issues.append("Missing decision digest. Add 'Decision Digest:' or '决策摘要：' before asking for review.")
    if not has_any_marker(markdown, AUTOMATED_GATE_MARKERS):
        issues.append("Missing automated quality gate. Add 'Automated Quality Gate:' or '自动质量门禁：' before asking for review.")
    if not has_any_marker(markdown, SECOND_REVIEW_MARKERS):
        issues.append("Missing second review section. Add 'Second Review:' or '二轮复核：' before asking for review.")

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
        ids = extract_case_ids(row)
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
    markdown = path.read_text(encoding="utf-8-sig")
    issues: list[str] = []
    cases = find_cases(markdown)
    if not cases:
        issues.append("No executable test cases found. Add at least one '### CASE-ID Priority Title' section.")
        return issues

    case_ids: set[str] = set()
    for case in cases:
        case_ids.update(extract_case_ids(case.heading))

    issues.extend(validate_coverage(markdown, case_ids))
    issues.extend(validate_second_review(markdown))
    issues.extend(validate_execution_refresh(markdown))

    for case in cases:
        issues.extend(validate_ui_fidelity_violations(case))
        for sections, label in REQUIRED_SECTION_GROUPS:
            matched_section, content = first_section_content(case.body, sections)
            if content is None:
                display = "' or '".join(sections)
                issues.append(f"Line {case.line}: {case.heading} is missing {label} section '{display}:'")
                continue
            has_content, has_placeholder = section_status(content)
            if not has_content:
                issues.append(f"Line {case.line}: {case.heading} has empty or placeholder-only {label}.")
            if has_placeholder:
                issues.append(f"Line {case.line}: {case.heading} still has placeholder text in {label}.")
        issues.extend(validate_independent_verification(case))
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
