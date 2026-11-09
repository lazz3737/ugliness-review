# Changelog

## 0.2.1 — 2026-11-09

C 域：角色与动画。

- 新增 `references/clauses/character-animation.md`：12 条红线 + 2 条倾向，覆盖规格卡一致、关键姿态剪影、持具接触（含有手指/圆手两种角色）、绑骨形变、解剖可达性、弧线与预备-跟随、节奏缓动、挤压拉伸、脚部接触、循环与待机、穿模、表情视线、动作个性、次级运动。
- 条款取材于真实项目教训：修手 17 版全败后的"磁吸持具"、大头短臂的"嘴够不到碗"解剖发现、八条动作规则（歪头/过冲回弹/压扁帧/滞后/快停慢/待机微动作）。
- 附加匿名化判卷样例（吃播动作首轮：3 条红线 + 1 条存疑）。
- `project-params.md` 新增第 7 节"角色与动画参数"（规格卡、关键点距离、吸附点、帧率、过冲幅度、待机层数）。
- `clauses/README.md`、`SKILL.md`、`README.md` 同步更新域列表与导航。

## 0.2.0 — 2026-11-09

取证自动化。

- 新增 `scripts/evidence.py`（Python 3.9+ / Pillow，离线、确定性）：`kit` / `silhouette` / `thumbs` / `gray` / `blur` / `crop` / `colors` / `grid` / `contrast` 九个子命令。
- `kit` 一条命令产出灰度图、眯眼模糊、剪影墙、64px 缩略墙、主色与饱和面积统计、`manifest.md`。
- 新增 `scripts/README.md`：命令表、条款映射与示例。
- `references/evidence-kit.md`：工具说明改为"脚本命令 + 手工操作"混合；新增"自动化"一节。
- `SKILL.md`：流程第 3 步接入脚本；文件导航新增 `scripts/evidence.py`。

## 0.1.1 — 2026-11-09

- 新增 `examples/case-game-ui-round1.md`：小游戏首屏 UI 的匿名化判卷样例（8 条红线 + 8 条存疑），演示数值条款与项目参数豁免的用法。
- 记录首轮实测暴露的取证缺口：单张截图无法完成剪影 / 64px / 灰度取证，数值条款需要脚本量。

## 0.1.0 — 2026-11-09

首个骨架版本。

- `SKILL.md`：触发条件、两档模式（草稿免检 / 交付判卷）、七步流程、最小判词格式。
- `references/evidence-kit.md`：16 项取证工具（首眼、眯眼、灰度、剪影墙、64px 缩略、切线放大、取色器、网格、对比度等）。
- `references/verdict-format.md`：三态判定、四段式判词、报告结构、复判、否决立法。
- `references/clauses/art-scene-props.md`：A 域 10 条（R9 + T1）。
- `references/clauses/ui-layout.md`：B 域 10 条（R9 + T1）。
- `references/clauses/project-params.md`：度量表 / 色卡 / 字号 / 材质 / 网格 / 最小观看尺寸参数槽。
- `examples/case-game-art-round1.md`：匿名化首轮判卷节选。
- `evals/evals.json`：10 条触发与行为用例。
