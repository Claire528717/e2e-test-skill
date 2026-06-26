# Execution Guardrails

Read this reference before executing approved E2E cases or deciding whether to continue after a bug.

## Shortcut Rules

- Preserve UI fidelity: every tested user action must start from the same visible affordance a real user would use, such as a button, link, menu item, form field, tab, drawer, dialog, upload/drop area, drag handle, checkbox, radio, switch, pagination control, or confirmation control.
- Automation APIs may drive the browser, but they must not change the product state through a path unavailable to a real user. Do not mutate DOM state, invoke component methods, dispatch synthetic product events, call hidden controls directly, seed local storage/session state, or call backend APIs to replace the UI action under test.
- Low-level framework helpers are allowed only when they implement a user-triggered browser capability that has already been reached through a visible UI action. The test evidence must show the visible affordance before interaction and the visible result after interaction.
- If the product exposes no visible path for a required action, mark the case blocked or failed. Do not recover by operating hidden DOM, internal selectors, component internals, local storage, network calls, or database writes.
- Do not call backend APIs to create the tested object when the case is about creating it through the UI.
- Do not use database writes to force state transitions that the UI is supposed to perform.
- Do not infer external integration success from local product records alone; query the external system.
- Do not infer product data consistency from external-system records alone; query the product database too.
- Do not declare a case passed without both UI evidence and independent verification when the case covers persistence or integration behavior.
- Do not replace role-switching tests with a single high-privilege account.
- Do not treat a success toast as sufficient evidence of creation, update, deletion, approval, subscription, or external synchronization.

## Production Safety

- Default to local, test, or staging environments.
- If the target URL or app context looks like production and the user has not explicitly approved writes, stop and ask.
- On production, only perform read-only validation unless the user has explicitly authorized the exact scope of writes.
- Do not create, update, delete, or clean shared production data unless the user has confirmed the environment and impact.
- Do not use real customer, financial, credential, or private data as mock data.

## Evidence Rules

Record evidence after each major step:

- Current page, drawer, modal, tab, or visible state.
- Submitted values.
- Screenshots when available.
- Request, correlation, product record, database, and external-system IDs.
- Relevant database/API/log response excerpts.
- Cleanup status or reason cleanup was deferred.

Mark any case with missing critical evidence as inconclusive rather than passed.

Evidence must include enough visible UI state to prove the user-facing path was used: the visible affordance before interaction, the visible submitted values or selected state when relevant, and the visible result after interaction. Evidence from hidden DOM state, internal selectors, automation APIs, network calls, or database/API verification alone is invalid for proving the UI operation path.

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
