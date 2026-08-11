**Language:** English | [日本語](README-ja.md) | [中文](README-zh.md)

# Examples — Novel Samples

A collection of samples demonstrating the **write → evaluate → rewrite** loop for each genre.

## Folder Structure

| Folder | Genre | Contents |
|----------|---------|------|
| `novel-sample/` | Sample novel | Evaluation target text + Story Report |

Each sample folder contains:
- `input.md` — the novel to be evaluated (before anonymization)
- `input-anonymized.md` — the body text anonymized with `utils/anonymize.py` (evaluation input)
- `report-v1.json` — initial evaluation (strict score)
- `report-v2.json` — re-evaluation after rewrite (demonstrates the loop's improvement)
- `report.md` — Markdown view (readable in GitHub / VSCode preview)

## Usage

**Anonymizing input (first blind):**
```bash
python ../utils/anonymize.py input.md --author "著者名" --title "作品名" > input-anonymized.md
```

**Reading evaluations (as Markdown):**
```bash
python ../utils/render_report.py --format md novel-sample/report-v2.json
```

**Showing individual reports for all evaluators:**
```bash
python ../utils/render_report.py --individuals novel-sample/report-v2.json
```

**Comparing the loop's improvement:**
```bash
python ../utils/compare_reports.py novel-sample/report-v1.json novel-sample/report-v2.json
```

**Validating all samples:**
```bash
for f in */report-*.json; do python3 ../utils/validate_output.py "$f"; done
```

## Individual evaluation reports (individual_reports)

Each report's `individual_reports` contains the **raw data from all convened evaluators** (`weaknesses`・`improvement_suggestions`・`narrative`). This is input to be read as **material for rewriting**.

## Short story sample (short-story/)

`short-story/` is a sample of an **actual short story (text)** rather than a synopsis (plot). It was written as a flash piece (prose) based on the "Last Line" premise. Because of `content_type: text`, it is evaluated by **all 10 evaluators, including prose-style, narrative-technique, and reader-experience**, which are not convened in plot mode.

| File | Contents |
|---------|------|
| `input.md` | Short story (v1→v2→v3) |
| `report-v1.json` | Initial evaluation (present value 68 / potential 71) |
| `report-v2.json` | Loop 2 (69/71, worldview +9) |
| `report-v3.json` | After correcting the user-noted issues (**69/72, theme +6, quality +4**) |
| `report-v4.json` | Added sensory texture (**70/72, prose style +7**) |
| `report-v5.json` | Tidied the mid-section prosody and the "paper" metaphor (prose style maintained at 70) |
| `report-v6.json` | **Final draft** (opening scene-setting, trimming repetitions, removing the mold structure, **prose style 72**) |
| `report.md` | v6 (final draft) Markdown view |

**v3 is the revision that corrects the user-noted "sorry-dependence"**: instead of relying on words of apology, it precisely embodies the world rule (words are delivered through a response) with words that await a response ("welcome home" → "I'm home"). It separates the three registers of apology (mother), farewell (daughter), and return (old woman / Yū). In the evaluation, quality (54→62) and theme (78→83) improved, and the criticisms of the sentimental mold and the symmetry were resolved.

**v4 responds to the prose-style evaluation (59) by adding sensory texture**: the moment of not squeezing the sweaty mother's hand in return, the old woman's hand dry as if stacked paper, the words on a single slip of paper held between fingertips, the thin and nearly torn notebook and the smell of ink. prose-style went from 59 to **70**.

**v6 is the final draft**: it opens with a scene of opening the notebook, making the world rule felt through an object. Using the commercial register of "cutting through" and "crossing", it trims the repetition of "spend / reach" and removes the mold of the two mid-section encounters. Prose style reaches **72**. Improvement from v1: prose style +9, worldview +9, theme +6, quality +4 (present value 68→70).

## Notes on verification (operational)

`novel-sample/` is a real example evaluated over 3 loops in story-council **plot mode** (content_type: plot, mode: full):

| File | Contents |
|---------|------|
| `input.md` | Synopsis (v1→v2→v3) |
| `report-v1.json` | Initial evaluation (present value 62 / potential 65) |
| `report-v2.json` | Loop 2 (65/66) |
| `report-v3.json` | Loop 3 (**68/68**, +4.6 average improvement) |
| `report.md` | v3 Markdown view |

**Operational notes**:
- **A restart of Claude Code (or `/agents`) is required** for the native launch of the evaluator agents (`agents/`). Before the restart, a fallback method that reads the system prompt from the agent files and launches from it can be used.
- In plot mode, the three evaluators `prose-style`, `narrative-technique`, and `reader-experience` are not convened and become `null` in the Story Vector (recorded in `non_consulted_evaluators`).
- From the improvement trend across the 3 loops, the evaluation → revision loop can be confirmed to work.
