# Execution Guardrails

Read this reference before executing approved E2E cases or deciding whether to continue after a bug.

## Shortcut Rules

- Do not call backend APIs to create the tested object when the case is about creating it through the UI.
- Do not use database writes to force state transitions that the UI is supposed to perform.
- Do not infer external integration success from local product records alone; query the external system.
- Do not infer product data consistency from external-system records alone; query the product database too.
- Do not declare a case passed without both UI evidence and independent verification when the case covers persistence or integration behavior.
- Do not replace role-switching tests with a single high-privilege account.
- Do not treat a success toast as sufficient evidence of creation, update, deletion, approval, subscription, or external synchronization.

## Evidence Rules

Record evidence after each major step:

- Current page, drawer, modal, tab, or visible state.
- Submitted values.
- Screenshots when available.
- Request, correlation, product record, database, and external-system IDs.
- Relevant database/API/log response excerpts.
- Cleanup status or reason cleanup was deferred.

Mark any case with missing critical evidence as inconclusive rather than passed.

## Bug Handling

By default, record bugs but do not fix them.

Stop and ask the user before fixing, bypassing, or continuing when a bug:

- Blocks the current test step.
- Blocks the current case.
- Makes many later cases unreliable.
- Prevents required independent verification.
- Risks corrupting shared test data or external systems.

In the question, include:

- Observed behavior.
- Expected behavior.
- Evidence.
- Impact.
- Whether it blocks only this case or the suite.
- Recommended decision.

If the user grants permission to automatically fix future blocking bugs in the current run, follow that preference and record each fix.

Non-blocking bugs may be recorded while testing continues, unless the user requested stop-on-any-bug.

Do not silently work around blocking bugs.
