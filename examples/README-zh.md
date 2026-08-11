**Language:** [English](README.md) | [日本語](README-ja.md) | 中文

# Examples — 小说样本

按体裁演示 **写作 → 评估 → 重写** 循环的样本集。

## 文件夹结构

| 文件夹 | 体裁 | 内容 |
|----------|---------|------|
| `novel-sample/` | 示例小说 | 评估对象的文本 + Story Report |

每个样本文件夹包含:
- `input.md` — 评估对象的小说（匿名化前）
- `input-anonymized.md` — 用 `utils/anonymize.py` 匿名化后的正文（评估输入）
- `report-v1.json` — 初次评估（严格评分）
- `report-v2.json` — 重写后的再评估（演示循环的改善）
- `report.md` — Markdown 显示（可用 GitHub / VSCode 预览阅读）

## 使用方法

**对输入进行匿名化（第一重盲评）:**
```bash
python ../utils/anonymize.py input.md --author "著者名" --title "作品名" > input-anonymized.md
```

**阅读评估结果（转换为 Markdown）:**
```bash
python ../utils/render_report.py --format md novel-sample/report-v2.json
```

**显示到全部评估者的个别报告:**
```bash
python ../utils/render_report.py --individuals novel-sample/report-v2.json
```

**比较循环的改善:**
```bash
python ../utils/compare_reports.py novel-sample/report-v1.json novel-sample/report-v2.json
```

**验证所有样本:**
```bash
for f in */report-*.json; do python3 ../utils/validate_output.py "$f"; done
```

## 个别评估报告（individual_reports）

每份报告的 `individual_reports` 中包含**所召集全部评估者的原始数据**（`weaknesses`・`improvement_suggestions`・`narrative`）。这是**作为重写素材来阅读的输入**。

## 短篇小说样本（short-story/）

`short-story/` 不是梗概（plot），而是**实际短篇小说（text）**的样本。它把「最后一句台词」的设定写成掌篇（散文）。由于 `content_type: text`，评估由**包括 plot 模式中未召集的 prose-style・narrative-technique・reader-experience 在内的全部10体**进行。

| 文件 | 内容 |
|---------|------|
| `input.md` | 短篇小说（v1→v2→v3） |
| `report-v1.json` | 初次评估（现在价值68/潜在71） |
| `report-v2.json` | 循环2（69/71、世界观+9） |
| `report-v3.json` | 修正用户指摘后（**69/72、主题+6・品质+4**） |
| `report-v4.json` | 追加感官质感（**70/72、文体+7**） |
| `report-v5.json` | 整理中段的韵律与「纸」的比喻（文体维持70） |
| `report-v6.json` | **最终稿**（开头场景化・削减重复・消除模具结构、**文体72**） |
| `report.md` | v6（最终稿）的 Markdown 显示 |

**v3 是修正了用户指摘的「依赖道歉」的版本**: 不依赖道歉之词，而是用等待应答的话语（「欢迎回来」→「我回来了」）精确体现世界的规则（话语通过应答得以传达）。它分离了道歉（母亲）・告别（女儿）・归返（老妇/悠）三种语域。在评估上，品质（54→62）与主题（78→83）得到改善，感伤的套路与对称性的批判得到化解。

**v4 是回应文体评估（59）的指摘、追加了感官质感的版本**: 没有反握出汗的母亲之手的一瞬、干燥得像叠起的纸张一样的老妇之手、夹在指尖的一张纸上的话语、变薄而快要破损的账本与墨水的气味。prose-style 从 59 提升到 **70**。

**v6 是最终稿**: 以翻开账本的场景开篇，让世界的规则透过道具得以感官化。用「凿穿」「渡越」的商业语域削减「费/达」的重复，化解中段两处相遇的模具结构。文体达到 **72**。自 v1 的改善: 文体+9・世界观+9・主题+6・品质+4（现在价值 68→70）。

## 运行确认的注意事项（运用时）

`novel-sample/` 是使用 story-council 的 **plot 模式**（content_type: plot, mode: full）进行 3 轮循环评估的实际示例:

| 文件 | 内容 |
|---------|------|
| `input.md` | 梗概（v1→v2→v3） |
| `report-v1.json` | 初次评估（现在价值62/潜在65） |
| `report-v2.json` | 循环2（65/66） |
| `report-v3.json` | 循环3（**68/68**、平均改善+4.6） |
| `report.md` | v3 的 Markdown 显示 |

**运用上的注意事项**:
- 评估者代理（`agents/`）的原生启动需要**重启 Claude Code（或使用 `/agents`）**。在重启之前，可以采用读取代理文件中的系统提示词并据此启动的回退方式运行。
- 在 plot 模式下，`prose-style`・`narrative-technique`・`reader-experience` 这 3 体不会被召集，在 Story Vector 中变为 `null`（记录在 `non_consulted_evaluators` 中）。
- 从 3 轮循环的改善趋势可以确认，评估 → 修正循环是有效的。
