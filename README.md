# E2E Test Skill

`e2e-test-skill` 是一个面向 Codex/Agent 的端到端验收测试 Skill，用于根据 PRD 和真实 UI 来源生成可评审、可执行、可追踪证据的 E2E 测试计划。它适合产品经理在开发和联调完成后，推动 Agent 像真实测试人员一样完成验收测试、采集证据、验证数据一致性，并输出可决策的运行总结。

这个仓库根目录就是正式 Skill 包入口；Agent 实际读取的规则以 `SKILL.md` 为准。`README.md` 主要面向 GitHub 访客和维护者，解释这个 Skill 的目标、边界、目录和脚本。

## 核心目标

这个 Skill 不只是生成测试点，而是把 PRD、页面、测试数据、依赖条件、执行证据和用户决策串成一个完整验收流程。

它默认先生成测试计划，停止等待用户评审；只有用户确认或修改计划，并明确要求执行 E2E 后，Agent 才开始真实测试。评审通过测试计划不等于授权执行，也不等于最终上线验收。

对于有 PRD 支撑的验收，Skill 默认追求完整 PRD 覆盖，而不是代表性 happy path。每个明确需求、验收标准、角色权限、业务规则、状态流转、异常/空状态、数据一致性规则和非功能/SLA 项，都要映射为已覆盖、部分覆盖、阻塞、超出 E2E/专项或超出发布范围。

## 适用阶段

最适合在以下阶段使用：

- 前端开发已完成
- 后端开发已完成
- 前后端联调已完成
- 冒烟测试已通过
- 准备进行全局 E2E 测试、验收测试或发布前回归

不适合用于单元测试、开发自测、早期接口联调、纯接口自动化测试、性能压测、安全渗透测试或生产事故修复。

## 运行纪律

Skill 要保持 UI 操作和独立验证分离：

- UI 操作路径：像真实用户一样，通过可见页面、导航、表单、抽屉、弹窗、上传、确认和状态变化操作。
- 独立验证：完成 UI 操作后，通过数据库、API、日志、队列、文件、后台系统或外部系统验证持久化或集成结果。

禁止用直接调用 API、写数据库、操作隐藏 DOM、派发合成事件、写入 storage/session、调用组件内部方法，或自动化专用捷径来替代被测 UI 操作。如果产品没有可见路径，就把用例标记为阻塞或失败。

缺少关键证据的用例不能标记为完整通过。对于通过的 UI 用例，需要主动保存 UI 截图，不能只依赖 Playwright 等测试框架的 `only-on-failure` 失败截图配置。DB/API/log 证据用于证明数据和集成结果，不能替代 UI 路径证据。

## 用户决策节点

Skill 使用三个用户决策节点：

1. 用例评审节点：用户评审用例质量、PRD 覆盖完整性、高风险项、假设和数据需求，用于决定是否执行 E2E。
2. 阻塞 BUG 节点：执行中遇到阻塞当前用例、影响大量后续覆盖，或让必要验证不可靠的 BUG 时，停止让用户决策。
3. 结果与修复节点：执行后展示结果、BUG、证据、清理状态和残余风险，让用户决定修复、延期、重跑或查看修复后结果。

计划顶部需要包含 PM 审核包。PM 审核包是给非技术产品经理优先阅读的决策面，包含决策摘要、自动质量门禁、二轮复核结果、覆盖缺口、高风险项、阻塞项和当前需要用户拍板的 1-3 个事项。详细用例是支撑材料，不要求用户第一次决策时逐条阅读。

## 依赖说明

生成测试用例依赖：

- PRD 或等价需求说明。
- 真实 UI 来源，例如截图、原型、HTML、运行中的产品或前端代码。
- 基本业务规则，例如谁能操作、什么状态可以流转、成功后应该看到什么结果。

执行测试用例还依赖：

- 能打开的本地、测试或预发环境。
- 测试账号、角色、租户、权限，或允许安全创建/mock 它们。
- 能验证结果的渠道，例如数据库只读查询、后端 API、日志、队列、文件、管理后台或外部系统。
- 明确的数据操作边界，例如能否创建、修改、删除和清理测试数据。
- 用户明确授权执行。

如果用户无法提供账号、租户、角色、应用或权限，Skill 可以在规划阶段根据 PRD 推导 mock 测试主体矩阵。真实执行时不能假装这些主体已经存在，必须把它们作为待创建或待提供的数据需求，或者在环境支持时创建隔离 mock 数据。

## 仓库结构

```text
e2e-test-skill/
├── README.md
├── SKILL.md
├── agents/
│   ├── openai.yaml
│   └── reviewer.yaml
├── references/
│   ├── workflow.md
│   ├── coverage.md
│   ├── templates.md
│   ├── examples.md
│   └── execution-guardrails.md
├── scripts/
│   ├── create_run_id.py
│   ├── scaffold_plan.py
│   ├── validate_plan.py
│   └── validate_evidence.py
├── dev/
│   └── zh-CN/
├── e2e-test-plans/        # generated, ignored
└── e2e-test-evidence/     # generated, ignored
```

说明：

- `SKILL.md`：Skill 主入口，定义运行规则、工作流、引用文件路由和脚本入口。
- `agents/openai.yaml`：Skill 展示和 Agent 配置元数据。
- `agents/reviewer.yaml`：二轮评审 agent 配置，用于在大型或 PRD 支撑计划进入用户评审前做独立复核。
- `references/workflow.md`：详细工作流、依赖发现、测试数据规则、评审门禁、执行就绪和结果分类。
- `references/coverage.md`：PRD 覆盖审计规则、覆盖状态定义和需求矩阵质量要求。
- `references/templates.md`：测试计划、PM 审核包、覆盖矩阵、数据计划、用例和执行总结模板。
- `references/examples.md`：高质量测试用例示例，用于约束生成质量。
- `references/execution-guardrails.md`：执行阶段的 UI 保真、证据、生产安全和阻塞 BUG 规则。
- `scripts/create_run_id.py`：生成标准 E2E run ID。
- `scripts/scaffold_plan.py`：根据 feature/run ID 生成测试计划骨架，并创建证据目录。
- `scripts/validate_plan.py`：在评审或执行前检查计划结构、PRD 覆盖审计、PM 审核包、二轮复核和独立验证等硬性要求。
- `scripts/validate_evidence.py`：执行后检查已通过 UI 用例是否有截图证据，P0 通过用例是否有独立证据文件。
- `dev/zh-CN/`：中文阅读版和中文模板，方便维护中文输出；正式入口仍以根目录 `SKILL.md` 为准。
- `e2e-test-plans/`：Skill 运行时生成的测试计划目录，属于输出产物，不建议默认提交。
- `e2e-test-evidence/`：Skill 运行时生成的截图、记录和验证证据目录，属于输出产物，不建议默认提交。

## 工作流程

1. 发现：阅读 PRD 和 UI 来源，识别参与者、对象、状态、规则、操作路径和集成点。
2. 分析：抽取能力、状态流转、权限、事实源系统和验收标准，建立 PRD 覆盖审计。
3. 设计：生成专用 E2E 测试计划文件，包含 PM 审核包、覆盖审计、mock/数据计划、主体矩阵和详细用例。
4. 自动门禁：运行 `scripts/validate_plan.py`，修复结构性失败后再请求用户评审。
5. 二轮复核：大型或 PRD 支撑计划需要通过独立 reviewer agent 复核关键风险、覆盖缺口和用户决策。
6. 用户评审：用户决定执行、修改或标记阻塞。
7. 执行：用户明确授权后，刷新 URL、账号、验证访问和清理权限，严格按 UI 路径执行。
8. 证据采集：保存 UI 截图、DB/API/log/external-system 证据和清理状态。
9. 证据校验：执行后运行 `scripts/validate_evidence.py`，缺少必要证据的通过用例降级为无法确认。
10. 汇总：在同一个计划文件中补充执行结果、证据引用、BUG、修复状态、延期项、清理状态和残余风险。

## 脚本工具

```bash
python3 scripts/create_run_id.py "ability api"
python3 scripts/scaffold_plan.py "ability api" --run-id E2E-ability-api-202606241130-A7K2
python3 scripts/validate_plan.py e2e-test-plans/e2e-test-plan-ability-api-E2E-ability-api-202606241130-A7K2.md
python3 scripts/validate_evidence.py e2e-test-plans/e2e-test-plan-ability-api-E2E-ability-api-202606241130-A7K2.md
```

这些脚本只负责确定性门禁和文件布局，不替代对 PRD、UI 和业务规则的分析。

`validate_plan.py` 用于执行前，防止缺少 PM 审核包、决策摘要、自动质量门禁、二轮复核、PRD 覆盖审计、真实 UI 路径、独立验证、证据和清理规则的计划进入评审或执行。

`validate_evidence.py` 用于执行后，防止只有 DB/API/log 文本、没有 UI 截图的结果被标记为完整通过。

## 安装方式

通过 GitHub 安装时，直接安装仓库根目录。根目录包含 `SKILL.md`、`references/`、`scripts/` 和 `agents/`，不需要再指定子目录。

建议安装后的 Skill 名称使用：

```text
e2e-test-skill
```

默认生成的测试计划建议放在 `e2e-test-plans/`，证据放在 `e2e-test-evidence/{run_id}/`。这些运行产物默认会被 `.gitignore` 忽略；如果某次验收结果需要长期归档，建议单独挑选报告或证据文件提交，而不是把整个输出目录加入版本控制。
