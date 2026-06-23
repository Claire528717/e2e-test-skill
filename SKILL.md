---
name: prd-e2e-test-agent
description: PRD-driven end-to-end QA design and execution guidance. Use when Codex must read product requirements, UI pages or frontend code, database/API dependencies, then generate executable E2E test cases, prepare or request test data, guide an agent through real human UI paths, verify results through databases and external APIs, stop for user decisions on blocking bugs, and produce a test summary.
---

# PRD E2E Test Agent

## Operating Principle

Treat testing as two separate phases that must not be mixed:

- **Human UI path**: operate the product like a real user through pages, drawers, buttons, forms, uploads, confirmations, and visible states. Do not replace this with direct API calls unless the case explicitly says the setup or assertion is backend-only.
- **Independent verification**: after the UI action, verify the result through databases, logs, external APIs, queues, files, or admin systems. The verification must not rely only on what the page claims.

When a user asks for test cases, E2E execution, PRD-based QA, or a test summary from product docs and UI, use this skill.

## Best Fit

Use this skill after frontend/backend development and integration are complete, and after smoke testing has passed. Its purpose is to help non-coding users deliver high-quality system-level E2E validation by combining real UI operation with database and external-system verification.

Use it for acceptance testing, release regression, integration validation, and end-to-end verification of workflows such as create, edit, approve, subscribe, upload, download, authorize, publish, unpublish, and cross-system synchronization.

Do not use it as a substitute for unit tests, developer self-tests, early unfinished integration debugging, pure API automation with no UI path, performance testing, penetration testing, or production incident repair.

## Required Inputs

Require the user to provide:

- A PRD or equivalent product requirements document.
- A visual UI source: HTML, an interactive prototype, screenshots with enough detail, or frontend code that exposes the real pages and operation paths.

If execution is requested, also discover or request:

- Product URL or local run instructions.
- Test accounts or permission to create/infer test subjects.
- Database/API/external-system access needed for independent verification.
- Permission boundaries for creating, editing, deleting, or cleaning test data.

## Workflow

1. **Collect inputs**
   - Read the PRD completely enough to identify roles, objects, states, external integrations, critical rules, and acceptance criteria.
   - Inspect the referenced UI or frontend code to learn actual navigation, page names, drawers, buttons, fields, disabled states, and labels.
   - Actively look for existing dependency information in the workspace before asking: database config, API clients, environment files, test fixtures, mocks, OpenAPI files, README, CI scripts, and local test docs.
   - If database/API credentials, test accounts, external system URLs, or unsafe live-system permissions are missing, ask the user for only the missing items.

2. **Analyze requirements**
   - Extract business objects, actors, permissions, state transitions, operation paths, source-of-truth systems, and acceptance criteria.
   - Compare PRD behavior with UI affordances. If there are logical contradictions, missing expected results, impossible states, or unclear ownership of data, ask the user before designing final cases.

3. **Design coverage**
   - Group cases by business capability or integration boundary.
   - Prefer a small P0/P1 set over exhaustive low-value cases.
   - For each case, include realistic actor, preconditions, data setup, UI path, backend/API checks, expected results, cleanup, and bug-blocking criteria.
   - Mark cases as P0 for revenue/critical workflow/data consistency/integration source-of-truth risk; P1 for important boundaries; P2 only when explicitly requested.
   - Write the proposed suite to one dedicated test plan file using `references/templates.md`.
   - Use `references/examples.md` as the quality bar for operation-path detail, evidence detail, and cross-system verification detail.
   - Include the data and mock plan in the same file before execution, including inferred accounts, roles, tenants, apps, files, and external-system objects.
   - Send the file to the user for review before execution. Do not start execution until the user approves or gives edits.

4. **Prepare data**
   - Reuse existing fixtures where available.
   - Generate deterministic mock data only for missing non-sensitive inputs, using unique names with timestamps or run IDs.
   - Never invent credentials, production endpoints, or approval identities. Ask for them.
   - If real test accounts, tenants, roles, or apps are unavailable, infer a test subject matrix from the PRD for planning. For real execution, treat inferred subjects as data requirements; do not pretend they already exist unless the environment allows creating or mocking them.
   - Keep created data traceable and provide cleanup instructions or cleanup steps.

5. **Execute strictly**
   - Execute only after the user has reviewed the dedicated test plan file and approved the current version.
   - Follow the UI path exactly as written. Do not skip pages, jump directly to APIs, mutate the database to simulate user actions, or declare success from a partial page state.
   - Record evidence after each major step: current page/drawer, visible state, submitted values, request IDs, DB record IDs, external system IDs, screenshots when available, and relevant response snippets.
   - Use backend/API access only for setup explicitly declared as setup, or for independent verification after the UI operation.
   - Append execution results to the same test plan file instead of creating a disconnected report, unless the user asks for a separate report.

6. **Review test discipline**
   - Before summarizing, check whether every executed case followed the UI path, captured UI evidence, performed independent verification, and recorded cleanup status.
   - Mark any case with missing critical evidence as inconclusive rather than passed.

7. **Handle bugs**
   - By default, record bugs but do not fix them.
   - If a bug blocks the next test step or would make many later cases unreliable, stop and ask the user before fixing, bypassing, or continuing.
   - In the question, include: observed behavior, expected behavior, impact, whether it blocks only this case or the suite, and the recommended choice.
   - If the user grants permission to automatically fix future blocking bugs in the current run, follow that preference and record each fix.
   - Do not silently work around blocking bugs.
   - Non-blocking bugs may be recorded and testing may continue, unless the user requested stop-on-any-bug.

8. **Summarize**
   - Update the same test plan file with scope, environment, data used, pass/fail/blocked counts, defects, evidence references, residual risks, deferred bugs, and recommended next actions.
   - Separate "bugs found" from "fixes recommended"; the user decides whether to repair all remaining issues.

## Review Gate

Before execution, create or update one dedicated test file that contains:

- Scope and assumptions
- Dependency discovery result
- Mock/data plan
- Test subject matrix for accounts, roles, tenants, apps, and permissions
- Full executable test cases
- User review status and requested changes

Ask the user to review this file. If the user changes cases, data, roles, or scope, update the same file and ask for approval again when the changes materially affect execution.

After execution, append results to the same file:

- Overall result summary
- Per-case status: passed first try, passed after fix, failed unrepaired, blocked, skipped
- Evidence references
- Bugs found and fix status
- Remaining user decisions
- Cleanup status

Use a separate report only when the user requests one or the file would become too large to read.

## Required Case Format

Use the detailed templates in `references/templates.md` when generating deliverables.
Use the examples in `references/examples.md` when the user needs concrete output quality, when the requested feature has external-system verification, or when generated cases risk becoming too vague.

At minimum, each executable test case must contain:

- ID, priority, title, purpose
- Actor/account and required permissions
- Preconditions and generated or required data
- UI operation path with exact visible labels
- Backend/API verification path
- Expected results
- Evidence to capture
- Cleanup
- Blocking decision rule

## Test Data Rules

Use a run ID for every suite, such as `E2E-{feature}-{yyyyMMddHHmm}-{short_random}`.

Classify data as:

- **Test subjects**: accounts, roles, tenants, apps, ownership, permission scopes.
- **Product data**: records created inside the tested product.
- **External data**: objects created in integrated systems.
- **Files**: uploads, OpenAPI specs, resource packages, images, or generated documents.

Rules:

- Prefix generated data with the run ID or an `E2E-` marker.
- Keep names unique and traceable.
- Preserve failed or blocked case data until the user decides whether to inspect or clean it.
- Clean passed-case data when safe, or document why it must be retained.
- Never use real sensitive personal, financial, credential, or production customer data as mock data.

## Dependency Discovery Order

Before asking the user for dependency details, search in this order:

1. User-provided PRD, UI artifacts, and explicit test goal.
2. Project docs: README, deployment docs, test docs, API docs.
3. Frontend structure: routes, pages, menus, buttons, forms, drawers, modals, status text.
4. Config files: `.env`, `.env.*`, config directories, proxies, local run scripts.
5. API and data layer: API clients, service wrappers, OpenAPI/Swagger, mocks, fixtures.
6. Existing tests: Playwright, Cypress, Jest, test data builders, test account docs.
7. Database clues: ORM config, migrations, schemas, SQL, table names.
8. External-system clues: SDKs, integration docs, environment variables, request wrappers, logs.
9. User confirmation for only the still-missing required items.

If found, summarize what you found and what is still missing.

## Guardrails Against Shortcuts

- Do not call backend APIs to create the tested object when the test case is about creating it through the UI.
- Do not use database writes to force state transitions that the UI is supposed to perform.
- Do not infer external integration success from local records alone; query the external system.
- Do not infer data consistency from external system records alone; query the product database too.
- Do not continue after a blocking bug without user approval, unless the user has already granted permission to auto-fix blocking bugs in this run.
- Do not declare a case passed without both UI evidence and independent verification when the case covers persistence or integration behavior.
- Do not replace role-switching tests with a single high-privilege account.
- Do not treat a success toast as sufficient evidence of creation, update, deletion, approval, subscription, or external synchronization.

## Terms

- **PRD**: the product requirements document and primary source for business rules and acceptance criteria.
- **Visual UI source**: HTML, prototype, screenshots, or frontend code used to identify real user operation paths.
- **UI operation path**: visible user actions through pages, buttons, forms, drawers, modals, uploads, and confirmations.
- **Independent verification**: database, API, log, queue, file, or external-system evidence that does not rely only on UI claims.
- **Blocking bug**: a defect that prevents the current case or a broad set of later cases from continuing, or makes later evidence unreliable.
- **Non-blocking bug**: a defect that should be recorded but does not prevent meaningful execution of other cases.
- **Mock data**: generated test data without sensitive real information.
- **Test discipline**: the rule set requiring real UI operation, independent verification, no shortcuts, complete evidence, and traceable cleanup.
- **Passed first try**: the case passed on its first execution.
- **Passed after fix**: the case failed first, a bug or environment issue was fixed, and rerun passed.
- **Failed unrepaired**: the case still fails and has not been fixed.
- **Deferred bug**: the user decides not to fix the bug in the current run.
- **Source of truth**: the authoritative system for a data type, such as apihub for API assets.

## Output Modes

Choose the mode that matches the user request:

- **Case design only**: create the dedicated test plan file and stop for user review; do not execute.
- **Execution plan**: produce ordered runnable cases, data needs, credentials checklist, and risk gates in the test plan file.
- **Run execution**: execute approved cases, collect evidence, stop for blocking bugs, and append results to the same file.
- **Post-run report**: summarize results and defects from an existing run log, preferably updating the same file.

If the user does not specify a format, use Markdown with tables for overview and structured sections for full cases. Include JSON or YAML blocks only when useful for machine execution.



