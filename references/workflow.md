# PRD E2E Test Agent Workflow

Use this reference when the task spans both case design and execution, or when the user asks for detailed E2E planning.

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

## Execution Readiness Check

Before promising real execution, confirm that the environment can:

- Open the target UI or local app.
- Log in with the needed accounts or create them safely.
- Perform the required UI actions.
- Read the independent verification source.
- Create, modify, or clean test data if the run needs it.
- Avoid production writes unless the user has explicitly approved them.

If any item is missing, stop at planning and return a dependency request instead of implying that execution is already possible.

## Coverage Design

Prioritize cases by risk:

- **P0**: revenue, critical workflow, permission boundary, persistence, external integration, source-of-truth consistency, or release-blocking risk.
- **P1**: important boundary cases, alternate state transitions, common failure paths, or role differences.
- **P2**: broad regression or low-risk coverage; include only when explicitly requested or when the suite has enough room.

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
- Preserve failed or blocked case data until the user decides whether to inspect or clean it.
- Clean passed-case data when safe, or document why it must be retained.
- Never use real sensitive personal, financial, credential, or production customer data as mock data.

## Review Gate

Before execution, create or update one dedicated test file that contains:

- Scope and assumptions.
- Dependency discovery result.
- Mock/data plan.
- Test subject matrix for accounts, roles, tenants, apps, and permissions.
- Full executable test cases.
- User review status and requested changes.

Ask the user to review this file. If the user changes cases, data, roles, or scope, update the same file and ask for approval again when changes materially affect execution.

After execution, append results to the same file:

- Overall result summary.
- Per-case status: passed first try, passed after fix, failed unrepaired, blocked, skipped.
- Evidence references.
- Bugs found and fix status.
- Remaining user decisions.
- Cleanup status.

Use a separate report only when the user requests one or the file would become too large to read.

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
