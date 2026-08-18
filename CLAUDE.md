**Language:** English | [日本語](CLAUDE-ja.md) | [中文](CLAUDE-zh.md)

# Novel Council Layer

## Project Identity

This is the **Novel Council Layer**. It is a set of Claude Code agents in which multiple AI evaluator agents evaluate a novel from different narrative perspectives, and the council skill produces a structured Story Report.

> **Division of roles**: This layer is **evaluation only**. The **writing** of a work is left to the writer, the editor, and the generative AI. This repository does not "write"; it "sees through to the value of a narrative", and it prepares its evaluation results as material to be handed to the next rewrite.

## The Core Thesis

**A story is read within time.** A novel is not an object; it is an experience that unfolds within time in the reader's mind. The object of evaluation is the "quality of the time spent reading", not the attributes of the work.

The seven questions specific to narrative evaluation:
1. **Quality of time** — How does this story put the reader's time to use?
2. **Distribution of information** — What is revealed, when, and to whom?
3. **Narrative distance** — Who narrates, and from what distance?
4. **Design of gaps** — Are the gaps the reader must fill designed deliberately?
5. **Alignment of style and time** — Does the prose style control the reading speed and sensation?
6. **Depth of rereading** — When read a second time, does the same book become a different book?
7. **Post-reading displacement** — After reading, does a sense that something in one's life has moved remain?

## The Core Philosophy

- **A story is an art of time**: The object of evaluation is the "quality of the time spent reading".
- **Polyphonic evaluation**: Deliberation by multiple evaluators holding different perspectives.
- **Disagreement itself is a signal**: Conflicts among evaluators are not averaged away; they are preserved as they are.
- **Double blinding**: Reputation is blocked from both the input (author name, title) and the criteria (proper nouns). The precondition that protects the discovery of buried masterpieces.
- **Evaluation over generation**: Discerning the value of a narrative is the competitive arena.

## Directory Conventions

- `agents/{name}.md` — the authoritative source of the evaluator agents (12). Launched as independent subagents acting as persona-based experts
- `skills/story-council/SKILL.md` — the authoritative source of the council orchestrator (the only skill)
- `.claude/agents/` — symlinks for in-project detection (evaluator agents)
- `.claude/skills/` — symlinks for in-project detection (council orchestrator)
- `~/.claude/agents/`, `~/.claude/skills/` — global installation targets (set up by `./install.sh`, callable from anywhere)
- `.claude-plugin/` — plugin distribution definition (for `/plugin marketplace add`)
- `schemas/` — JSON schemas for structured output
- `references/` — the theoretical foundation of narrative evaluation (genealogy of the thesis, structural calibration, blinding, benchmarks)
- `examples/` — sample inputs and outputs
- `utils/` — anonymization, validation, visualization, and comparison utilities

## How to Invoke the Evaluators

**The council is invoked as a skill, the evaluators as subagents.** This division of roles is the crux of the architecture — the evaluators must evaluate independently without knowing each other's results. A skill shares the same context and is therefore unsuited to independent evaluation. Launching the evaluators as subagents isolates the context.

### The Full Council (Recommended)

```
Skill: story-council
Args: {"content": "...", "content_type": "text", "domain": "pure-literature"}
```

The council performs the following:
1. Determines the narrative subdomain of the input
2. Selects the relevant evaluator agents (`anti-generic-story-filter` is always included)
3. Launches each evaluator as a subagent (via the Agent tool, evaluating independently without knowing each other's results)
4. Integrates them into the Story Report
5. Preserves all disagreements

### Plot Evaluation Mode (a synopsis can also be evaluated)

Specifying `content_type: "plot"` allows a pre-writing concept or a simple synopsis to be evaluated. Because there is no prose, narration, or reading experience, the three agents `prose-style`, `narrative-technique`, and `reader-experience` are not convened; evaluation is carried out by the remaining nine (narrative-originality, anti-generic-story-filter, emotional-power, plot-architecture, character-depth, theme-resonance, world-building, admiration, hook).

```
Skill: story-council
Args: {"content": "簡単なあらすじ...", "content_type": "plot", "domain": "genre-fiction"}
```

### Single Evaluator

For when you want to evaluate only a particular perspective. The evaluator is launched as a subagent.

```
Agent tool, subagent_type: plot-architecture
Prompt: {"content": "...", "content_type": "text", "domain": "genre-fiction"}
```

If running as an installed plugin, use the plugin-scoped name (`novel-council-layer:plot-architecture`).

## Output Rules

Every evaluator output must be valid JSON conforming to `schemas/novel-value-output.schema.json`.

```bash
python utils/validate_output.py < output.json
python utils/validate_output.py --json output.json   # 機械可読な検証結果
```

**Automatic retry**: The council skill **deterministically validates** each evaluator's output with `validate_output.py --json`; if it fails, the same evaluator is **restarted up to 3 times** (the feedback includes the error details). If it still fails after 3 retries, it is explicitly recorded in `excluded_evaluators` as `reason: "JSON validation failed after 3 retries"`. **No silent drops.**

**If broken, regenerate (no machine fixing)**: If an evaluator's output JSON is broken (`validate_output.py` returned `"valid": false`), you **must not hand-edit the JSON directly to fix it**. Always **restart that evaluator to regenerate** and re-run validation on the regenerated output. Because a human patching the JSON risks destroying the evaluator's independent voice (scores, judgment, style, narrative), the handling of broken output is unified under "regenerate".

**Anonymize the input (the first blind):**

```bash
python utils/anonymize.py input.txt --author "著者名" --title "作品名" > anonymized.txt
```

## Tools

| Tool | Role |
|--------|------|
| `utils/anonymize.py` | **Anonymizes the input** — removes the author name and title, establishing the precondition for blinded evaluation (the first blind) |
| `utils/validate_output.py` | Schema validation of evaluator output. Outputs machine-readable results via the `--json` flag (used by the council skill's automatic retry) |
| `utils/render_report.py` | Visual rendering of the Story Report (12-dimensional bar chart, category badges, conflicts between dimensions). Saves as a Markdown document with `-o report.md`, displays all individual reports with `--individuals` |
| `utils/compare_reports.py` | Diff comparison before and after a rewrite (for the evaluation → rewrite loop) |

## Evaluation Output Is Designed as "Input"

**The evaluation results of this layer are not themselves the final deliverable.** They are **input** for the writer, the editor, and the generative AI to rewrite with.

- The council **does not generate rewrite instructions themselves**. That is the responsibility of the writer, the editor, and the generative AI.
- Instead, it preserves in full, in `individual_reports`, the **raw material** of each evaluator (`weaknesses`, `improvement_suggestions`, `expected_disagreement_points`, `narrative`).
- Field names are fixed and consistent (conforming to `schemas/novel-value-output.schema.json`).
- Synthetic narratives (e.g. executive_summary) are auxiliary; raw data is never discarded.

**Evaluation → rewrite loop:**
```
評価 → revision_direction（次回の修正方向）→ リライト → 再評価
  → compare_reports.py で改善度確認 → 繰り返し
```

## Key Principles

- An evaluator scores only the dimensions of its own specialty. It returns `null` outside its specialty.
- **Enforce double blinding thoroughly**: the input is anonymous, the criteria are structural. Proper nouns (author names, titles) are excluded from the evaluation venue.
- Predicting disagreement is the evaluator's duty.
- Evaluation must not be diplomatic. Candor is the value.
- Scoring is **deliberately strict**. High scores are rare. **"Readable" does not reach 50.**
- Sentimentality is penalized. The **aesthetic of restraint** — emotion strengthened by what is left unsaid — is evaluated.
- The orchestrator does not dictate judgments to the evaluators. It only convenes and integrates.
- The council does not render a verdict. The final value judgment is the responsibility of the human.
- **i18n baseline**: multilingual support (en/ja/zh) is the default baseline for any fix or change. New or modified agent prompts, schemas, and report templates must resolve through the language mechanism (evaluator agents' `-ja`/`-zh` variants, locale JSON, mirror tree), and user-facing text must be produced in the run's language.

## Installation

```bash
./install.sh            # グローバル: ~/.claude/agents/ + ~/.claude/skills/（どこからでも呼べる）
./install.sh --local    # プロジェクト: .claude/agents/ + .claude/skills/
./install.sh --uninstall
```
