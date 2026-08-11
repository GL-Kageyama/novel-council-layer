**Language:** English | [日本語](ja/meaning-of-novels.md) | [中文](zh/meaning-of-novels.md)

# Meaning of Novels (The Meaning of Novels and the Criteria for Evaluation — Structural)

The subject of evaluation in this plan is not mere "enjoyability." It is **"works that become a part of one's life."** The criteria for making that judgment are defined through **structural description** (no proper nouns).

## What Is a "Work That Becomes Part of One's Life"

| Criterion | Meaning | Structural Description (no proper nouns) |
|------|------|--------------------------|
| **Persistence of the post-reading shift** | Weeks or months after reading, a certain scene or phrase is still recalled | A device in which the ending recontextualizes a small motif from the opening and returns the reader's memory to the first scene. Upon reaching the ending, the reader recalls the opening "with a different meaning" |
| **Inseparability from life's turning points** | The work becomes bound to the reader's state at the time of reading and cannot be separated | A structure that leaves the work room for interpretation, producing polysemy onto which the reader can project their personal experience |
| **Deepening with each rereading** | Each rereading reveals a new layer, and interpretation deepens | A structure in which the knowledge the narrator concealed on the first reading is revealed to have already been hinted at on rereading. The second-time reader is reading a different story from the first |
| **Telling to others** | One comes to want to tell about oneself through the work | Polysemy in which the work functions as a mirror for telling the reader's own experience |

## Deepening of Emotion: Distinguishing Sentimentality from Genuine Emotion

| | Sentimentality (deduction) | Genuine Emotion (evaluation) |
|---|------------|------------------|
| Source | Formulaic devices (using tragedy, parting, and death for facile tears) | The characters' internal conflicts arise naturally from the narrative structure as a chain of actions and choices |
| Structure | Tragic events are arranged solely for the sake of emotional buildup | The protagonist's self-deception — recognizing their own flaws yet being unable to change them — is depicted as a chain of choices and regret. The honesty of suffering that is not beautified |
| Memory | Only at the moment of consumption. Soon forgotten | Remains after reading and is recalled over time |

**Aesthetics of restraint**: What deepens emotion most is restraint in expression. By not telling, room is opened in the reader's emotions. This kind of restraint is the archetype of a genuine emotional experience and the polar opposite of sentimentality. The "restraint" axis of the emotional-power evaluator is based on this principle.

## The Tension Between the Mission of Meaning and the Filtering Infrastructure

The "B2B filtering infrastructure" of the revenue hypothesis appears at first glance to be in tension with the mission of meaning. This tension is organized explicitly as follows.

> **The purpose of filtering is not efficiency. It is the discovery of buried masterpieces.**

- **Primary filtering** is a judgment of "is it worth reading," while **evaluation of meaning** is a deeper judgment of "does it change one's life."
- The system's ultimate purpose is to see through to meaning. Filtering is a means to that end; meaning must not be lost for the sake of efficiency.
- The fact that the benchmark (`references/benchmark-50novels.md`) uses literary history — the accumulation of meaning — as validation data is the key to resolving this tension. The system validates itself against the history of meaning.

## Treatment in the Evaluation Setting

- The structural descriptions above are reflected in the prompts of the evaluator agents (especially theme-resonance, emotional-power) **only in forms that carry no proper nouns**.
- The criterion of "becoming a part of one's life" is concretized in implementation as the dimensions of theme-resonance (post-reading shift, depth of rereading) and emotional-power (post_reading_shift).
