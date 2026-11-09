# 否决立法案例库

> 这里存的是**判词的反对票**：用户否掉判词、工具改正判词、或一次否决最终变成条款修订的记录。
> 条款告诉 AI “怎么判”，案例告诉 AI “判错了怎么改”。这是本 skill 里唯一靠使用攒出来的部分。

## 案例类型

- **否决**：用户否掉一条判词。记录原判词、否决理由、最终裁决。
- **改判**：工具测量或新证据推翻了判词（例如目测 vs 实测）。
- **立法**：一次否决/改判最终改写了条款或参数。
- **外部试跑**：由另一个会话或另一位使用者按 skill 流程实跑，记录结果与暴露的缺口。

## 文件命名

`YYYY-MM-DD-<短横线英文 slug>.md`，例如 `2026-11-09-saturation-measurement.md`。

## 一个案例怎么走完

1. 用 `TEMPLATE.md` 建文件，编号顺延。
2. 归因三选一：**条款错**（判据不成立）/ **参数错**（项目参数不适用）/ **执行错**（取证或判断有误）。
3. 对应修订：改条款、改参数、或改取证流程；在 CHANGELOG 留痕。
4. 如果修订影响判法，在 `references/clauses/` 对应文件里更新，并链回本案例。

## 隐私

- 公开案例必须匿名化：项目名、角色、剧情、商业信息一律替换。
- 证据截图同样检查；不确定就不放图，只留文字描述。

## 现有案例

- [2026-11-08-ugliness-as-principle.md](2026-11-08-ugliness-as-principle.md) — 立法：从“炼化高级感”到“只判丑”
- [2026-11-09-saturation-measurement.md](2026-11-09-saturation-measurement.md) — 改判：目测“信号色争宠”被 0.3% 的实测推翻
- [2026-11-09-dogfood-self-review.md](2026-11-09-dogfood-self-review.md) — 改判：自审发现 linter 把代码当正文
- [2026-11-09-external-pixel-playtest.md](2026-11-09-external-pixel-playtest.md) — 外部试跑：像素画首屏，促成 H 域诞生
- [2026-11-09-pixel-rerun-h-domain.md](2026-11-09-pixel-rerun-h-domain.md) — 复跑验收：H 域六条红线全部带数字，催生 palette/lightness 工具
