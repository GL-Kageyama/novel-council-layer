**Language:** English | [日本語](README-ja.md) | [中文](README-zh.md)

# Novel Council Layer

<p align="center">
  <img src="assets/repo-hero.png" width="100%" alt="Novel Council Layer">
</p>

**小説評議会 (Novel Council)** — a multi-agent value evaluation layer that picks out, from among a flood of stories, the stories truly worth reading.

> **From "creating" to "discerning."**

---

## Why It Is Needed

Generative AI can now mass-produce novels in every genre: web novels, light novels, pure literature, short-shorts, AI novels. The cost of generation has approached zero.

What this era demands is not "how many novels you can write."

> **Whether you can discern, from among a flood of stories, the stories truly worth reading.**

You can generate novels that are well-formed on average. But truly valuable stories do not exist in the average. Stories that look clumsy at first glance yet are unforgettable. Stories not understood today yet that endure across the ages. Stories that deviate meaningfully from existing types. Stories that change the reader's perception.

**Novel Council Layer** is the foundation for this act of "discerning a story's value." It stands independent as a sister project of the **Wisdom Council Layer**, adopting the same method of "multi-voiced evaluation by council." Its criteria, however, are its own, specific to the form of narrative.

---

## Core Thesis: Stories Are Read in Time

Generic value evaluation treats content as a single "valuable object." Originality, beauty, marketability, philosophical depth—these are attributes that can be cut out of a work.

But a novel is not an object. **A novel is an experience that unfolds in time within the reader's inner self.** Even the same book becomes a different book on first and second reading. A book read in youth and a book read in old age are different books.

> **A story's value lies in the time in which it is read.**

From this thesis we derive **seven questions** specific to narrative evaluation.

### The Seven Questions of Narrative Evaluation

| # | Question | Why It Is Specific to Narrative |
|---|----------|--------------------------------|
| 1 | **Quality of Time** — How does this story use the reader's time? | Narrative is the art of time. Whether the hand stops turning pages or sets the book down is the essence |
| 2 | **Distribution of Information** — What is revealed, when, and to whom? | A story's power lies not in "what is told" but in "what is revealed, and when" |
| 3 | **Narrative Distance** — Who narrates, and from what distance? | The novel is the art of "telling." Point of view and distance create the relationship with the reader |
| 4 | **Design of Gaps** — Are the gaps the reader must fill deliberately designed? | A novel is completed through collaboration with the reader. The writer speaks by not speaking |
| 5 | **Alignment of Style and Time** — Does the prose control the pace and feel of reading? | Prose style sets the rhythm of reading |
| 6 | **Depth of Rereading** — On a second reading, does the same book become a different book? | A story's value accrues with compound interest |
| 7 | **Post-Reading Displacement** — After reading, does a sense remain that something in life has moved? | A story's ending begins after reading |

These seven questions cannot be answered by generic value evaluation. The question—**"How does this story change the reader's time?"**—is precisely the criterion on which Novel Council Layer stands alone.

---

## Core Philosophy

- **Narrative is the art of time**: The object of evaluation is the "quality of the time read," not the attributes of the work.
- **Multi-voiced evaluation**: A council of multiple evaluators holding different viewpoints, rather than a single judge.
- **Disagreement is the signal**: Conflicts among evaluators are not averaged out but preserved as they are.
- **Double blinding**: Cut off reputation from both the input (author name, work title) and the criteria (proper nouns), and evaluate only on the structure of the text.
- **Evaluation over generation**: Discerning a story's value is this layer's competitive arena.

## Division of Roles (Where This Layer Stands)

> **This layer exists for Evaluation. The writing of works (Generation) is left to writers, editors, and generative AI.**

| Role | Responsibility |
|------|----------------|
| **Writing (Generation)** | Writers, editors, generative AI (this layer does **not** write) |
| **Evaluation** | This layer. With double blinding it evaluates only the text and prepares the material for the next rewrite (`weaknesses` / `improvement_suggestions`) |

The evaluation result is **not a final deliverable**. It is **input** for writers, editors, and generative AI to rewrite.

---

## Double Blinding: Shielding Against Anchoring on Reputation

To keep evaluation from being pulled by proper nouns—the reputations of authors and works—this layer evaluates with **double blinding**. This is not merely a countermeasure against distorted evaluation. It is the precondition for protecting the core mission: **the discovery of buried masterpieces**.

### First Blinding: Anonymizing the Input

> **Evaluation is based on the text alone. Evaluators assess without knowing the author's name, the work's title, or its standing in literary history.**

`utils/anonymize.py` removes the author's name and the work's title, passing only the text. Necessary context such as genre is passed, but no information that would steer toward reputation is given.

### Second Blinding: Structural Calibration

> **The criteria and calibration of evaluation are defined not by proper nouns but by structural descriptions.**

| | Criteria via proper nouns (excluded) | Criteria via structural description (adopted) |
|---|--------------------------------------|----------------------------------------------|
| Example | "A work like the famous transformation story" | "A structure in which a character's body transforms into something else, and the transformation is depicted flatly as an everyday detail, thereby generating anxiety about identity" |
| Effect | The authority of reputation transfers to the evaluation | The pattern itself becomes the object of evaluation |

Even if the prose style betrays the author (stylometry), as long as the criteria are structural, evaluation is directed at structure rather than reputation.

---

## Architecture

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

### Division of Roles (Implementation)

**Evaluators are agents; the council is a skill.** The ten evaluators are persona-based specialist agents (`agents/{name}.md`) that evaluate in independent contexts. A skill shares the same context and is therefore unsuited to independent evaluation; launching the evaluators as subagents isolates their contexts. The council orchestrator (story-council) is the only skill.

---

## Directory Structure

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

## Usage

### Installation

**Global (callable from anywhere):**

```bash
./install.sh
```

Symlinks are created in `~/.claude/agents/` (evaluator agents) and `~/.claude/skills/` (council skill), making them available in any project.

**Project-scoped:**

```bash
./install.sh --local
```

### The Call Flow (Three Levels)

| Level | What You Call | What It Returns | Use Case |
|-------|---------------|-----------------|----------|
| **1** | A **single** evaluator | A single-dimension evaluation JSON | To check only a specific viewpoint |
| **2** | **Council (auto)** | An integrated Story Report (3–5 dimensions) | For an efficient overall assessment according to the domain |
| **3** | **Council (full)** | A complete Story Report with all 10 dimensions filled | To have everyone evaluate at once from the start |

#### Level 1: Call a Single Evaluator

Evaluators are launched as **subagents**.

```
Agent tool, subagent_type: plot-architecture
Prompt: {"content": "...", "domain": "genre-fiction"}
```

Examples:
- Check only the plot design → `plot-architecture`
- Check for AI-likeness (mediocrity) → `anti-generic-story-filter`
- Check only the quality of the prose → `prose-style`

Note: When running as a plugin, launch with the scope name (e.g. `novel-council-layer:plot-architecture`); inside the project, launch with the bare name.

#### Level 2: Call the Council (Recommended)

For an overall assessment from multiple perspectives. The council determines the narrative subdomain, has evaluators assess independently, and returns an integrated Story Report.

```
Skill: story-council
Args: {"content": "...", "domain": "pure-literature"}
```

#### Level 3: Call All Evaluators at Once

```
Skill: story-council
Args: {"content": "...", "domain": "genre-fiction", "mode": "full"}
```

### List of Modes

The council (story-council) has the following modes. A guide is also shown at launch.

| Item | Options | Description |
|------|---------|-------------|
| **Input format** `content_type` | `text` (default) / `plot` | `plot` also allows evaluating from an **outline or concept** (evaluated by 7. prose-style, narrative-technique, and reader-experience are not convened) |
| **Convening scope** `mode` | `auto` (default) / `full` | `auto` convenes **3–5** evaluators according to the domain; `full` convenes **all** applicable ones (text: 10 / plot: 7) |
| **Iteration** `iteration` | `confirm` (default) / `persistent` | `confirm` confirms the revision direction each turn; `persistent` fixes the direction and polishes |
| **Domain** `domain` | `pure-literature` / `genre-fiction` / `light-novel` / `short-story` / `historical-fiction` | The story's subdomain. Optional (the council determines it) |

**Example of evaluating an outline (plot mode, all 7):**
```
Skill: story-council
Args: {"content": "あらすじ...", "content_type": "plot", "domain": "genre-fiction", "mode": "full"}
```

### Output Validation and Automatic Retry

The council skill **deterministically validates** each evaluator's output with `utils/validate_output.py --json`. Because it returns machine-readable results (`{"valid": bool, "kind": str, "errors": [string]}`), it does not rely on visual LLM inspection (which is imprecise).

```bash
python utils/validate_output.py --json output.json
```

If an output fails, the same evaluator is **restarted up to 3 times** (with the error content included in the feedback); if it still fails after 3 attempts, it is explicitly recorded in `excluded_evaluators` as `"JSON validation failed after 3 retries"`. **Silent drops are prohibited.**

---

## List of Evaluators

The ten evaluators are **subagents** (`agents/{name}.md`). Each scores only its own dimension and maintains a clear boundary from adjacent dimensions.

| Evaluator (agent name) | Core Question | Dimension |
|------------------------|---------------|-----------|
| Narrative Originality（`narrative-originality`） | Does the story's **form** deviate meaningfully from existing patterns? | narrative_originality |
| Anti-Generic Story Filter（`anti-generic-story-filter`） | Has it fallen into cliché, type, or predictable harmony? | quality |
| Emotional Power（`emotional-power`） | Does it move the reader's heart and lodge in memory? | emotional_power |
| Plot Architecture（`plot-architecture`） | Are causality and information disclosure skillfully designed? | plot_architecture |
| Character Depth（`character-depth`） | Do the characters stand up as living people? | character_depth |
| Prose Style（`prose-style`） | Does the prose function as music of words? | prose_style |
| Theme Resonance（`theme-resonance`） | Is the theme deep, consistent, and touching on questions of existence? | theme_resonance |
| World Building（`world-building`） | Is the setting creative and internally coherent? | world_building |
| Narrative Technique（`narrative-technique`） | Do narrative distance and time manipulation strengthen the story? | narrative_technique |
| Reader Experience（`reader-experience`） | As a reading experience, does it immerse, complete, and invite rereading? | reader_experience |

### Council Orchestrator: story-council

Determines the narrative subdomain and convenes and integrates evaluators. The only skill that produces a Story Report that preserves disagreement.

---

## Scoring: Strict Criteria (Novel Edition)

The purpose of this council is not "to praise good novels" but **"to discern stories worth reading."** Scoring is deliberately strict.

| Band | Meaning (as applied to novels) | Expected frequency |
|------|--------------------------------|--------------------|
| 0-10 | Severe defect. Does not function as a story | Rare |
| 11-30 | Weak. Merely takes the reader's time | Somewhat common |
| 31-50 | Safe and mediocre. Readable, but the time spent reading changed nothing | **Largest share of the distribution** |
| 51-70 | Truly good. The time spent reading was a valuable experience | Somewhat rare |
| 71-90 | Exceptional. After reading, something in life has moved | Rare |
| 91-100 | Earns a place in literary history | Almost never given |

**Iron rules of judgment specific to novels:**
1. **Judge by "time read."** Ask, as the reader's experience rather than the writer's intent, "Was this time worth it?"
2. Before assigning a score, ask yourself: "Is this really a reading experience above 50? Does anything remain after reading?" When in doubt, score low. **"Readable" does not reach 50.**
3. Mediocrity falls to a low score. "Easy-to-read, safe entertainment" sits in the 20-40 range.
4. Sentimentality is penalized. Evaluate the **aesthetic of restraint**—emotion that grows stronger by not being said.
5. Meaning and beauty are evaluated through **experience**, not explanation.
6. The input is the text alone (first blinding). Anchoring on reputation is the greatest distortion of evaluation.
7. The criteria are structural (second blinding). Ask not "Does it resemble a famous work?" but "Does this structure produce valuable time?"

---

## Classification Model

A two-axis model of current value × potential value.

```
             Hidden Potential
                  ↑
   Discovery Target   Innovation
────────────────┼──────────────────→  Current Value
   Low Signal        Current Success
```

| Classification | Meaning for Stories |
|----------------|---------------------|
| **Discovery Target** | Stories currently buried, whose value rises as readers or the era change |
| **Innovation** | Stories of high value now and in the future |
| **Current Success** | Stories read today but with low potential value |
| **Low Signal** | Stories with no sign of value at present |

Note: The classification is derived from the structure of the text and does not depend on the proper nouns of literary history.

---

## The Evaluation → Rewrite Loop

The evaluation result of this layer is **not a final deliverable**. It is **input** for writers, editors, and generative AI to rewrite.

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

Each evaluator's `weaknesses`, `improvement_suggestions`, and `expected_disagreement_points` are saved as material for concrete rewrite instructions.

---

## Verifying the Track Record: Blind Benchmark (50 Books)

The project's biggest bet is "can this system actually discern a story's value?" To verify this, we design a **blind benchmark** using **50 books from literary history**.

### Procedure (Applying Double Blinding)

1. Each work's **opening + summary** is entered as anonymized text with the **author's name and title removed** (first blinding)
2. The system evaluates with the ten evaluators under **structural criteria** (second blinding) and derives a classification
3. Only **after** evaluation concludes are the results matched against the literary-history labels (ground truth) to measure the agreement rate

```
入力: 「ある男が朝目覚めると、身体が別のものへ変容していた。家族は…」（匿名・構造的記述）
システムの盲検分類: Discovery Target / Innovation
評価後の照合: 文学史ラベル = Innovation
一致: ✓
```

### Selection Criteria (4 Quadrants × Genre)

| Classification | Selection Criteria |
|----------------|--------------------|
| **Discovery Target** | Works that were neglected or underrated in their lifetime but later re-evaluated as masterpieces |
| **Innovation** | Works consistently evaluated highly from their release to the present |
| **Current Success** | Works highly rated and bestsellers in their own time but that did not endure |
| **Low Signal** | Works that, after release, were barely read and barely evaluated |

### Target Values

- **70% agreement** (achieving this is the condition for commercialization)
- Analyze where disagreement occurs and feed it back into adjusting each evaluator's strictness (calibration)

---

## Roadmap

- **Phase 1**: Novel Evaluation Core — the ten evaluator agents (implemented with structural dimensions and weights) + double blinding (anonymize + structural calibration) + the council skill (story-council) + Story Vector + Story Report
- **Phase 2**: Blind benchmark (verify 50 books, targeting 70% agreement) → calibration adjustment. Launch of paid diagnostics for individual writers (freemium)
- **Phase 3**: Debate Engine (multi-turn debate among evaluators) + a submission-platform PoC (targeting 65% agreement and 40% labor savings)
- **Phase 4**: Meta Value Layer (including Bias Detection and Evaluation Critic—monitoring anchoring bias and proper-noun leakage) + commercialization (SaaS)
- **Phase 5**: Full-length mode (an evaluation process that reads the entire text chapter by chapter)

See [novel-council-strategy.md](./novel-council-strategy.md) for detailed specifications and design.

---

## License

MIT License — Copyright (c) 2026 GL-Kageyama

## Core Statement

> Among a flood of stories, how many valuable ones can you discern?

Novel Council Layer is the narrative-value discovery infrastructure for that purpose.

A story lives within the reader's time. The value to be discerned lies in that time as well. This layer evaluates a work not as an object but as **time within someone's life**. It conceals both the author's name and the work's title and reads only the text. And at the heart of its judgment it places, not reputation, but **structure**. When that time touches meaning, beauty, and emotion—such that for some reader it becomes part of their life—that is value worth discerning.
