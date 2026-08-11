**Language:** [English](README.md) | [日本語](README-ja.md) | 中文

# Novel Council Layer

**小说评议会（小説評議会）** —— 从海量故事中甄别出真正值得阅读的故事的多智能体价值评估层。

> **从「能够创作」走向「能够甄别」。**

---

## 为什么需要它

生成式AI已经能够大量生成各种类型的小说——网络小说、轻小说、纯文学、掌篇、AI小说。生成的成本已经无限趋近于零。

这个时代所追问的，不是「你能写出多少小说」。

> **能否从海量故事中甄别出真正值得阅读的故事。**

可以生成在平均水平上工整的小说。然而，真正有价值的故事并不存在于平均值之中。那些乍看笨拙却令人难忘的故事；当下不被理解、却能跨越时代留存的故事；以有意义的方式偏离既有类型的故事；改变读者认知的故事。

**Novel Council Layer** 正是为了「甄别故事的价值」而存在的基座。它作为**智慧评议会（Wisdom Council Layer）**的姊妹项目独立存在，同样采用「合议式的多声部评估」方法。不过，它所依据的判断标准，是专属于故事这一形式的独特标准。

---

## 核心命题：故事是在时间中被阅读的

通用的价值评估把内容当作一个「有价值的对象」来处理。独创性、美、市场性、思想深度——这些都是可以从作品中剥离出来的属性。

但小说并不是对象。**小说，是读者的内心在时间中展开的体验。** 同一本书，初读与重读会变成不同的书。年轻时读过的书，与年老时读的书，是两本不同的书。

> **故事的价值，存在于它被阅读的那段时间里。**

基于这一命题，我们提出故事评估所特有的**七个问题**。

### 故事评估的七个问题

| # | 问 | 对故事而言独特的原因 |
|---|-----|----------------------|
| 1 | **时间的质感** —— 这个故事如何运用读者的时间？ | 故事是时间的艺术。翻页的手是停住，还是放下书——这才是本质 |
| 2 | **信息的分配** —— 何时、向谁、揭示什么？ | 故事的力量不在于「讲述了什么」，而在于「何时揭示了什么」 |
| 3 | **叙事的距离** —— 由谁讲述，从多远讲述？ | 小说是「讲述」的艺术。视角与距离构成了与读者的关系 |
| 4 | **空白的設計** —— 读者需要填补的缝隙，是否被刻意设计？ | 小说在与读者的共同协作中完成。写作者通过「不说」来言说 |
| 5 | **文体与时间的契合** —— 文体是否控制了阅读的速度与感受？ | 文体决定阅读的节奏 |
| 6 | **重读的深度** —— 第二次阅读时，同一本书会变成另一本书吗？ | 故事的价值以复利方式累积 |
| 7 | **读后的位移** —— 读完之后，是否留下了「人生中有什么被动摇了」的感觉？ | 故事的结局，在读完时才真正开始 |

这七个问题，是无法用通用的价值评估来回答的。**「这个故事会如何改变读者的时间」**——正是这一追问，构成了 Novel Council Layer 所独自立足的判断标准。

---

## 核心哲学

- **故事是时间的艺术**：评估的对象是「被阅读的时间的品质」，而不是作品的属性。
- **多声部评估**：不是由单一的裁判者，而是由拥有不同视角的多位评估者合议。
- **不一致本身就是信号**：评估者之间的对立不作平均化处理，而是原样保存。
- **双重盲检**：从输入（作者名、作品名）与基准（专有名词）两方面隔绝名声，仅依据正文的结构进行评估。
- **评估重于生成**：甄别故事的价值，才是这一层的竞争领域。

## 角色分工（这一层的位置）

> **这一层为评估（Evaluation）而存在。作品的写作（Generation）则交由写作者、编辑与生成式AI承担。**

| 角色 | 负责方 |
|------|--------|
| **写作（Generation）** | 写作者、编辑、生成式AI（这一层**不写作**） |
| **评估（Evaluation）** | 这一层。以双重盲检只评估正文，并整理出用于下一轮改写（Rewrite）的材料（`weaknesses`、`improvement_suggestions`） |

评估结果**不是最终成果**。它是供写作者、编辑与生成式AI进行改写的**输入**。

---

## 双重盲检：隔绝对名声的锚定

为了让评估不被专有名词——作家名、作品名的名声——所牵动，这一层以**双重盲检**进行评估。这并不只是针对评估偏差的对策，而是守护**发现被埋没的杰作这一核心使命**的前提。

### 第一重盲检：输入的匿名化

> **评估仅基于正文。评估者在不知道作者名、作品名与文学史评价的状态下进行评价。**

用 `utils/anonymize.py` 去除作者名与作品名，只传递正文。诸如类型（genre）等必要的语境会传递，但不会传递任何会引导向名声的信息。

### 第二重盲检：结构性校准

> **评估的标准与校准，不是由专有名词，而是由结构性的描述来规定。**

| | 基于专有名词的标准（排除） | 基于结构性描述的标准（采用） |
|---|----------------------------|------------------------------|
| 示例 | 「像那部有名的变身故事那样的作品」 | 「角色的身体转变为别的事物，而这一转变以日常细节的方式被平静地描写，由此生出对身份认同的不安的结构」 |
| 效果 | 名声的权威转移到了评估上 | 模式本身成为评估的对象 |

即使文体泄露了作者的身份（文体识别），只要判断标准是结构性的，评估就会指向结构而非名声。

---

## 架构

```
小説（全文・冒頭＋要約・プロット）
        ↓
  匿名化（作者名・作品名を除去）※第一の盲検
        ↓
┌─────────────── 小説評議会 ───────────────┐
│  narrative-originality  plot-architecture │
│  anti-generic-story-filter    character-depth   │
│  emotional-power        prose-style       │
│  theme-resonance        world-building    │
│  narrative-technique    reader-experience │
│  ※各評価者は構造的基準で判断（第二の盲検）│
└────────────────────────────────────────────┘
        ↓
  Story Vector（10次元スコア）
        ↓
  Disagreement Map（不一致の保存）
        ↓
  Story Report（人間の書き手・編集者へ）
        ↓
  revision_direction（次回のリライト方向）
```

### 角色分工（实现）

**评估者是智能体（Agent），合议是技能（Skill）。** 10位评估者是以人格（persona）为基础的专业智能体（`agents/{name}.md`），在各自独立的上下文中进行评估。技能会共享同一个上下文，因此不适合进行独立评估；通过以子智能体（subagent）方式启动，可以使上下文彼此隔离。唯一的技能是合议编排器（story-council）。

---

## 目录结构

```
novel-council-layer/
├── CLAUDE.md                          # プロジェクト規約
├── README.md                          # 本ドキュメント
├── install.sh                         # グローバル/プロジェクトインストーラー
├── LICENSE                            # MIT
├── .gitignore
├── .claude-plugin/                    # プラグイン配布定義
│   ├── marketplace.json
│   └── plugin.json
├── agents/                            # 評価者エージェントの正本（10体）
│   ├── narrative-originality.md
│   ├── anti-generic-story-filter.md
│   ├── emotional-power.md
│   ├── plot-architecture.md
│   ├── character-depth.md
│   ├── prose-style.md
│   ├── theme-resonance.md
│   ├── world-building.md
│   ├── narrative-technique.md
│   └── reader-experience.md
├── schemas/
│   └── novel-value-output.schema.json # 物語評価者用出力スキーマ
├── skills/                            # スキルの正本（合議オーケストレーター）
│   └── story-council/SKILL.md         # 合議オーケストレーター
├── .claude/agents/                    # プロジェクト内検出用symlink（評価者）
├── .claude/skills/                    # プロジェクト内検出用symlink（合議）
├── references/                        # 物語評価の理論基盤
│   ├── evaluator-taxonomy.md          # 評価者分類と次元の境界
│   ├── scoring-strictness.md          # 厳格スコアリング基準（小説版）
│   ├── narrative-time.md              # テーゼの理論的系譜（出典の記録）
│   ├── meaning-of-novels.md           # 物語の意味と評価の基準（構造的）
│   ├── blind-evaluation.md            # 二重の盲検
│   ├── structural-calibration.md      # 構造的キャリブレーション（固有名詞を使わない基準）
│   ├── benchmark-50novels.md          # 盲検ベンチマーク（50冊・ラベルは照合時のみ）
│   └── revision-loop.md               # 評価→リライトループ
├── examples/                          # 小説サンプル（評価→リライトループ）
│   ├── README.md
│   └── novel-sample/
└── utils/
    ├── anonymize.py                   # 入力の匿名化（第一の盲検の前処理）
    ├── validate_output.py             # 出力バリデーション（--json で機械可読。合議の自動リトライに利用）
    ├── render_report.py               # 視覚化（コンソール / Markdown）
    └── compare_reports.py             # 改訂前後の比較
```

---

## 使用方法

### 安装

**全局（可随处调用）：**

```bash
./install.sh
```

会在 `~/.claude/agents/`（评估者智能体）和 `~/.claude/skills/`（合议技能）下创建符号链接（symlink），从而可以在任何项目中使用。

**仅限项目：**

```bash
./install.sh --local
```

### 调用流程（三个阶段）

| 级别 | 调用什么 | 返回什么 | 用途 |
|------|----------|----------|------|
| **1** | **1位**评估者 | 单一维度的评估 JSON | 只想确认某个特定视角 |
| **2** | **合议（auto）** | 整合后的 Story Report（3～5 个维度） | 依据领域高效地进行综合评价 |
| **3** | **合议（full）** | 填满全部 10 个维度的完整 Story Report | 从一开始就让所有人一次性评估 |

#### 级别 1：调用一位评估者

评估者以**子智能体**方式启动。

```
Agent tool, subagent_type: plot-architecture
Prompt: {"content": "...", "domain": "genre-fiction"}
```

示例：
- 只确认情节（plot）设计 → `plot-architecture`
- 检查是否带有 AI 味（平庸） → `anti-generic-story-filter`
- 只确认文体的质量 → `prose-style`

※ 以插件方式运行时使用作用域名称（例如：`novel-council-layer:plot-architecture`），在项目内则使用原名启动。

#### 级别 2：调用合议（推荐）

当你想从多个视角进行综合评价时使用。合议会判定故事的子领域，让评估者进行独立评估，并返回整合后的 Story Report。

```
Skill: story-council
Args: {"content": "...", "domain": "pure-literature"}
```

#### 级别 3：一次性调用全部评估者

```
Skill: story-council
Args: {"content": "...", "domain": "genre-fiction", "mode": "full"}
```

### 模式一览

合议（story-council）有以下模式。启动时也会显示相关说明。

| 项目 | 选项 | 说明 |
|------|------|------|
| **输入形式** `content_type` | `text`（默认）/ `plot` | `plot` 也可用于**梗概、构思**的评估（由 7 位评估。prose-style、narrative-technique、reader-experience 不参与召集） |
| **召集范围** `mode` | `auto`（默认）/ `full` | `auto` 依据领域召集 **3～5 位**，`full` 召集适用范围内的**全体**（text：10 位 / plot：7 位） |
| **迭代** `iteration` | `confirm`（默认）/ `persistent` | `confirm` 在每一轮确认修正方向，`persistent` 固定方向进行打磨 |
| **领域** `domain` | `pure-literature` / `genre-fiction` / `light-novel` / `short-story` / `historical-fiction` | 故事的子领域。可省略（由合议判定） |

**梗概评估的示例（plot 模式・全部 7 位）：**
```
Skill: story-council
Args: {"content": "あらすじ...", "content_type": "plot", "domain": "genre-fiction", "mode": "full"}
```

### 输出的验证与自动重试

合议技能用 `utils/validate_output.py --json` 对每位评估者的输出进行**确定性验证**。由于它返回机器可读的结果（`{"valid": bool, "kind": str, "errors": [string]}`），因此不依赖 LLM 的目视验证（不够精确）。

```bash
python utils/validate_output.py --json output.json
```

未通过时，对同一评估者**最多重新启动 3 次**（在反馈中包含错误内容）；3 次后仍未通过，则明确记录到 `excluded_evaluators` 中，标记为 `"JSON validation failed after 3 retries"`。**禁止静默丢弃。**

---

## 评估者一览

10 位评估者都是**子智能体**（`agents/{name}.md`）。每位评估者只对自己的维度打分，并与相邻维度保持明确的边界。

| 评估者（智能体名） | 核心问题 | 维度 |
|--------------------|----------|------|
| Narrative Originality（`narrative-originality`） | 故事的**形式**是否对既有模式作出了有意义的偏离？ | narrative_originality |
| Anti-Generic Story Filter（`anti-generic-story-filter`） | 是否堕入了俗套、类型与预定和谐？ | quality |
| Emotional Power（`emotional-power`） | 能否打动读者的心、并烙印在记忆中？ | emotional_power |
| Plot Architecture（`plot-architecture`） | 因果与信息的揭示是否设计精巧？ | plot_architecture |
| Character Depth（`character-depth`） | 人物是否作为活生生的人站立起来？ | character_depth |
| Prose Style（`prose-style`） | 文体是否作为语言之音乐发挥作用？ | prose_style |
| Theme Resonance（`theme-resonance`） | 主题是否深刻、一贯，并触及存在的追问？ | theme_resonance |
| World Building（`world-building`） | 舞台是否具有创造性，并具备内在一致性？ | world_building |
| Narrative Technique（`narrative-technique`） | 叙事的距离与时间操作是否强化了故事？ | narrative_technique |
| Reader Experience（`reader-experience`） | 作为阅读体验，是否令人沉浸、完满，并引人重读？ | reader_experience |

### 合议编排器：story-council

判定故事的子领域，召集并整合评估者。是唯一生成保存了不一致的 Story Report 的技能。

---

## 评分：严格标准（小说版）

这个评议会的目标不是「称赞好的小说」，而是**「甄别出值得阅读的故事」**。评分是刻意严格的。

| 区间 | 含义（对应到小说） | 频度预期 |
|------|--------------------|----------|
| 0-10 | 存在严重缺陷。不能作为故事成立 | 罕见 |
| 11-30 | 薄弱。只是在消耗读者的时间 | 较多 |
| 31-50 | 稳妥、平庸。读得下去，但被阅读的时间没有改变任何东西 | **占分布的最大比重** |
| 51-70 | 真正的好。被阅读的时间是一段有价值的体验 | 较为罕见 |
| 71-90 | 例外级。读完之后，人生中有什么被触动了 | 罕见 |
| 91-100 | 载入文学史 | 几乎不会给出 |

**小说特有的判断铁律：**
1. **以「被阅读的时间」来判断**。不是依据写作者的意图，而是作为读者的体验来追问「这段时间是否有价值」。
2. 在给出分数前扪心自问：「这真的是一段超过 50 的阅读体验吗？读完之后，会留下什么吗？」若有疑虑就往低打。**仅凭「读得下去」，够不到 50。**
3. 平庸会落入低分。「读起来轻松又稳妥的娱乐作品」在 20-40 分区间。
4. 感伤要扣分。评价**克制的美学**——因不说出口而愈发强烈的感情。
5. 意义与美，要用**体验**而非说明来评价。
6. 输入仅限于正文（第一重盲检）。对名声的锚定，是评估中最大的偏差。
7. 基准是结构性的（第二重盲检）。追问的不是「它像不像那部有名的作品」，而是「这个结构能否创造出有价值的时间」。

---

## 分类模型

以「当前价值 × 潜在价值」为两轴的模型。

```
             Hidden Potential
                  ↑
   Discovery Target   Innovation
────────────────┼──────────────────→  Current Value
   Low Signal        Current Success
```

| 分类 | 对故事的含义 |
|------|--------------|
| **Discovery Target** | 当下被埋没，但随着读者或时代的变化价值会上升的故事 |
| **Innovation** | 现在与未来都价值很高的故事 |
| **Current Success** | 当下被阅读，但潜在价值较低的故事 |
| **Low Signal** | 现阶段没有任何价值迹象的故事 |

※ 分类从正文的结构中推导出来，不依赖文学史上的专有名词。

---

## 评估 → 改写的循环

这一层的评估结果**不是最终成果**。它是供写作者、编辑与生成式AI进行改写的**输入**。

```
① 執筆（v1）
    ↓
② 評価（story-council / mode:full）※二重の盲検
    ↓
③ revision_direction（次回の修正方向）を確認
    ↓
④ リライト（書き手 or 生成AI）
    ↓
⑤ 再評価
    ↓
⑥ 比較（compare_reports.py で改善度を確認）
    ↓
⑦ 目標に達するか頭打ちになるまで繰り返す
```

每位评估者的 `weaknesses`、`improvement_suggestions`、`expected_disagreement_points` 都会被保存，作为具体改写指示的素材。

---

## 成果的验证：盲检基准（50 本）

这一计划最大的赌注是「这套系统是否真的能甄别出故事的价值」。为了验证这一点，我们设计了一个基于**文学史上的 50 本作品**的**盲检基准（Benchmark）**。

### 步骤（双重盲检的运用）

1. 将各作品的**开头＋梗概**作为**去除了作者名、作品名**的匿名文本输入（第一重盲检）
2. 系统以 10 位评估者、依据**结构性标准**（第二重盲检）进行评估，并推导出分类
3. 仅在评估结束**之后**，才与文学史标签（ground truth）进行对照，测量一致率

```
入力: 「ある男が朝目覚めると、身体が別のものへ変容していた。家族は…」（匿名・構造的記述）
システムの盲検分類: Discovery Target / Innovation
評価後の照合: 文学史ラベル = Innovation
一致: ✓
```

### 选定标准（4 个象限 × 类型）

| 分类 | 选定标准 |
|------|----------|
| **Discovery Target** | 生前不被待见、评价低，但在后世被重新评价为杰作的作品群 |
| **Innovation** | 从发表时起至今一直受到一贯评价的作品群 |
| **Current Success** | 在同时代获得高评价、成为畅销书，但未能流传后世的作品群 |
| **Low Signal** | 发表之后几乎无人阅读、也无人评价的作品群 |

### 目标值

- **一致率 70%**（达成这一目标，是开启收费服务的条件）
- 分析不一致发生在何处，并将其反馈到对每位评估者严苛程度的调整（校准）中

---

## 路线图

- **Phase 1**：Novel Evaluation Core——10 位评估者智能体（以结构性维度与权重实现）+ 双重盲检（anonymize + 结构性校准）+ 合议技能（story-council）+ Story Vector + Story Report
- **Phase 2**：盲检基准（验证 50 本作品，以一致率 70% 为目标）→ 校准调整。面向个人作家的付费诊断（Freemium）上线
- **Phase 3**：Debate Engine（评估者之间的多轮辩论）+ 投稿平台的 PoC（以一致率 65%、工数削减 40% 为目标）
- **Phase 4**：Meta Value Layer（包括 Bias Detection、Evaluation Critic——监视锚定偏差与专有名词混入）+ 收费化（SaaS）
- **Phase 5**：长篇模式（逐章阅读全文的评估流程）

详细规格与设计请参照 [novel-council-strategy.md](./novel-council-strategy.md)。

---

## 许可证

MIT License — Copyright (c) 2026 GL-Kageyama

## Core Statement

> 在大量的故事中，能甄别出多少有价值的故事。

Novel Council Layer，正是为此而生的故事价值发现基础设施。

故事活在读者的时间之中。应当被甄别出的价值，也在那段时间里。这一层不是把作品当作对象，而是当作**某人生命中的时间**来评估。隐去作者名与作品名，只读正文。而且，在判断的标准上，放置的也不是名声，而是**结构**。当那段时间——对某一位读者而言，足以成为人生的一部分——触及意义、美与感情时，它就是应当被甄别出的价值。
