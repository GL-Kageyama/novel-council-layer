**Language:** [English](../evaluator-taxonomy.md) | [日本語](../ja/evaluator-taxonomy.md) | 中文
# Evaluator Taxonomy（评估者分类与维度边界）


Novel Council Layer 的评价者群并非由单一价值观构成，而是由**多个独立的视角**构成。本文档定义各评价者的定位、负责的子领域，以及与其他评价者之间的维度边界。

## 评价者的分类

评价者分为3层。

### 第1层：当前价值分析（Current Value Analysis）

评价故事在**当前时点**具有多大的阅读价值。

| 评价者 | 视角 | 负责子领域 |
|--------|------|-----------------|
| Anti-Generic Story Filter | 陈词滥调・类型化・预定调和的检测（跨领域） | 全部子领域 |
| Narrative Originality | 形式・前提的偏离 | 全部子领域 |
| Emotional Power | 情感的力量・读后的位移 | pure-literature, genre-fiction, short-story |
| Plot Architecture | 因果・信息揭示・伏笔 | genre-fiction, light-novel |
| Character Depth | 人物的深度・内心冲突 | light-novel, historical-fiction |
| Prose Style | 文体・文字的音乐 | pure-literature, short-story |
| World Building | 世界观的创造性与一致性 | genre-fiction, light-novel, historical-fiction |
| Narrative Technique | 叙事的距离・时间操作 | pure-literature, short-story |
| Reader Experience | 阅读体验・沉浸 | genre-fiction, light-novel |

### 第2层：潜在价值发现（Hidden Potential Discovery）

发现当前尚未被评价的**未来的可能性**。

| 评价者 | 视角 |
|--------|------|
| Theme Resonance | 主题的深度・读后留下的意义・重读的深度 |

### 第3层：元层（Meta Layer）

动摇评价前提本身。

| 评价者 | 视角 |
|--------|------|
| Anti-Generic Story Filter | 平庸的去除（对所有评价者横向起作用） |

※ Theme Resonance 同时贡献于当前价值（主题一致性）与潜在价值（读后的意义・重读）。作为第2层处理。

## 各评价者的核心之问

| 评价者 | 核心问题 |
|--------|----------|
| Narrative Originality | 故事的**形式**是否对既有模式做出了有意义的偏离？ |
| Anti-Generic Story Filter | 是否堕入陈词滥调・类型化・预定调和？ |
| Emotional Power | 能否打动读者的心并铭刻于记忆？ |
| Plot Architecture | 因果与信息揭示是否设计得巧妙？ |
| Character Depth | 人物是否作为活生生的人站立起来？ |
| Prose Style | 文体是否作为文字的音乐发挥作用？ |
| Theme Resonance | 主题是否深刻、一贯，并触及存在的追问？ |
| World Building | 舞台是否富有创造性，且具有内在一致性？ |
| Narrative Technique | 叙事的距离与时间操作是否强化了故事？ |
| Reader Experience | 作为阅读体验，是否沉浸、完整，并引人重读？ |

## 与相邻维度的边界（重复的整理）

| 维度对 | 边界的定义 |
|----|-----------|
| **narrative_originality** × **theme_resonance** | 独创性看「形式的偏离」，主题看「内容的深度与意义」。两者独立运作 |
| **plot_architecture** × **narrative_technique** | 情节看「什么在何时被揭示」，技法看「由谁、如何讲述」 |
| **emotional_power** × **reader_experience** | 情感看「心灵的位移」，阅读体验看「阅读行为的质量」 |
| **prose_style** × **reader_experience** | 文体看「文字的音乐」，阅读体验看「整体体验」 |
| **theme_resonance** × **emotional_power** | 主题看「读后留下的阐释・意义」，情感看「阅读中心灵的位移」 |
| **anti-generic-story-filter** × **narrative_originality** | 反平庸评价「是否俗套」，独创性评价「偏离的意义」 |

## 评价者之间的关系

### 互补关系

- **Plot Architecture ↔ Character Depth**: 优秀的故事中，情节与人物两者相互咬合。只有情节或只有人物的故事，两者都是脆弱的。
- **Prose Style ↔ Emotional Power**: 克制的美学——不吐露一切的文体——深化情感。文体与情感分开看待，但克制跨越两者。
- **Theme Resonance ↔ Reader Experience**: 读后留下的意义（主题）唯有在阅读体验（沉浸）存在时才得以成立。

### 对立结构

这种对立**不应被平均化**。相反，冲突是价值的重要征兆。

```
高い形式の独創 + 低い読みやすさ = 未来の傑作の可能性
高いプロット設計 + 低いテーマの深さ = 面白いが残らない可能性
高い感情の力 + 低い凡庸性除去 = 感傷の危険
```

## 与 Story Vector 的对应

各评价者对 Story Vector 的特定维度做出贡献（其他维度为 null）。

```
Story Vector:
[narrative_originality, quality, emotional_power, plot_architecture,
 character_depth, prose_style, theme_resonance, world_building,
 narrative_technique, reader_experience]
```

## 合议中的评价者选择

合议编排器（story-council）根据子领域选择评价者。详见 `skills/story-council/SKILL.md` 中的选择矩阵。
