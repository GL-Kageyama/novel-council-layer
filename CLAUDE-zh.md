**Language:** [English](CLAUDE.md) | [日本語](CLAUDE-ja.md) | 中文

# Novel Council Layer

## 项目身份

这是**小说评议会（Novel Council Layer）**。这是一组Claude Code代理：多个AI评价者代理从不同的叙事视角评价小说，由合议技能生成结构化的Story Report。

> **角色分工**: 本层**仅负责评价**。作品的**执笔**交由作者、编辑和生成式AI。本仓库承担的并非"写作"，而是"识别故事的价值"，并将评价结果整理为可交给下次改写的素材。

## 核心命题

**故事是在时间中被阅读的。** 小说不是对象，而是在读者内心随时间展开的体验。评价的对象是"被阅读时间的质量"，而非作品的属性。

叙事评价所特有的7个问题:
1. **时间的质量** —— 这个故事如何支配读者的时间？
2. **信息的分配** —— 什么、在何时、向谁揭示？
3. **叙事的距离** —— 谁来讲述，从多远的距离讲述？
4. **留白的设计** —— 读者应当填补的空隙是否经过有意的设计？
5. **文体与时间的一致** —— 文体是否控制了阅读的速度与感受？
6. **重读的深度** —— 读第二遍时，同一本书是否变成了另一本书？
7. **读后的位移** —— 读完之后，是否留下"人生中有什么东西发生了移动"的感觉？

## 核心哲学

- **故事是时间的艺术**: 评价的对象是"被阅读时间的质量"。
- **复调评价**: 由持有不同视角的多个评价者进行合议。
- **不一致本身就是信号**: 评价者之间的对立不予平均化，而是原样保留。
- **双重盲检**: 从输入（作者名、作品名）与基准（专有名词）两侧屏蔽名声。这是守护被埋没杰作之发现的先决条件。
- **评价重于生成**: 识别故事的价值才是竞争领域。

## 目录约定

- `agents/{name}.md` — 评价者代理的正本（11位）。作为基于人格的专家，以独立子代理启动
- `skills/story-council/SKILL.md` — 合议编排者的正本（唯一技能）
- `.claude/agents/` — 用于项目内发现的symlink（评价者代理）
- `.claude/skills/` — 用于项目内发现的symlink（合议编排者）
- `~/.claude/agents/`, `~/.claude/skills/` — 全局安装位置（通过`./install.sh`设置，可在任何地方调用）
- `.claude-plugin/` — 插件分发定义（用于`/plugin marketplace add`）
- `schemas/` — 结构化输出的JSON schema
- `references/` — 叙事评价的理论基础（命题的谱系・结构性校准・盲检・基准）
- `examples/` — 示例输入与输出
- `utils/` — 匿名化・验证・可视化・比较实用工具

## 评价者的调用方式

**合议以技能调用，评价者以子代理调用。** 这一角色分工是架构的要害——评价者必须在互不知晓对方结果的情况下独立评价。技能共享同一上下文，因此不适合独立评价。将评价者作为子代理启动，可以隔离上下文。

### 全体合议（推荐）

```
Skill: story-council
Args: {"content": "...", "content_type": "text", "domain": "pure-literature"}
```

合议将执行以下步骤:
1. 判定输入的故事子领域
2. 选择相关的评价者代理（始终包含 `anti-generic-story-filter`）
3. 将各评价者作为子代理启动（经由Agent tool，互不知晓结果，独立评价）
4. 整合到Story Report
5. 保存所有不一致

### 情节评价模式（只有梗概也能评价）

指定 `content_type: "plot"`，即可对执笔前的构想或简单梗概进行评价。由于不存在散文、叙事与阅读体验，`prose-style`、`narrative-technique`、`reader-experience` 这3位不被召集，由其余8位（narrative-originality, anti-generic-story-filter, emotional-power, plot-architecture, character-depth, theme-resonance, world-building, admiration）进行评价。

```
Skill: story-council
Args: {"content": "簡単なあらすじ...", "content_type": "plot", "domain": "genre-fiction"}
```

### 单一评价者

当只想评价特定视角时使用。评价者以子代理启动。

```
Agent tool, subagent_type: plot-architecture
Prompt: {"content": "...", "content_type": "text", "domain": "genre-fiction"}
```

若作为已安装的插件运行，请使用插件作用域名（`novel-council-layer:plot-architecture`）。

## 输出约定

所有评价者的输出都必须是符合 `schemas/novel-value-output.schema.json` 的有效JSON。

```bash
python utils/validate_output.py < output.json
python utils/validate_output.py --json output.json   # 機械可読な検証結果
```

**自动重试**: 合议技能用 `validate_output.py --json` 对每位评价者的输出进行**确定性验证**，不合格时对同一评价者**最多重启3次**（反馈中包含错误内容）。3次重试后仍不合格的，明确记录到 `excluded_evaluators` 中，记作 `reason: "JSON validation failed after 3 retries"`。**禁止静默丢弃。**

**坏了就重新生成（禁止人工修复）**: 评价者输出的JSON损坏时（`validate_output.py` 返回了 `"valid": false`），**不得手工直接编辑JSON来修复**。必须**重启该评价者以重新生成**，并用重新生成的输出重新验证。因为人手工修补JSON可能会破坏评价者的独立声音（分数・判断・文体・叙事），因此对损坏输出的应对方式统一为"重新生成"。

**输入要进行匿名化（第一重盲检）:**

```bash
python utils/anonymize.py input.txt --author "著者名" --title "作品名" > anonymized.txt
```

## 工具组

| 工具 | 作用 |
|--------|------|
| `utils/anonymize.py` | **输入匿名化**——去除作者名、作品名，建立盲检评价的前提（第一重盲检） |
| `utils/validate_output.py` | 评价者输出的schema验证。通过`--json`标志输出机器可读的结果（合议技能自动重试所使用） |
| `utils/render_report.py` | Story Report的视觉展示（11维条形图・分类徽章・维度间的对立）。用`-o report.md`保存为Markdown文档，用`--individuals`显示全部个别报告 |
| `utils/compare_reports.py` | 改写前后的差异比较（用于评价→改写循环） |

## 评价输出被设计为"输入"

**本层的评价结果本身并非最终成果。** 它是供作者、编辑和生成式AI进行改写的**输入**。

- 合议**不生成改写指示本身**。那是作者、编辑和生成式AI的职责。
- 取而代之，将每位评价者的**原始素材**（`weaknesses`・`improvement_suggestions`・`expected_disagreement_points`・`narrative`）完整保存到 `individual_reports`。
- 字段名固定且一致（符合 `schemas/novel-value-output.schema.json`）。
- 合成叙事（executive_summary等）只是辅助，不丢弃原始数据。

**评价 → 改写循环:**
```
評価 → revision_direction（次回の修正方向）→ リライト → 再評価
  → compare_reports.py で改善度確認 → 繰り返し
```

## 重要原则

- 评价者只给自己的专业领域的维度打分。专业之外返回 `null`。
- **彻底贯彻双重盲检**: 输入匿名，基准结构性。从评价场合中排除专有名词（作家名・作品名）。
- 预测不一致是评价者的义务。
- 评价不应外交化。坦率才是价值。
- 打分**有意从严**。高分罕见。**"能读"达不到50分。**
- 感伤扣分。评价的是**克制的审美**——通过不讲述而增强的情感。
- 编排者不指示评价者作出判断。只负责召集与整合。
- 合议不下判决。最终的价值判断由人来负责。
- **i18n 基准**: 多语言支持（en/ja/zh）是任何修改・变更的默认基准。新增或修改的评估者 prompt / schema / 报告模板必须通过语言机制（评估者智能体的 `-ja`/`-zh` 变体 / locale JSON / 镜像树）解析，面向用户的文本用运行语言生成。

## 安装

```bash
./install.sh            # グローバル: ~/.claude/agents/ + ~/.claude/skills/（どこからでも呼べる）
./install.sh --local    # プロジェクト: .claude/agents/ + .claude/skills/
./install.sh --uninstall
```
