# Changelog

## 0.6.0 — 2026-11-09

插件市场打包。

- 新增 `.claude-plugin/plugin.json` 与 `.claude-plugin/marketplace.json`，仓库可直接作为 Claude Code 插件市场安装。
- README 安装节增加插件安装命令。

## 0.5.0 — 2026-11-09

否决立法案例库。

- 新增 `cases/`：案例模板、类型定义（否决 / 改判 / 立法）、贡献与隐私规则。
- 种子案例 2 个：001 从"炼化高级感"到"只判丑"（立法）；002 目测"信号色争宠"被 0.3% 实测推翻（改判）。
- `verdict-format.md` 的否决立法流程接入 `cases/`；SKILL 与 README 导航同步。

## 0.4.0 — 2026-11-09

F 域 PPT / 文档 + G 域视频 / 动效。

- 新增 `references/clauses/slides-docs.md`：9 条红线 + 2 条倾向——一页一断言（标题即结论）、断言-证据配对、页密度、可读字号、图表纪律（坐标轴/3D 饼图/数据墨水）、母版与网格、视觉层级与强调、事实与出处、交付可用性；备注与中文排版。
- 新增 `references/clauses/video-motion.md`：10 条红线 + 2 条倾向——动效动机、参数克制（时长/距离/曲线）、编排（一个主角动作）、可访问与性能、视频前 3 秒、节奏与剪辑、字幕与安全区、音画同步、抽帧可读、素材与版权；风格统一与导出规格。
- `project-params.md` 新增第 10 节幻灯片与文档参数、第 11 节视频与导出参数。
- `evidence-kit.md` 新增幻灯片缩略墙（18）与视频抽帧板（19）。
- F/G 各附匿名化判卷样例。

## 0.3.0 — 2026-11-09

D 域文案 + E 域网页。

- 新增 `references/clauses/copywriting.md`：10 条红线 + 2 条倾向——说人话、一词一义、动作即结果、错误与空状态可行动、中文标点与排版、术语与称谓一致、语气统一、不注水（删句测试 + AI 味黑名单）、可扫读、事实与数字纪律、句长、本地化。
- 新增 `references/clauses/web-pages.md`：11 条红线 + 2 条倾向——首屏说清、一屏一节、响应式断点、状态覆盖、可访问性下限、触控目标、真实内容、稳定与性能、导航与位置感、表单与输入、模板指纹黑名单、动效克制、视觉与文案同源。
- 新增 `scripts/copy_lint.py`：中文标点半角、直引号、省略号、连续标点、空括号、中西文空格、句长、AI 味黑名单；支持 `--json` 与 CI 退出码。
- `project-params.md` 新增第 8 节文案参数、第 9 节网页参数。

## 0.2.1 — 2026-11-09

C 域：角色与动画。

- 新增 `references/clauses/character-animation.md`：12 条红线 + 2 条倾向，覆盖规格卡一致、关键姿态剪影、持具接触（含有手指/圆手两种角色）、绑骨形变、解剖可达性、弧线与预备-跟随、节奏缓动、挤压拉伸、脚部接触、循环与待机、穿模、表情视线、动作个性、次级运动。
- 条款取材于真实项目教训：修手 17 版全败后的"磁吸持具"、大头短臂的"嘴够不到碗"解剖发现、八条动作规则。
- 附加匿名化判卷样例（吃播动作首轮：3 条红线 + 1 条存疑）。

## 0.2.0 — 2026-11-09

取证自动化。

- 新增 `scripts/evidence.py`（Python 3.9+ / Pillow，离线、确定性）：`kit` / `silhouette` / `thumbs` / `gray` / `blur` / `crop` / `colors` / `grid` / `contrast` 九个子命令。
- `kit` 一条命令产出灰度图、眯眼模糊、剪影墙、64px 缩略墙、主色与饱和面积统计、`manifest.md`。
- 新增 `scripts/README.md`：命令表、条款映射与示例。

## 0.1.1 — 2026-11-09

- 新增 `examples/case-game-ui-round1.md`：小游戏首屏 UI 的匿名化判卷样例（8 条红线 + 8 条存疑）。
- 记录首轮实测暴露的取证缺口：单张截图无法完成剪影 / 64px / 灰度取证。

## 0.1.0 — 2026-11-09

首个骨架版本。

- `SKILL.md`：触发条件、两档模式（草稿免检 / 交付判卷）、七步流程、最小判词格式。
- `references/evidence-kit.md`：16 项取证工具。
- `references/verdict-format.md`：三态判定、四段式判词、报告结构、复判、否决立法。
- `references/clauses/art-scene-props.md`：A 域 10 条（R9 + T1）。
- `references/clauses/ui-layout.md`：B 域 10 条（R9 + T1）。
- `references/clauses/project-params.md`：参数槽。
- `examples/case-game-art-round1.md`：匿名化首轮判卷节选。
- `evals/evals.json`：10 条触发与行为用例。
