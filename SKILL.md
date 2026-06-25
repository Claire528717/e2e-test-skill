---
name: prd-e2e-test-agent
description: "Design PRD-driven end-to-end acceptance test plans from product requirements and real UI sources. Use when Codex needs to turn a PRD, screenshots, prototype, HTML, frontend code, or other visual UI source into executable E2E test cases with realistic UI paths, mock/test data plans, review gates, and independent database/API/external-system verification. Also use for Chinese-language requests such as \u9a8c\u6536\u6d4b\u8bd5, \u7aef\u5230\u7aef\u6d4b\u8bd5, E2E \u7528\u4f8b, \u6d4b\u8bd5\u8ba1\u5212, or \u6839\u636e\u9875\u9762\u751f\u6210\u6d4b\u8bd5\u7528\u4f8b after development and integration are complete. Execute cases, collect evidence, handle bugs, and produce run summaries only after the user approves the plan and explicitly asks to run it."
---

# PRD E2E Test Agent

## Default Behavior

Default to **case design only**. Create a dedicated E2E test plan file and stop for user review.

Start execution only after the user confirms or modifies the test plan and then gives an explicit instruction to run it.

If the user's request does not include accounts, roles, tenants, or permissions, infer a mock test subject matrix from the PRD for planning. Treat those mock subjects as data requirements before execution; do not pretend they already exist unless the environment can create or provide them.

Run execution only when the current environment has the required URL, accounts or creatable test subjects, data permissions, and verification access.

## Core Rule

Keep UI operation and verification separate:

- **UI operation path**: act like a real user through visible pages, navigation, forms, drawers, uploads, confirmations, and states.
- **Independent verification**: after the UI action, verify persistence or integration through a database, API, log, queue, file, admin system, or external system.

Do not replace a tested UI action with direct API calls, database writes, hidden DOM manipulation, synthetic DOM events, storage/session seeding, component internals, or automation-only shortcuts. Every tested action must start from the same visible affordance a real user would use; if no visible path exists, mark the case blocked or failed.

## Required Inputs

Require:

- PRD or equivalent product requirements.
- Visual UI source: screenshots, prototype, HTML, running product, or frontend code that exposes real operation paths.
- If the user is a non-technical product manager, translate their goal into a short test brief first: target feature, PRD source, UI source, roles, environment, allowed test data actions, and what must be independently verified.

For execution, also require or discover:

- Product URL or local run instructions.
- Test accounts, roles, tenants, permissions, or permission to create them.
- Database/API/log/external-system access for independent verification.
- Permission boundaries for creating, editing, deleting, and cleaning test data.

For planning, infer missing accounts, roles, tenants, permissions, apps, and test files as mock data when the PRD provides enough clues. Ask only for missing items that block planning or real execution.

Prefer to keep one run focused on one feature slice or one integration boundary.

## Workflow

1. **Discover**
   - Read the PRD and UI source enough to identify actors, objects, states, rules, operation paths, and integrations.
   - Search the workspace for dependency clues before asking the user: docs, routes, API clients, `.env*`, mocks, fixtures, tests, schema/migrations, OpenAPI/Swagger, SDKs, and local run scripts.
   - Summarize what was found and what is still missing.
   - If execution is requested, verify that the environment can actually perform UI interaction and independent verification before promising a run.

2. **Analyze**
   - Extract business capabilities, state transitions, permissions, source-of-truth systems, and acceptance criteria.
   - Compare PRD behavior with UI affordances.
   - Stop and ask the user when contradictions, impossible states, missing expected results, or unclear data ownership affect the suite.

3. **Design**
   - Group cases by business capability or integration boundary.
   - Prefer a focused P0/P1 suite over exhaustive low-value coverage.
   - Include actor, preconditions, data setup, exact UI path, independent verification, expected result, evidence, cleanup, and blocking rule for each executable case.
   - Write the suite to one dedicated Markdown file using `references/templates.md`.
   - Use `references/examples.md` as the quality bar when cases risk becoming vague or when external-system verification is involved.
   - Include the inferred or provided test subject matrix and data/mock plan before execution.
   - Ask the user to review or modify the file before executing.

4. **Execute Only After Approval**
   - Follow the approved UI paths exactly.
   - Use APIs/databases only for declared setup or independent verification after the UI action.
   - Capture evidence after major steps.
   - Append results to the same test plan file unless the user requests a separate report.
   - Apply the stop rules in `references/execution-guardrails.md`.

5. **Summarize**
   - Update the same file with pass/fail/blocked/skipped counts, evidence references, defects, fixes, deferred bugs, cleanup status, residual risks, and remaining user decisions.

## Reference Routing

- Read `references/templates.md` before generating a test plan, test case, review request, dependency request, blocking-bug question, or run summary.
- Read `references/examples.md` when the requested feature involves external-system verification, multi-role behavior, or when generated cases might be too vague.
- Read `references/workflow.md` when a task spans both design and execution, or when dependency discovery, test data planning, review gates, or result categories need more detail.
- Read `references/execution-guardrails.md` before executing approved cases or deciding whether to continue after a bug.

## Default File Layout

- Write the suite to `e2e-test-plans/` by default when the user does not specify a path.
- Use `e2e-test-plan-{feature}-{run_id}.md` as the plan filename.
- Put screenshots and other evidence under `e2e-test-evidence/{run_id}/`.
- Keep the plan file and evidence paths consistent throughout the run.

## Scripts

Use bundled scripts when deterministic file layout or validation helps:

- Run `python scripts/create_run_id.py "{feature}"` to generate a standard run ID.
- Run `python scripts/scaffold_plan.py "{feature}" --run-id "{run_id}"` to create the default plan file and evidence directory.
- Run `python scripts/validate_plan.py "{plan_path}"` before asking for review or before execution; fix missing actor, UI path, independent verification, evidence, or cleanup sections before proceeding.

## Output Modes

Choose the narrowest mode that matches the request:

- **Case design only**: create the dedicated test plan file and stop for review.
- **Execution plan**: create runnable cases, data needs, credentials checklist, and risk gates.
- **Run execution**: execute approved cases, collect evidence, stop for blocking bugs, and append results.
- **Post-run report**: summarize an existing run log, preferably by updating the same file.

Use Markdown by default. Use JSON or YAML only when useful for machine execution.
