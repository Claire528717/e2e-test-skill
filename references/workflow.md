# E2E Test Skill Workflow

Use this reference when the task spans both case design and execution, or when the user asks for detailed E2E planning.

## Document Ownership

Keep responsibilities separated:

- `SKILL.md`: mandatory operating rules and reference routing only.
- `references/workflow.md`: workflow details, dependency discovery, review gates, execution readiness, and result handling.
- `references/coverage.md`: PRD coverage rules, status definitions, and requirement mapping quality bar.
- `references/templates.md`: output structure and user-facing packet format.
- `agents/reviewer.yaml`: second-review role, input boundary, checklist, and output contract.
- `scripts/validate_plan.py`: deterministic structural checks that must pass before user review or execution.

Do not duplicate long explanations across these files. When a rule can be enforced by a template field, reviewer checklist, or validator check, prefer that enforcement point over adding more prose to `SKILL.md`.

When `scripts/validate_plan.py` appears to report false positives, do not treat user-approved bypass as the normal path. First classify the failures by rule, fix the validator or template when the rule is too blunt, rerun the validator, and leave only genuine plan gaps or explicitly accepted residual risks for the user decision.
## Best Fit

Use this skill after frontend/backend development and integration are complete, and after smoke testing has passed.

Use it for acceptance testing, release regression, integration validation, and workflows such as create, edit, approve, subscribe, upload, download, authorize, publish, unpublish, and cross-system synchronization.

Do not use it as a substitute for unit tests, developer self-tests, early unfinished integration debugging, pure API automation with no UI path, performance testing, penetration testing, or production incident repair.

## Dependency Discovery Order

Search in this order before asking the user for dependency details:

1. User-provided PRD, UI artifacts, and explicit test goal.
2. Project docs: README, deployment docs, test docs, API docs.
3. Frontend structure: routes, pages, menus, buttons, forms, drawers, modals, status text.
4. Config files: `.env`, `.env.*`, config directories, proxies, local run scripts.
5. API and data layer: API clients, service wrappers, OpenAPI/Swagger, mocks, fixtures.
6. Existing tests: Playwright, Cypress, Jest, test data builders, test account docs.
7. Database clues: ORM config, migrations, schemas, SQL, table names.
8. External-system clues: SDKs, integration docs, environment variables, request wrappers, logs.
9. User confirmation for only the still-missing required items.

Summarize found and missing dependencies before case design or execution.

Before asking the user, decide whether each missing item can be reasonably handled by:

- reading project documentation or source code,
- using local setup scripts, fixtures, seeds, or mocks,
- creating isolated mock users, roles, tenants, permissions, apps, files, or product data,
- generating non-sensitive test files,
- downgrading the affected case to planning-only or blocked.

If a missing dependency cannot be honestly solved, explain it plainly. Do not work around it by bypassing UI actions, inventing credentials, writing database state that the UI should create, faking verification, or claiming that an unverified result passed.

## User Decision Gates

Use these gates in order:

1. **Case review gate**: ask the user to review test case quality, PRD coverage completeness, high-risk markers, assumptions, and unified data needs. This gate decides whether to execute E2E; it is not final release acceptance and does not prove the execution environment is ready.
2. **Blocking-bug gate**: during execution, ask whether to fix before continuing when a blocking bug prevents the case, blocks broad follow-on coverage, prevents required independent verification, or risks corrupting shared data.
3. **Result-and-fix gate**: after execution, summarize evidence, bugs, cleanup, residual risks, and deferred items so the user can decide whether to fix all bugs, defer some bugs, rerun cases, and review the fix result.

Before the case review gate, create a **PM Review Packet**. The packet is the user's primary reading surface; detailed cases are supporting material. It must include decision digest, automated quality gate status, second-review status, coverage summary, blockers, and only the user decisions needed now.

## Execution Readiness Check

After the user gives an explicit instruction to execute E2E, refresh the plan before running cases. Confirm that the environment can:

- Open the target UI or local app.
- Log in with the needed accounts or create them safely.
- Perform the required UI actions.
- Read the independent verification source.
- Create, modify, or clean test data if the run needs it.
- Avoid production writes unless the user has explicitly approved them.

If any item is missing, update the test plan's dependency, data, and verification sections, then stop with a dependency request instead of implying that execution is already possible.

Refresh each independent verification path at execution time because the user may now have provided a real URL, database, API, log, external-system access, or cleanup permission that was absent during case design. Replace vague entries such as query database/API with the concrete source, lookup key, field, and expected assertion when those details are available.

When the plan is large or is a PRD-backed full acceptance plan, the main agent must spawn a separate reviewer sub-agent through the available multi-agent tool before showing the plan to the user. Give the reviewer only the decision digest, coverage audit, mock/data plan, blocker list, and the 3-5 highest-risk cases, then revise the plan using the reviewer output. Return only the go/no-go judgment, the top issues, and the decisions the user must make now. If the current AI tool cannot spawn or access a reviewer sub-agent, mark Second Review as Blocked or Manual review required, state the reason, and do not imply that an independent review happened.

Reviewer output must be normalized before user review: fix must-fix issues, move blocked items into the decision digest, summarize non-blocking suggestions, and keep the visible reviewer result to verdict, must-fix issues, user decisions, rationale, and main-agent response.

Local test environments often do not come with ready-made users, roles, tenants, or permissions. For local execution, prefer creating or using isolated mock subjects when the project supports it. If the project cannot create or mock those subjects safely, mark the affected execution blocked and document exactly what is missing.

## Coverage Design

Prioritize cases by risk:

- **P0**: revenue, critical workflow, permission boundary, persistence, external integration, source-of-truth consistency, or release-blocking risk.
- **P1**: important boundary cases, alternate state transitions, common failure paths, or role differences.
- **P2**: broad regression or low-risk coverage; include only when explicitly requested or when the suite has enough room.

Coverage audit requirements:

- Include a PRD coverage audit or requirement coverage matrix in every PRD-backed full acceptance plan.
- Preserve PRD section numbers or stable checklist titles when available.
- Mark each row as exactly one of covered, partially covered, blocked, out-of-E2E/specialty, or out of release scope.
- Mark high-risk items in a separate risk column or high-risk register; do not mix risk or blocker labels into coverage status.
- Do not count a nearby happy path as coverage for rejection, disabled actions, role differences, cross-tenant visibility, audit logs, duplicate prevention, retry, timeout, or failure states.
- For every partially covered high-risk or P0/P1 row, add a case, add the missing branch to an existing case, or document the concrete missing dependency before review.
- Put SLA, load, availability, security, and similar non-UI requirements into specialty rows rather than pretending a UI click verifies them.

For each case, include:

- ID, priority, title, purpose.
- Actor/account and required permissions.
- Preconditions and generated or required data.
- UI operation path with exact visible labels.
- Backend/API/external-system verification path.
- Expected results.
- Evidence to capture.
- Cleanup.
- Blocking decision rule.

### Analytics and Statistics Coverage

For analytics, statistics, reporting, dashboard, ranking, or operations-monitoring requirements, do not treat page rendering plus one static API check as full E2E coverage. A complete plan must show how source business data is created or changed, how the statistic is calculated, and how the UI reflects it.

Include these checks when they apply:

- A data matrix covering time ranges, tenant/domain or scope, business category, status/state, item type, ranking values, empty data, and error data.
- Source business mutations such as create, submit, approve, publish, unpublish, subscribe, edit, or other domain actions, followed by V0 to V1 assertions on the affected metrics.
- Filter consistency from visible UI control to request parameter to backend result to UI update, such as range, scope, status, category, or custom date filters.
- Ranking and top-N behavior, including ties, fewer-than-N rows, empty results, and unsupported upstream metrics.
- Cross-scope isolation, such as platform versus domain, tenant, role, or ownership boundaries.
- Empty, loading, backend-error, invalid-filter, and return-navigation states.
- Clear separation between SQL/API seed data and real UI business actions. Seed data can prepare coverage dimensions, but it does not replace the visible UI path for the business behavior under test.
- Result summaries that distinguish full UI-path passes from API/DB-only verification, skipped upstream dependencies, blocked cases, and evidence-incomplete cases.
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
- Generate deterministic mock data only for missing non-sensitive inputs.
- Never invent credentials, production endpoints, or approval identities.
- When the user does not provide accounts, tenants, roles, permissions, apps, or files, infer a mock test subject matrix from the PRD for planning.
- Treat inferred accounts, tenants, roles, permissions, apps, or files as planning requirements until the environment can create or provide them.
- Do not start real execution from inferred subjects unless the environment supports creating or mocking those subjects.
- Record the mock scope: which users, roles, tenants, permissions, apps, product records, files, and external objects are mocked; why they are needed; how they will be created; which cases use them; and how they will be cleaned up or preserved.
- When the user requests any case addition, deletion, scope change, role change, file change, or verification change, update the unified mock/data plan, subject matrix, product data, files, external-system data, and cleanup rules in the same edit. Do not update only the case body.
- For local testing, treat mock users, roles, tenants, permissions, and app ownership as the default path unless real test subjects are already provided.
- Preserve failed or blocked case data until the user decides whether to inspect or clean it.
- Clean passed-case data when safe, or document why it must be retained.
- Never use real sensitive personal, financial, credential, or production customer data as mock data.

## Review Gate

Before execution, create or update one dedicated test file that contains:

- PM review packet with decision digest, automated quality gate, second review, blockers, and user decisions.
- Scope and assumptions.
- Dependency discovery result.
- Mock/data plan.
- Mock scope and assumptions, including anything inferred from the PRD.
- Test subject matrix for accounts, roles, tenants, apps, and permissions.
- Full executable test cases.
- User review status and requested changes.

Ask the user to review this file for test quality and completeness before execution. If the user changes cases, data, roles, verification, or scope, update the same file including the unified data plan, then ask for approval again when changes materially affect execution. When the file is large, lead with the decision digest and the top issues instead of asking the user to inspect every case before deciding.

After execution, append results to the same file:

- Overall result summary.
- Per-case status: passed first try, passed after fix, failed unrepaired, blocked, skipped.
- Evidence references.
- Bugs found and fix status.
- Remaining user decisions.
- Cleanup status.

Use a separate report only when the user requests one or the file would become too large to read.

## User-Facing Communication

Use plain language for non-technical users:

- Say "I can design the cases, but I cannot run these cases yet because..." instead of using only infrastructure jargon.
- Separate "what I found", "what I assumed or mocked", "what is missing", "what can still be tested", and "what decision I need from you".
- Do not hide blocked execution behind vague wording such as "environment issue" or "dependency problem".
- When mock data is used, state that it is test-only data and list the affected users, roles, tenants, permissions, files, and records.

## Terms

- **PRD**: the product requirements document and primary source for business rules and acceptance criteria.
- **Visual UI source**: HTML, prototype, screenshots, running product, or frontend code used to identify real operation paths.
- **UI operation path**: visible user actions through pages, buttons, forms, drawers, modals, uploads, and confirmations.
- **Independent verification**: database, API, log, queue, file, or external-system evidence that does not rely only on UI claims.
- **Blocking bug**: a defect that prevents the current case or a broad set of later cases from continuing, or makes later evidence unreliable.
- **Non-blocking bug**: a defect that should be recorded but does not prevent meaningful execution of other cases.
- **Mock data**: generated test data without sensitive real information.
- **Passed first try**: the case passed on its first execution.
- **Passed after fix**: the case failed first, a bug or environment issue was fixed, and rerun passed.
- **Failed unrepaired**: the case still fails and has not been fixed.
- **Deferred bug**: the user decides not to fix the bug in the current run.
- **Source of truth**: the authoritative system for a data type, such as an external API hub for API assets.
