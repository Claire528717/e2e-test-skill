---
name: e2e-test-skill
description: "Design PRD-driven end-to-end acceptance test plans from product requirements and real UI sources. Use when Codex needs to turn a PRD, screenshots, prototype, HTML, frontend code, or other visual UI source into executable E2E test cases with realistic UI paths, mock/test data plans, review gates, and independent database/API/external-system verification. Also use for Chinese-language requests such as 验收测试, 端到端测试, E2E 用例, 测试计划, or 根据页面生成测试用例 after development and integration are complete. Execute cases, collect evidence, handle bugs, and produce run summaries only after the user approves the plan and explicitly asks to run it."
---

# E2E Test Skill

## Operating Rules

Default to **case design only**. Create one dedicated E2E test plan file, then stop for user review. Start execution only after the user confirms or modifies the plan and explicitly asks to run E2E.

Match the user's language for all visible prose in generated plans, summaries, and review requests. Use Chinese for Chinese prompts and English for English prompts. Keep file names, paths, case IDs, code tokens, and exact UI labels unchanged.

Use three user decision gates:

1. **Case review gate**: the user reviews case quality, PRD coverage completeness, high-risk markers, assumptions, and data needs to decide whether to execute E2E. Do not present this as final release acceptance or proof that the execution environment is ready.
2. **Blocking-bug gate**: during execution, stop when a blocking bug prevents the current case, blocks broad follow-on coverage, or makes required verification unreliable.
3. **Result-and-fix gate**: after execution, show results, bugs, evidence, cleanup status, and residual risks so the user can decide whether to fix, defer, rerun, or review post-fix results.

Before the case review gate, produce a **PM Review Packet** at the top of the plan. It must include a concise decision digest, validator status, second-review status when required, coverage gaps, high-risk items, blockers, and the 1-3 user decisions needed now. Treat detailed cases as supporting material, not required first-pass reading.

For PRD-backed full acceptance plans or plans with more than 10 executable cases:

- Run `scripts/validate_plan.py` before asking for review and fix structural failures first.
- Spawn a separate reviewer sub-agent before exposing the plan to the user. Give it only the PM review packet, decision digest, coverage audit, mock/data plan, blocker list, and 3-5 highest-risk cases.
- Resolve reviewer must-fix issues, move blocked findings into user decisions, and summarize only the verdict, must-fix issues, user decisions, rationale, and main-agent response.

For PRD-backed requests, default to **complete PRD coverage**, not a representative happy-path suite. Every explicit must-have item, acceptance criterion, role/permission rule, business rule, state transition, exception/empty state, data consistency rule, and declared non-functional/SLA item must be mapped as covered, partially covered, blocked, out-of-E2E/specialty, or out of release scope. If the user asks for a narrow slice, label it as a focused slice and summarize what remains uncovered.

Mark high-risk items separately from coverage status. Risk describes business impact and execution priority; it is not a coverage state.

Keep UI operation and verification separate:

- **UI operation path**: act like a real user through visible pages, navigation, forms, drawers, uploads, confirmations, and states.
- **Independent verification**: after the UI action, verify persistence or integration through a database, API, log, queue, file, admin system, or external system.

Do not replace tested UI actions with direct API calls, database writes, hidden DOM manipulation, synthetic DOM events, storage/session seeding, component internals, or automation-only shortcuts. If no visible user path exists, mark the case blocked or failed.

This is not a fully automatic testing tool. Discover, create, or mock missing dependencies when the project supports doing so safely. If a critical dependency cannot be solved honestly, explain the gap, impact, and next user decision in plain language. Never fabricate evidence, credentials, permissions, environments, or verification sources.

## Required Inputs

Require:

- PRD or equivalent product requirements.
- Visual UI source: screenshots, prototype, HTML, running product, or frontend code that exposes real operation paths.
- For non-technical product managers, first translate the goal into a short test brief: target feature, PRD source, UI source, roles, environment, allowed test data actions, and required independent verification.

For execution, also require or discover:

- Product URL or local run instructions.
- Test accounts, roles, tenants, permissions, or permission to create/mock them.
- Database/API/log/external-system access for independent verification.
- Permission boundaries for creating, editing, deleting, and cleaning test data.

During planning, infer missing non-sensitive accounts, roles, tenants, permissions, apps, files, and product records as mock data when the PRD provides enough clues. Treat inferred data as execution requirements until the environment can create or provide it. When the user modifies cases, roles, scope, files, or verification expectations, update the unified mock/data plan in the same file.

After the user explicitly asks to execute E2E, refresh URL, account matrix, verification access, and cleanup permissions before running. Update the plan first if any verification path is vague, stale, unavailable, or no longer independent.

## Workflow

1. **Discover**
   - Read the PRD and UI source enough to identify actors, objects, states, rules, operation paths, and integrations.
   - Search the workspace for dependency clues before asking the user. Use `references/workflow.md` for the full discovery order.
   - Summarize what was found, what is missing, and what can be mocked or created safely.

2. **Analyze**
   - Extract capabilities, state transitions, permissions, source-of-truth systems, and acceptance criteria.
   - Compare PRD behavior with UI affordances.
   - Build the PRD coverage audit and stop for clarification when contradictions, impossible states, missing expected results, or unclear data ownership affect the suite.

3. **Design**
   - Group cases by business capability or integration boundary.
   - Include actor, preconditions, data setup, exact UI path, independent verification, expected result, evidence, cleanup, and blocking rule for each executable case.
   - Write the suite to one dedicated Markdown file using the template for the user's language.
   - Put the PM Review Packet before detailed coverage and cases.
   - Ask the user to review or modify the file before execution.

4. **Execute Only After Approval**
   - Refresh execution readiness and independent verification sources.
   - Follow the approved UI paths exactly.
   - Use APIs/databases only for declared setup or independent verification after the UI action.
   - Capture evidence, including active UI screenshots for passed UI cases, append results to the same plan file, and apply `references/execution-guardrails.md`.
   - After execution, run `scripts/validate_evidence.py "{plan_path}"` when evidence files are available; downgrade passed cases to inconclusive when required UI or independent evidence is missing.

5. **Summarize**
   - Update the same file with pass/fail/blocked/skipped counts, evidence references, defects, fixes, deferred bugs, cleanup status, residual risks, and remaining user decisions.

## Reference Routing

- Read `references/templates.md` for English output or `dev/zh-CN/references/templates.zh-CN.md` for Chinese output before generating a test plan, test case, review request, dependency request, blocking-bug question, or run summary.
- Read `references/coverage.md` for English output or `dev/zh-CN/references/coverage.zh-CN.md` for Chinese output before generating or reviewing any PRD-backed full acceptance plan, and whenever the user asks whether coverage is complete.
- Read `references/workflow.md` for English output or `dev/zh-CN/references/workflow.zh-CN.md` for Chinese output when dependency discovery, test data planning, review gates, execution readiness, or result categories need more detail.
- Read `references/examples.md` when external-system verification, multi-role behavior, or vague case quality is a risk.
- Read `references/execution-guardrails.md` before executing approved cases or deciding whether to continue after a bug.

## File Layout And Scripts

- Write plans to `e2e-test-plans/` by default.
- Use `e2e-test-plan-{feature}-{run_id}.md` for plan files.
- Put evidence under `e2e-test-evidence/{run_id}/`.
- Run `python3 scripts/create_run_id.py "{feature}"` to generate a run ID when needed.
- Run `python3 scripts/scaffold_plan.py "{feature}" --run-id "{run_id}"` to scaffold a plan and evidence directory when useful.
- Run `python3 scripts/validate_plan.py "{plan_path}"` before review or execution; fix missing actor, UI path, independent verification, evidence, cleanup, PRD coverage audit, decision digest, automated gate, or second-review sections before proceeding.
- Run `python3 scripts/validate_evidence.py "{plan_path}"` after execution to confirm passed UI cases have screenshot evidence and independent evidence under the declared evidence directory.

## Output Modes

Choose the narrowest mode that matches the request:

- **Case design only**: create the dedicated test plan file and stop for review.
- **Execution plan**: create runnable cases, data needs, credentials checklist, and risk gates.
- **Run execution**: execute approved cases, collect evidence, stop for blocking bugs, and append results.
- **Post-run report**: summarize an existing run log, preferably by updating the same file.

Use Markdown by default. Use JSON or YAML only when useful for machine execution.

