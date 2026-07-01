# E2E Test Skill 示例中文版

使用这些示例作为生成测试用例的质量标尺。不要盲目复制示例领域；需要根据用户的 PRD 和 UI 调整参与者、UI 文案、数据命名、数据库字段和外部系统验证方式。

> 说明：这是 `examples.md` 的中文阅读版，原始英文参考文件仍为 `references/examples.md`。

## 模式目录

- **示例 1：外部系统同步**：适用于一次可见 UI 操作同时创建/更新产品数据和外部事实源数据的场景。
- **示例 2：执行结果分类**：适用于执行后区分首次通过、修复后通过、未修复失败、阻塞、跳过、延期 BUG 和清理状态。
- **示例 3：用例质量对比**：适用于生成结果过于空泛、缺少精确 UI 路径和独立验证时。
- **示例 4：多角色审批和可见性**：适用于提交/审核/通过/驳回、角色边界、租户隔离和审计链路。
- **示例 5：基础数据生命周期**：适用于简单创建/编辑/删除流程；如果需要定位失败点，应拆成多个用例。
- **示例 6：权限边界**：适用于角色专属操作、受限可见性和越权防护。
- **示例 7：异步状态流转**：适用于队列/后台任务/延迟完成；需要按场景补充超时、失败态、重试和重复提交检查。
- **示例 8：统计/分析看板**：适用于报表、看板、排行和运营分析类场景；指标必须由源业务变化证明，不能只把静态数字看一遍。
## 示例 1：外部 API 资产创建

模式：通过用户创建的产品对象同步外部系统。
适用：可见 UI 操作会创建产品数据，并在外部事实源系统中创建或同步数据。
不要照抄：请把 Ability、API Hub、cap-market、OpenAPI 替换成用户产品中的真实领域对象、事实源和验证面。

背景：
- PRD 说明用户可以创建一个“能力”，并选择 API 作为服务方式。
- UI 中包含工作台、资产管理能力页面、创建能力抽屉、服务方式步骤、服务内容步骤和完成步骤。
- 产品数据库会存储外部 API 分组引用。
- API 资产的事实源是外部 API Hub。

### 测试套件片段

```markdown
# E2E Test Plan: Ability API Integration

Scope:
- In scope: 创建 API 服务方式的能力，将 OpenAPI 导入 API Hub，验证产品数据库和 API Hub 一致性。
- Out of scope: API 运行时网关调用和性能。

Assumptions:
- 前后端联调和冒烟测试已经通过。
- 测试环境可以创建产品记录和 API Hub 分组。

Environment:
- Product URL: 待提供
- Database: cap-market 测试数据库
- External systems: API Hub 测试环境
- Test accounts: 根据 PRD 推导，执行前需要创建或提供
- Test data run ID: E2E-ability-api-202606231430-A7K2

Review Status:
- Current status: Waiting for user review
- Reviewer: Product owner / QA owner
- Review notes: Pending
- Last updated: 2026-06-23 14:30

Execution Authorization:
- Current status: Not requested
- Authorized by:
- Authorization notes:
- Authorized at:

Coverage Summary:
| ID | Priority | Title | Actor | Main UI Path | Independent Verification | Status |
|---|---|---|---|---|---|---|
| API-E2E-001 | P0 | 创建 API 服务方式的能力 | Employee U-001 | Workbench > Asset Management > Ability > Create Ability | cap-market DB + API Hub 分组/接口查询 | Draft |
```

### Mock 和数据计划片段

```markdown
## Mock and Test Data Plan

Run ID:
- `E2E-ability-api-202606231430-A7K2`

Data Naming Rule:
- `E2E-AbilityAPI-{timestamp}-{short_random}`

Test Subject Matrix:
| Subject ID | Account/User | Role | Tenant/Domain | App/Ownership | Permission Purpose | Source |
|---|---|---|---|---|---|---|
| U-001 | employee_a@example.test | Employee | Tenant A | API Test App owner | 创建/管理自己的资产 | To create |
| U-002 | domain_admin_a@example.test | Domain admin | Tenant A | - | 查看租户资产 | To create |
| U-003 | employee_b@example.test | Employee | Tenant B | API Test App B owner | 跨租户可见性检查 | To create |

Product Data:
| Data ID | Object Type | Name/Key | Created By | Used By Cases | Cleanup Rule |
|---|---|---|---|---|---|
| D-001 | Ability | E2E-AbilityAPI-202606231430-A7K2 | U-001 | API-E2E-001 | 失败时保留；通过时删除或下架 |

Files:
| File ID | File Name | Purpose | Generated/Provided | Used By Cases |
|---|---|---|---|---|
| F-001 | openapi-ability-api-a.yaml | 包含 3 个 endpoint 的 OpenAPI 源文件 | Generated | API-E2E-001 |

External System Data:
| External System | Object Type | Name/Key | Creation Method | Used By Cases | Cleanup Rule |
|---|---|---|---|---|---|
| API Hub | API Group | 产品根据 ability ID 生成 | 产品 UI 提交触发后端同步 | API-E2E-001 | 除非产品规则要求，否则不删除 |

User Must Provide Before Execution:
- 产品 URL 或本地运行命令
- cap-market 测试数据库只读访问权限
- API Hub 测试 API base URL 和读取 token
```

### 可执行测试用例

```markdown
### API-E2E-001 P0 创建 API 服务方式的能力

Purpose:
验证通过 UI 创建选择 API 服务方式的能力后，系统会创建一条产品能力记录、创建一个 API Hub 分组，并完整导入 OpenAPI 接口。

Actor:
- Account: employee_a@example.test
- Role/permissions: Employee，API Test App owner
- Tenant/domain: Tenant A

Preconditions:
- Product state: U-001 可以打开 Workbench，并有权限访问 Asset Management > Ability。
- External system state: API Hub 测试环境可访问，并且不存在当前 run ID 对应的分组。
- Required feature flags/config: 测试环境已开启 API Hub 集成。

Test Data:
- Generated data: ability name `E2E-AbilityAPI-202606231430-A7K2`
- Files: F-001 `openapi-ability-api-a.yaml`，预期 endpoint 数量 = 3
- Records to create: 通过 UI 创建一个 ability
- Data that must be provided by user: 产品 URL、数据库只读权限、API Hub read token

UI Operation Path:
1. 打开产品 URL。
2. 使用 employee_a@example.test 登录。
3. 打开 `Workbench`。
4. 在左侧导航中打开 `Asset Management` > `Ability`。
5. 点击 `Create Ability`。
6. 在基础信息步骤中，将能力名称填写为 `E2E-AbilityAPI-202606231430-A7K2`。
7. 按照 PRD 字段规则选择分类、领域、来源应用 `API Test App`、开放范围、描述和标签。
8. 点击 `Next`。
9. 在服务方式步骤中选择 `API`，除非用例另有说明，否则不要选择无关服务方式。
10. 点击 `Next`。
11. 在服务内容步骤中，通过可见上传入口上传 `openapi-ability-api-a.yaml`。
12. 确认 API 卡片显示已上传状态，并且接口预览显示 3 个 endpoint。
13. 确认或填写 API 名称、版本、标签和介绍。
14. 点击 `Next`。
15. 在文档步骤中选择在线 Markdown，并填写简短使用文档。
16. 点击 `Finish Create`。
17. 确认完成页显示创建成功。
18. 返回能力列表，确认存在一条名称为 `E2E-AbilityAPI-202606231430-A7K2` 的新记录。

Independent Verification:
1. 通过能力名称 `E2E-AbilityAPI-202606231430-A7K2` 查询 cap-market ability 表。
2. 验证只存在一条产品 ability 记录。
3. 验证 `service_methods` 包含 `API`。
4. 验证 `apihub_group_id` 非空。
5. 通过 `apihub_group_id` 查询 API Hub 分组详情。
6. 验证 API Hub 分组存在，并且与该 ability 或其生成的分组名关联。
7. 通过 `apihub_group_id` 查询 API Hub 接口列表。
8. 验证 method、path 和 summary 与 OpenAPI 文件一致。
9. 验证导入接口数量为 3。
10. 通过生成的 ability/group key 查询 API Hub 分组，确认不存在重复分组。

Expected Results:
- UI: 创建成功，能力列表中出现该能力，并显示 API 服务方式。
- Product database: 存在一条 ability 记录，状态为初始完成/未发布状态，且 `apihub_group_id` 已填充。
- External system: 存在一个 API Hub 分组，且包含 3 个已导入接口。
- Side effects: 没有重复创建产品 ability 或 API Hub 分组。

Evidence To Capture:
- 服务内容步骤截图，显示已上传 OpenAPI，且预览 3 个 endpoint。
- 创建后能力列表行截图。
- 产品 ability ID 和 `apihub_group_id`。
- API Hub 分组查询响应摘录。
- API Hub 接口列表响应摘录，count = 3。

Cleanup:
- 如果通过，按环境清理规则删除或下架该 ability。
- 如果失败或阻塞，保留产品和 API Hub 数据以便排查。

Blocking Decision Rule:
如果 UI 无法创建任何 ability，或 API Hub 同步在所有 API 创建用例中都失败，则停止并询问用户，因为这会阻塞大部分集成 E2E 用例。
```

## 示例 2：执行结果条目

模式：运行后的结果分类和缺陷归账。
适用：总结已执行测试套件，或把执行结果追加到已批准的测试计划中。
不要照抄：保留分类方式，但要根据真实运行调整证据 ID、BUG 严重级别、修复状态和发布建议。

使用精确的结果分类。不要把所有失败都折叠成一个笼统的 failed。

```markdown
## E2E Test Execution Results

Scope:
- Ability API integration / test environment / run E2E-ability-api-202606231430-A7K2

Result:
| Total | Passed First Try | Passed After Fix | Failed Unrepaired | Blocked | Skipped |
|---:|---:|---:|---:|---:|---:|
| 3 | 1 | 1 | 1 | 0 | 0 |

Executed Cases:
| ID | Title | Status | First Result | Final Result | Key Evidence | Bug/Fix Status | Notes |
|---|---|---|---|---|---|---|---|
| API-E2E-001 | 创建 API 服务方式的能力 | Passed First Try | Passed | Passed | ability_id=ab_1024, apihub_group_id=grp_7788, interface_count=3 | None | UI 列表、数据库和 API Hub 均一致 |
| API-E2E-002 | 保存草稿不应创建 API Hub 分组 | Passed After Fix | Failed: 草稿创建了分组 | Passed after fix | 修复前 grp_7790 存在；修复后 apihub_group_id=null | BUG-001 fixed | 重跑后数据干净 |
| API-E2E-003 | 无效 OpenAPI 应阻止创建 | Failed Unrepaired | Failed | Failed | UI 允许无效文件进入下一步 | BUG-002 open | 用户决定是否现在修复 |

Defects:
| Severity | Case | Bug | Impact | Blocking | Fix Status | Suggested Next Step |
|---|---|---|---|---|---|---|
| High | API-E2E-002 | 保存草稿错误触发 API Hub 分组创建 | 污染外部 API Hub，违反 PRD | 修复后不阻塞 | Fixed | 保留回归用例 |
| Medium | API-E2E-003 | 无效 OpenAPI 可以继续下一步 | 坏数据可能进入 API Hub 导入流程 | No | Open | 用户决定修复时机 |

Deferred Bugs:
| Bug ID | Case | Reason Deferred | Risk | User Decision Needed |
|---|---|---|---|---|
| BUG-002 | API-E2E-003 | 不阻塞剩余已批准 P0 流程 | 无效输入保护不完整 | 决定发布前修复还是延期 |
```

## 示例 3：差用例 vs 好用例

模式：模糊测试点与可执行 E2E 用例的质量对比。
适用：生成的用例像泛泛测试点，而不是可运行步骤时。
不要照抄：保留这种具体程度，不要照抄 API 能力领域。

差用例，过于模糊：

```markdown
1. 创建一个 API 能力。
2. 检查数据库。
3. 检查 API Hub。
Expected: success.
```

好用例：

```markdown
1. 打开 Workbench > Asset Management > Ability。
2. 点击 Create Ability。
3. 填写准确的能力名称和必填字段。
4. 在服务方式步骤中选择 API。
5. 通过可见上传入口上传指定 OpenAPI 文件，并确认 endpoint 预览数量。
6. 通过 UI 完成创建。
7. 确认列表中仅出现一条使用生成能力名称的新记录。
8. 通过能力名称查询产品数据库，并验证 `apihub_group_id` 非空。
9. 通过 `apihub_group_id` 查询 API Hub，并验证分组存在。
10. 查询 API Hub 接口，验证数量和路径与 OpenAPI 源文件一致。
Expected: UI、产品数据库和 API Hub 互相一致。
```

## 示例 4：带角色可见性的审批流

模式：多角色状态流转、可见性隔离和审计验证。
适用：PRD 描述提交/审核/通过/驳回流程、状态流转、租户或范围边界，以及基于角色的可见性。
不要照抄：请将 requester/reviewer/scope 替换为产品真实参与者、授权模型和审计来源。

当 PRD 描述提交/审核/通过/驳回流程、状态流转和基于角色的可见性时，使用此模式。

背景：
- PRD 说明请求人可以提交资源申请等待审批。
- 审核人可以审批或驳回同一租户或业务范围内的申请。
- 其他租户的请求人不能看到或操作该申请。
- 产品数据库存储申请状态、请求人、审核人和审计记录。

### 测试套件片段

```markdown
# E2E Test Plan: Resource Request Approval

Scope:
- In scope: 提交申请、审核人审批、请求人状态可见性、跨范围隔离、审计记录验证。
- Out of scope: 通知投递和审批 SLA 时效。

Environment:
- Product URL: 待提供
- Database: 产品测试数据库
- External systems: 该流程不需要
- Test accounts: 根据 PRD 推导，执行前需要创建或提供
- Test data run ID: E2E-approval-202606231530-B4Q8

Review Status:
- Current status: Waiting for user review
- Reviewer: Product owner / QA owner
- Review notes: Pending
- Last updated: 2026-06-23 15:30

Execution Authorization:
- Current status: Not requested
- Authorized by:
- Authorization notes:
- Authorized at:
```

### Mock 和数据计划片段

```markdown
## Mock and Test Data Plan

Run ID:
- `E2E-approval-202606231530-B4Q8`

Test Subject Matrix:
| Subject ID | Account/User | Role | Tenant/Domain | App/Ownership | Permission Purpose | Source |
|---|---|---|---|---|---|---|
| U-001 | requester_a@example.test | Requester | Scope A | Own request | 提交并查看自己的申请 | To create |
| U-002 | reviewer_a@example.test | Reviewer | Scope A | Review queue A | 审批范围内申请 | To create |
| U-003 | requester_b@example.test | Requester | Scope B | Own request | 验证跨范围隔离 | To create |

Product Data:
| Data ID | Object Type | Name/Key | Created By | Used By Cases | Cleanup Rule |
|---|---|---|---|---|---|
| D-001 | Resource request | E2E-approval-202606231530-B4Q8 | U-001 | APPROVAL-E2E-001 | 失败时保留；通过时删除或归档 |

User Must Provide Before Execution:
- 产品 URL 或本地运行命令
- request 和 audit 表的数据库只读访问权限
- 测试账号或账号创建权限
```

### 可执行测试用例

```markdown
### APPROVAL-E2E-001 P0 提交并审批申请，验证审计链路

Purpose:
验证请求人可以通过 UI 提交申请，有权限的审核人可以审批，请求人可以看到状态更新，并且产品数据库状态和审计记录一致。

Actor:
- Submitter: requester_a@example.test, Requester, Scope A
- Reviewer: reviewer_a@example.test, Reviewer, Scope A
- Restricted actor: requester_b@example.test, Requester, Scope B

Preconditions:
- U-001 可以访问申请创建页。
- U-002 可以访问 Scope A 的审核队列。
- U-003 属于不同范围，不能看到 Scope A 的申请。

Test Data:
- Generated request title: `E2E-approval-202606231530-B4Q8`
- Records to create: 通过 UI 创建一条申请
- Data that must be provided by user: 产品 URL、数据库只读权限、账号或账号创建权限

UI Operation Path:
1. 使用 requester_a@example.test 登录。
2. 打开 `Requests`。
3. 点击 `New Request`。
4. 将申请标题填写为 `E2E-approval-202606231530-B4Q8`。
5. 按 PRD 规则填写必填字段。
6. 点击 `Submit`。
7. 确认详情页或列表显示状态 `Pending Review`。
8. 退出登录，并使用 reviewer_a@example.test 登录。
9. 打开 `Review Queue`。
10. 打开 `E2E-approval-202606231530-B4Q8` 对应行。
11. 确认提交字段值与请求人输入一致。
12. 点击 `Approve`。
13. 确认申请状态变为 `Approved`。
14. 退出登录，并使用 requester_a@example.test 登录。
15. 打开 `My Requests`，确认同一申请显示状态 `Approved`。
16. 退出登录，并使用 requester_b@example.test 登录。
17. 搜索或浏览申请列表，确认看不到 Scope A 的申请。

Independent Verification:
1. 通过标题 `E2E-approval-202606231530-B4Q8` 查询产品 request 表。
2. 验证只存在一条 request 记录。
3. 验证 requester ID 映射到 U-001，reviewer ID 映射到 U-002。
4. 验证最终状态为 `Approved`。
5. 通过 request ID 查询 audit 表。
6. 验证存在一条 submit 事件和一条 approve 事件，且顺序正确。
7. 验证没有任何权限授权或可见性记录将该申请暴露给 U-003 或 Scope B。

Expected Results:
- UI: 请求人看到 pending 后变为 approved；审核人可以审批；受限用户看不到该申请。
- Product database: 存在一条 request 记录，最终状态为 approved，请求人和审核人正确，且无重复记录。
- Audit trail: submit 和 approve 事件按正确顺序存在。
- Side effects: 不存在跨范围可见性泄露。

Evidence To Capture:
- 已提交申请显示 `Pending Review` 的截图。
- 审核人审批前页面截图。
- 请求人视角显示 `Approved` 的截图。
- 受限用户无法找到该申请的截图或可见状态。
- Request record ID 和最终状态。
- Audit event 查询摘录。

Cleanup:
- 如果通过，按环境规则删除或归档该申请。
- 如果失败或阻塞，保留 request 和 audit 记录以便排查。

Blocking Decision Rule:
如果审核人无法访问审核队列、审批结果无法持久化，或跨范围用户可以看到该申请，则停止并询问用户，因为这些失败会使审批流覆盖失效。
```

## 示例 5：简单 CRUD 与数据库验证

模式：基础产品数据生命周期。
适用：验证简单的创建、编辑、删除、列表或详情一致性。
不要照抄：当创建/编辑/删除分别有不同风险、权限或失败处理时，应拆成独立用例。

背景：
- PRD 说明用户可以通过 UI 创建、编辑和删除一条基础记录。
- 产品数据库是事实源。

好用例形态：

```markdown
### CRUD-E2E-001 P0 创建记录并验证持久化

Purpose:
验证通过 UI 创建的记录会出现在列表中，持久化到数据库，并且可以通过 UI 编辑和移除。

Actor:
- Account: user_a@example.test
- Role/permissions: 拥有创建/编辑/删除权限的标准用户
- Tenant/domain: Tenant A

UI Operation Path:
1. 打开记录列表页。
2. 点击 `New`。
3. 填写必填字段。
4. 点击 `Save`。
5. 确认新记录行出现。
6. 打开该记录行并编辑一个字段。
7. 再次保存。
8. 通过 UI 删除该记录。

Independent Verification:
1. 通过生成的记录 key 查询产品数据库。
2. 验证创建、编辑和删除状态与 UI 流程一致。
```

## 示例 6：权限边界与受限用户

模式：权限边界和负向授权验证。
适用：某能力对一个角色可用，但对另一个角色隐藏、禁用或被阻止。
不要照抄：如果产品可能通过深链、搜索结果、详情页等入口暴露资源，也要覆盖这些路径或独立验证。

背景：
- PRD 说明管理员可以管理某资源，但普通用户只能查看。

好用例形态：

```markdown
### PERM-E2E-001 P0 普通用户看不到管理员专属操作

Purpose:
验证受限用户不能看到或使用管理员专属操作，而管理员可以看到并使用。

Actor:
- Admin: admin_a@example.test
- Restricted user: user_b@example.test

UI Operation Path:
1. 以管理员身份登录，并确认该操作存在。
2. 退出登录，以受限用户身份登录。
3. 打开同一页面。
4. 确认该操作被隐藏或禁用。

Independent Verification:
1. 检查权限表或审计日志。
2. 验证受限用户没有获得未授权权限。
```

## 示例 7：异步状态变化与独立验证

模式：异步处理和最终状态一致性。
适用：UI 提交触发队列、延迟任务、回调、webhook 或后台处理。
不要照抄：应按实际场景补充超时、轮询间隔、中间态、失败态、重试行为、重复提交保护和清理规则。

背景：
- PRD 说明提交任务后会创建一个排队任务，并在稍后完成。

好用例形态：

```markdown
### ASYNC-E2E-001 P1 提交任务并验证完成信号

Purpose:
验证 UI 提交会创建任务，处理后状态发生变化，并且后端记录与最终状态一致。

UI Operation Path:
1. 打开任务表单。
2. 提交一个有效任务。
3. 确认 UI 显示 queued 或 processing。
4. 刷新或重新打开，直到最终状态出现。

Independent Verification:
1. 通过生成的 job ID 查询 job 表或队列。
2. 验证状态从 queued 转为 completed。
3. 如果 PRD 要求，检查日志或 callback 记录。
```
## 示例 8：统计/分析看板

模式：通过源业务变化证明指标，并验证 UI/API/DB 一致性。
适用：PRD 描述运营分析、统计、报表、看板、排行、筛选或运营监控。
不要照抄：请替换资源、指标名、筛选项、角色和数据来源；保留测试模式，不要复制具体业务域。

坏用例形态，过于浅：

```markdown
1. 打开分析看板。
2. 确认指标卡片和图表可见。
3. 调一次汇总 API，比对当前数字。
Expected: 看板数据正确。
```

为什么弱：
- 只检查静态视图。
- 没有证明数据从哪里来。
- 没有证明筛选、排行、空态或跨范围隔离。
- 即使源业务动作已经不能更新统计，也可能通过。

好套件形态：

```markdown
## 统计数据矩阵

| Data ID | 目的 | 时间范围 | 范围/租户 | 分类 | 状态 | 类型 | 排行值 | 创建方式 | 用于用例 |
|---|---|---|---|---|---|---|---:|---|---|
| M-001 | 基线总量 | 今日 | Tenant A | Category X | active | API | 5 | SQL seed | ANALYTICS-E2E-001, 002 |
| M-002 | 跨范围隔离 | 近7天 | Tenant B | Category Y | active | API | 3 | SQL seed | ANALYTICS-E2E-003 |
| M-003 | 空态对照 | 全部 | Tenant C | Category Z | none | none | 0 | 隔离范围 | ANALYTICS-E2E-004 |
```

```markdown
### ANALYTICS-E2E-001 P0 源业务动作会更新看板指标

Purpose:
验证通过可见 UI 创建并发布资源后，分析看板的总量和已发布指标按预期从 V0 变化到 V1。

Actor:
- Operator: operator_a@example.test，Tenant A，拥有创建和发布资源权限。

Preconditions:
- 可通过产品导航打开看板。
- 基线数据矩阵 M-001 已存在，并能通过 run ID 追踪。

UI Operation Path:
1. 打开分析看板，选择 `All time` 和 `Tenant A`。
2. 记录可见卡片上的指标值 V0。
3. 通过导航打开资源管理页。
4. 点击 `Create`，填写带 run ID 的名称，并通过可见表单保存。
5. 按 PRD 要求通过可见 UI 发布或审批该资源。
6. 回到分析看板，选择相同筛选条件。
7. 记录指标值 V1。

Independent Verification:
1. 使用相同 range 和 scope 查询分析 API，验证 API 返回 V1。
2. 通过生成的 run ID 查询产品数据库，验证状态、类型、范围和时间戳落在预期统计桶内。
3. 直接从源表或日志复算预期差值，验证 V1 - V0 等于预期变化。

Expected Results:
- UI、分析 API、数据库聚合结果一致。
- 相关指标按预期差值变化，而不是只断言非 0。
- 无关范围、分类或时间维度的指标不应变化。

Evidence To Capture:
- 源业务动作前后的看板截图。
- 资源创建/发布截图。
- V1 的分析 API 响应。
- 能证明差值的数据库聚合摘录。

Cleanup:
- 安全时删除或归档生成资源。
- 如果指标不一致需要排查，保留数据。

Blocking Decision Rule:
如果源业务动作不能通过 UI 完成，或无法读取分析 API/数据库作为独立验证，停止并询问用户；静态查看看板不足以验证该需求。
```

结果记录提醒：
- SQL 或 API 种子数据可以准备数据矩阵，但只能记录为 setup，不能当作 UI 业务路径通过的证明。
- 如果某用例只有 setup 后的 API/DB 校验，要标为 API/DB-only 或证据不完整，而不是完整 UI 路径通过。
- 如果 validator 失败被确认是误报，要先修 validator 或模板并重跑，再让用户决定是否接受残余风险。