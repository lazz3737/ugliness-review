# Changelog

## 1.2.5 — 2026-11-09

触发词缺口修正（Eval Case 6 复盘）。

- 查明：Case 6 三次运行均无工具调用，skill 从未加载；此前按“格式不合规”判失败属于误判。
- 根因：description 只覆盖“审一下 / 检查 / 挑错 / 交付前过一遍”，未覆盖“看着不太舒服 / 哪里不对 / 怎么改才好”。
- `SKILL.md` description 补中英口语触发词（仍声明只判丑、不接审美委托）。
- `evals.json` 新增 Case 11（口语触发探针）；README 更新 Case 6 结论。

## 1.2.4 — 2026-11-09

Eval Case 6 复跑仍败，规则加锁。

- 二跑表现：风格选项已写成“二选一”（进步）；但仍无条款号，且出现效果承诺“页面会立刻安静下来”。
- `SKILL.md`「用户直接要好看」：固定输出结构（先判词表，再修复顺序，每条挂条款号）；补反例/正例对照；把“立刻安静 / 马上顺眼”列入禁用承诺。

## 1.2.3 — 2026-11-09

Eval Case 6 首跑未过，补应答规则。

- 失败表现：缺陷找得准、带坐标，但无条款号；出现效果承诺（“修完就会顺眼很多”）；一条风格主张（“改成地铁图式正交折线”）。
- `SKILL.md` 新增「用户直接要好看」：改判丑、风格选择写成选项由用户定、禁止效果承诺、仍走四段式判词。
- `verdict-format.md` 判词纪律同步；`evals/README.md` 更新进度，Case 6 待复跑。

## 1.2.2 — 2026-11-09

- 新增 `evals/README.md`：用例类型、跑法、判定口径与当前进度。
- 跑表与文档明确：每条用例单独开新会话；同会话连跑只能算宽松通过。
- 进度：Case 1 实跑通过；Case 3/4 宽松通过（同会话连跑）。

## 1.2.1 — 2026-11-09

- `SKILL.md` 取证纪律：先一次性跑 `kit` 与 `contrast`/`palette` 拿数据，再判；不许逐像素手算（外部试跑慢的主因）。
- `run_evals.py` 跑表增加建议顺序：先轻后重。

## 1.2.0 — 2026-11-09

Eval runner。

- 新增 `scripts/run_evals.py`：`--check` 校验题库结构；`--sheet` 生成人工跑表；`--run` 在已装 Claude CLI 时逐条自动跑并落盘。
- 跑表含每条用例的 prompt、期望、断言与 pass/fail 记录列；`evals/runs/` 与 `run_sheet.md` 已 gitignore。
- 文档补充：触发类用例必须在全新会话中运行。

## 1.1.2 — 2026-11-09

- H-R4 / H-R7 补齐测量口径：色板用全图色数、明度用 Lab L* 差。
- `evidence.py` v0.3.0：新增 `palette`（全图色数，可查局部）与 `lightness`（两点 L* 差）子命令。
- 新增案例 005（外部复跑：H 域验收），记录“判据缺口径”的修订闭环。
- 复测本图：1572 色；发色 vs 墙 L* 差 8.2（取样点不同，量级与复跑一致）。

## 1.1.1 — 2026-11-09

- 新增案例 004（外部试跑：像素版首屏），记录 H 域的反馈闭环：外部试跑 → 条款缺口 → 新增 H 域。
- 案例类型新增「外部试跑」。

## 1.1.0 — 2026-11-09

H 域：像素画（来自首次外部试跑反馈）。

- 新增 `references/clauses/pixel-art.md`：8 条红线 + 2 条倾向——整数缩放、像素密度（PPU）、描边策略、色板容量、无抗锯齿、像素字库、剪影对比、帧纪律；抖动与风格纯度。
- 写明与其它域的替换关系：像素画用 H-R3/R4 替代 A-R3 材质语言，A-R7 由 H-R7 继承加严，C 域动作结构照常、帧率照 H-R8。
- `project-params.md` 新增第 12 节像素画参数。
- `A-R3` 增加像素画替换说明；SKILL/README/索引同步。

## 1.0.1 — 2026-11-09

自审修正（dogfooding）。

- 修复 `SKILL.md` description 的 YAML 解析错误（冒号需加引号），`npx skills add` 现可正常安装。
- `copy_lint.py` v0.2.0：跳过 YAML frontmatter、fenced code、inline code；不再扫描 `.json`；避免对代码示例误报。
- 全库 Markdown 的中文直引号规范为 `“”`（217 行）；修正少量半角标点与空引号示例；复判 D-R5 违规归零。
- 安装验证：`npx skills add` 全局安装成功，落盘 `~/.claude/skills/ugliness-review`，分发 24 个 agent。
- 新增案例 003（自审：linter 误报代码为正文）。

## 1.0.0 — 2026-11-09

界面双语 + 编号冻结。

- `README.md` 改为英文主版；新增 `README.zh-CN.md` 中文版；两版顶部互链。
- 新增 `references/clauses/index.en.md`：全部 82 条条款的编号与英文一句话摘要；条款正文保持中文单源。
- `SKILL.md` 的 description 改为中英双语，英文触发词覆盖 "pre-delivery review / QA gate / critique"。
- 条款编号自 v1.0 起冻结：不复用、不改号；弃用标 `(deprecated)`。
- 仓库可通过 `npx skills add` 与 Claude Code 插件市场两种方式安装。

## 0.6.0 — 2026-11-09

插件市场打包。

- 新增 `.claude-plugin/plugin.json` 与 `.claude-plugin/marketplace.json`，仓库可直接作为 Claude Code 插件市场安装。
- README 安装节增加插件安装命令。

## 0.5.0 — 2026-11-09

否决立法案例库。

- 新增 `cases/`：案例模板、类型定义（否决 / 改判 / 立法）、贡献与隐私规则。
- 种子案例 2 个：001 从“炼化高级感”到“只判丑”（立法）；002 目测“信号色争宠”被 0.3% 实测推翻（改判）。
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
- 条款取材于真实项目教训：修手 17 版全败后的“磁吸持具”、大头短臂的“嘴够不到碗”解剖发现、八条动作规则。
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
