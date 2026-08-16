**Language:** English | [日本語](ja/evaluator-taxonomy.md) | [中文](zh/evaluator-taxonomy.md)
# Evaluator Taxonomy (Categorization of Evaluators and Boundaries of Dimensions)


The evaluators of the Novel Council Layer are composed not of a single value system but of **multiple independent perspectives**. This document defines each evaluator's positioning, the subdomains they cover, and the boundaries of dimensions with other evaluators.

## Evaluator Categories

Evaluators are divided into three layers.

### Layer 1: Current Value Analysis

Assesses how much reading value a narrative holds **at the present moment**.

| Evaluator | Perspective | Covered Subdomains |
|--------|------|-----------------|
| Anti-Generic Story Filter | Detection of clichés, stock types, and pre-established harmony (cross-cutting) | All subdomains |
| Narrative Originality | Deviation in form and premise | All subdomains |
| Emotional Power | Power of emotion; displacement after reading | pure-literature, genre-fiction, short-story |
| Plot Architecture | Causality, information disclosure, foreshadowing | genre-fiction, light-novel |
| Character Depth | Depth of characters; inner conflict | light-novel, historical-fiction |
| Prose Style | Prose style; the music of words | pure-literature, short-story |
| World Building | Creativity and consistency of the worldview | genre-fiction, light-novel, historical-fiction |
| Narrative Technique | Narrative distance; manipulation of time | pure-literature, short-story |
| Reader Experience | Reading experience; immersion | genre-fiction, light-novel |
| Admiration | The involuntary "wow" — surpassing prediction while earning inevitability | All subdomains |

### Layer 2: Hidden Potential Discovery

Discovers **future potential** that is not currently evaluated.

| Evaluator | Perspective |
|--------|------|
| Theme Resonance | Depth of theme; meaning that remains after reading; depth of re-reading |

### Layer 3: Meta Layer

Shakes the very premises of evaluation.

| Evaluator | Perspective |
|--------|------|
| Anti-Generic Story Filter | Removal of mediocrity (works cross-cuttingly across all evaluators) |

※ Theme Resonance contributes to both current value (thematic consistency) and hidden potential (meaning after reading; re-reading). It is treated as Layer 2.

## Core Question of Each Evaluator

| Evaluator | Core Question |
|--------|----------|
| Narrative Originality | Does the narrative's **form** deviate meaningfully from existing patterns? |
| Anti-Generic Story Filter | Has it fallen into clichés, stock types, or pre-established harmony? |
| Emotional Power | Does it move the reader's heart and stay fixed in memory? |
| Plot Architecture | Are causality and information disclosure skillfully designed? |
| Character Depth | Does the character stand up as a living person? |
| Prose Style | Does the prose function as the music of words? |
| Theme Resonance | Is the theme deep, consistent, and does it touch on questions of existence? |
| World Building | Is the setting creative and internally consistent? |
| Narrative Technique | Do narrative distance and time manipulation strengthen the story? |
| Reader Experience | As a reading experience, is it immersive, complete, and inviting of re-reading? |
| Admiration | Does it make the reader exclaim "interesting!" with admiration — by exceeding prediction while earning inevitability? |

## Boundaries with Adjacent Dimensions (Resolving Overlap)

| Pair | Boundary Definition |
|----|-----------|
| **narrative_originality** × **theme_resonance** | Originality looks at "deviation in form"; theme looks at "depth and meaning of content". They move independently |
| **plot_architecture** × **narrative_technique** | Plot looks at "what is revealed when"; technique looks at "who tells, and how" |
| **emotional_power** × **reader_experience** | Emotion looks at "displacement of the heart"; reading experience looks at "the quality of the act of reading" |
| **prose_style** × **reader_experience** | Prose style looks at "the music of words"; reading experience looks at "the overall experience" |
| **theme_resonance** × **emotional_power** | Theme looks at "the interpretation and meaning that remain after reading"; emotion looks at "displacement of the heart during reading" |
| **anti-generic-story-filter** × **narrative_originality** | Anti-generic evaluates "whether it is mundane"; originality evaluates "the meaning of the deviation" |
| **admiration** × **plot_architecture** | Plot looks at the machinery (what is revealed when); admiration looks at the reaction that machinery produces (surprise + inevitability = "wow") |
| **admiration** × **reader_experience** | Reader experience looks at the quality of the whole reading act; admiration looks at the single peak moment of "wow" |
| **admiration** × **emotional_power** | Emotion looks at the heart being moved; admiration looks at the involuntary exclamation (the cognitive "wow", not sentiment) |
| **admiration** × **narrative_originality** | Originality looks at deviation of form; admiration looks at the peak moment of surpassing prediction |

## Relationships Between Evaluators

### Complementary Relationships

- **Plot Architecture ↔ Character Depth**: In excellent stories, plot and characters interlock. Stories with only a plot or only characters are fragile in either case.
- **Prose Style ↔ Emotional Power**: The aesthetics of restraint — a prose style that does not say everything — deepens emotion. Prose style and emotion are viewed independently, but restraint spans both.
- **Theme Resonance ↔ Reader Experience**: Meaning that remains after reading (theme) comes into being only through the reading experience (immersion).

### Tension Structure

This tension should **not be averaged out**. Rather, conflict is an important sign of value.

```
高い形式の独創 + 低い読みやすさ = 未来の傑作の可能性
高いプロット設計 + 低いテーマの深さ = 面白いが残らない可能性
高い感情の力 + 低い凡庸性除去 = 感傷の危険
```

## Correspondence with the Story Vector

Each evaluator contributes to a specific dimension of the Story Vector (other dimensions are null).

```
Story Vector:
[narrative_originality, quality, emotional_power, plot_architecture,
 character_depth, prose_style, theme_resonance, world_building,
 narrative_technique, reader_experience, admiration]
```

## Evaluator Selection in the Council

The council orchestrator (story-council) selects evaluators according to the subdomain. For details, see the selection matrix in `skills/story-council/SKILL.md`.
