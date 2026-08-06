# Evaluator Taxonomy（評価者分類と次元の境界）

Novel Council Layer の評価者群は、単一の価値観ではなく**複数の独立した視点**から構成される。この文書は各評価者の位置づけ、担当サブドメイン、他の評価者との次元の境界を定義する。

## 評価者のカテゴリ

評価者は3つの層に分かれる。

### 第1層：現在価値分析（Current Value Analysis）

物語が**現時点で**どれだけ読む価値を持つかを評価する。

| 評価者 | 視点 | 担当サブドメイン |
|--------|------|-----------------|
| Anti-Generic Filter | クリシェ・類型・予定調和の検出（横断） | 全サブドメイン |
| Narrative Originality | 形式・前提の逸脱 | 全サブドメイン |
| Emotional Power | 感情の力・読後の変位 | pure-literature, genre-fiction, short-story |
| Plot Architecture | 因果・情報開示・伏線 | genre-fiction, light-novel |
| Character Depth | 人物の深さ・内的葛藤 | light-novel, historical-fiction |
| Prose Style | 文体・言葉の音楽 | pure-literature, short-story |
| World Building | 世界観の創造性・整合性 | genre-fiction, light-novel, historical-fiction |
| Narrative Technique | 語りの距離・時間操作 | pure-literature, short-story |
| Reader Experience | 読書体験・没入 | genre-fiction, light-novel |

### 第2層：潜在価値発見（Hidden Potential Discovery）

現在評価されていない**未来の可能性**を発見する。

| 評価者 | 視点 |
|--------|------|
| Theme Resonance | テーマの深さ・読後に残る意味・再読の深さ |

### 第3層：基準層（Meta Layer）

評価の前提そのものを揺さぶる。

| 評価者 | 視点 |
|--------|------|
| Anti-Generic Filter | 凡庸性の除去（全評価者に横断的に働く） |

※ Theme Resonance は現在価値（テーマの一貫性）と潜在価値（読後の意味・再読）の両方に寄与する。第2層として扱う。

## 各評価者の核となる問い

| 評価者 | コア質問 |
|--------|----------|
| Narrative Originality | 物語の**形式**が既存パターンから意味ある逸脱をしているか？ |
| Anti-Generic Filter | クリシェ・類型・予定調和に堕していないか？ |
| Emotional Power | 読者の心を動かし、記憶に定着するか？ |
| Plot Architecture | 因果と情報開示は巧みに設計されているか？ |
| Character Depth | 人物は生きた人間として立ち上がるか？ |
| Prose Style | 文体は言葉の音楽として機能するか？ |
| Theme Resonance | 主題は深く、一貫し、存在の問いに触れるか？ |
| World Building | 舞台は創造的で、内的整合性を持つか？ |
| Narrative Technique | 語りの距離と時間操作は物語を強化するか？ |
| Reader Experience | 読む体験として没入し、完成し、再読を誘うか？ |

## 隣接次元との境界（重複の整理）

| 対 | 境界の定義 |
|----|-----------|
| **narrative_originality** × **theme_resonance** | 独創性は「形式の逸脱」、テーマは「内容の深さと意味」を見る。独立に動く |
| **plot_architecture** × **narrative_technique** | プロットは「何がいつ明かされるか」、技法は「誰がどう語るか」を見る |
| **emotional_power** × **reader_experience** | 感情は「心の変位」、読書体験は「読む行為の質」を見る |
| **prose_style** × **reader_experience** | 文体は「言葉の音楽」、読書体験は「体験全体」を見る |
| **theme_resonance** × **emotional_power** | テーマは「読後に残る解釈・意味」、感情は「読中の心の変位」を見る |
| **anti-generic-filter** × **narrative_originality** | 反凡庸は「月並みかどうか」、独創性は「逸脱の意味」を評価する |

## 評価者間の関係

### 補完関係

- **Plot Architecture ↔ Character Depth**: 優れた物語はプロットと人物の両方が噛み合う。プロットだけ・人物だけの物語はどちらも脆い。
- **Prose Style ↔ Emotional Power**: 抑制の美学——語らない文体——は感情を深める。文体と感情は独立に見るが、抑制は両者に跨る。
- **Theme Resonance ↔ Reader Experience**: 読後に残る意味（テーマ）は、読む体験（没入）があって初めて成立する。

### 対立構造

この対立は**平均化されるべきではない**。むしろ、衝突が価値の重要な兆候である。

```
高い形式の独創 + 低い読みやすさ = 未来の傑作の可能性
高いプロット設計 + 低いテーマの深さ = 面白いが残らない可能性
高い感情の力 + 低い凡庸性除去 = 感傷の危険
```

## Story Vector との対応

各評価者は Story Vector の特定の次元に貢献する（他の次元は null）。

```
Story Vector:
[narrative_originality, quality, emotional_power, plot_architecture,
 character_depth, prose_style, theme_resonance, world_building,
 narrative_technique, reader_experience]
```

## 合議での評価者選択

合議オーケストレーター（story-council）はサブドメインに応じて評価者を選択する。詳細は `skills/story-council/SKILL.md` の選択マトリクスを参照。
