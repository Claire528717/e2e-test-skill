# PRD Coverage Rules

Use this reference when designing or reviewing a PRD-backed E2E acceptance plan, especially when the user asks whether the suite covers the PRD or can be used as a deliverable test standard.

## Coverage Inventory

Before writing final cases, extract a requirement inventory from these PRD sources when present:

1. Explicit must-have / V1 scope checklists.
2. Acceptance criteria and release-blocking checks.
3. Role and permission matrices.
4. Business rules and visibility rules.
5. State machines and status-specific allowed actions.
6. Object fields and data consistency requirements.
7. Exception, failure, empty, disabled, timeout, and retry states.
8. Integration contracts and external-system side effects.
9. Versioning, audit, cleanup, and history-retention rules.
10. Non-functional requirements such as SLA, performance, availability, and concurrency.
11. Out-of-scope or deferred items, so reviewers can see they were intentionally excluded.
12. Open decisions and blocking product questions.

If the PRD has numbered sections, keep the section number or stable title in the inventory. If the PRD uses unchecked checklist items, preserve each checklist item as a separate coverage row unless several items are inseparable in one UI workflow.

## Coverage Status

Assign every inventory row exactly one coverage status. Do not combine multiple statuses in one cell; use separate risk and decision fields for nuance.

- `Covered`: at least one executable case validates the item through a visible UI path and independent verification.
- `Partially covered`: a case touches the item, but a role, state, failure branch, data consistency check, or external verification path is missing.
- `Blocked`: the item cannot be planned or executed honestly because a product decision, account, permission, environment, source-of-truth system, or test data path is missing.
- `Out of E2E / specialty`: the item needs another test type such as performance, load, security, accessibility, disaster recovery, or manual content review.
- `Out of release scope`: the PRD explicitly excludes or defers the item.

Never mark an item covered only because a broad workflow passes nearby. Example: an approval happy path does not cover rejection, resubmission, cross-tenant isolation, audit trails, or disabled actions unless those are explicitly tested.

## Risk Marking

Mark high-risk items separately from coverage status.

- Risk level explains business impact and execution priority, such as High / Medium / Low or P0 / P1 / P2.
- Coverage status explains whether the case is planned and verifiable: Covered, Partially covered, Blocked, Out of E2E / specialty, or Out of release scope.
- A row must not use mixed status labels such as `Covered / Blocked` or `已覆盖/阻塞待确认`. Instead, choose one coverage status and put the risk, blocker, or decision in a separate `Risk` or `Gap / Decision` column.
- High-risk partially covered or blocked items should be easy for the user to find without scanning every case.

## Matrix Requirements

A full deliverable acceptance plan must include a section named one of:

- `## PRD Coverage Audit`
- `## PRD 全量覆盖审计`
- `## Requirement Coverage Matrix`
- `## 需求覆盖矩阵`

The matrix must include, at minimum:

| PRD Item | Acceptance Point | Risk | Coverage Status | Case IDs | Gap / Decision |
|---|---|---|---|---|---|

For Chinese plans, equivalent Chinese headers are acceptable.

For high-risk PRD-backed plans, add a risk column or a separate high-risk register:

| PRD Item | Risk | Coverage Status | Case IDs | Gap / Decision |
|---|---|---|---|---|

## Case Expansion Rules

For every `Partially covered` high-risk item, do one of the following before review. For lower-risk partially covered items, clearly mark the missing branch and decision needed:

- Add the missing branch to an existing case when it shares setup and verification.
- Add a new case when the missing branch has a distinct actor, permission boundary, state transition, failure mode, source-of-truth check, or cleanup rule.
- Mark it blocked or specialty with a concrete reason and user decision needed.

Create separate cases for these high-risk branches unless the PRD explicitly says they are not required:

- Create, edit, delete/downline, publish, unpublish, approve, reject, resubmit, transfer, subscribe, update, download, share, revoke.
- Role differences between ordinary user, domain/admin user, platform/global admin, restricted/cross-tenant user, and system/integration actor.
- State-specific disabled actions, especially pending review, rejected, offline, expired, unauthorized, already subscribed, and no-data states.
- Data subject differences such as user-subject subscription versus app-subject subscription.
- External side effects such as API Hub sync, gateway credential issue, resource package delivery, audit event creation, notification, queue job, or file generation.
- Failure branches where PRD requires explicit user feedback.

## Specialty And Blocked Items

Do not force non-E2E requirements into weak UI cases. Put them in the coverage audit as specialty or blocked when appropriate.

Common specialty items:

- Page response SLA, upload duration, scanner latency, credential issue latency, monthly availability, concurrency.
- Penetration/security testing and vulnerability scanning.
- Accessibility audits.
- Data migration or disaster recovery.

Common blocked items:

- Scanning service source or rules are not decided.
- Real test accounts and roles cannot be created.
- API/database/log/source-of-truth access is unavailable.
- External integration sandbox is missing.
- Cleanup permissions are undefined.

Plainly explain the impact. Example: `安全扫描来源未确认，因此扫描不通过、重试、超时提示只能设计为用例，不能执行为上线证据。`

## Review Gate

Before asking the user to review a full acceptance plan, confirm:

- Every explicit PRD must-have and acceptance item appears in the coverage audit.
- Every Covered row points to at least one case ID that exists in the plan.
- No coverage row uses mixed statuses such as 已覆盖/部分覆盖; risk and blockers are separated into their own fields.
- High-risk partially covered or blocked rows are visible in the coverage audit or high-risk register.
- Every P0/P1 business rule, permission boundary, state transition, and integration side effect is covered or explicitly blocked.
- The suite title and scope honestly say whether this is a full release plan, focused slice, prototype-only plan, or formal environment plan.
- The coverage audit does not still say `suggested case` after the case has been added.

If any of these checks fail, update the plan before requesting review.