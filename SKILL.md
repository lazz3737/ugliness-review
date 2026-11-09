---
name: ugliness-review
description: "审丑评审（ugliness-review）——对交付前的视觉产物（游戏美术、UI、版式、网页、PPT、角色动画、视频、像素画、文案）逐条找出可列举的缺陷，输出【条款】【判定】【证据】【修法】判词；只判丑，不判美。Use when the user asks for a pre-delivery review, QA gate, or critique of visual work: return clause-referenced defects with evidence and fixes; never decide what is beautiful. Not for drafts, exploration, or generation tasks."
license: MIT
---

# 审丑评审（Ugliness Review）

> 美归人判，丑归 AI 判；上限归拍板，下限归检查。

## 这是什么

一个**交付前的质检门**，不是审美顾问。它只回答一个问题：**这份东西哪里不及格**。判词必须带条款、带证据位置、带修法；“美不美”永远留给用户。

使用前提：产物的缺陷可以逐条列举（美术资产、UI、版式、网页、PPT、角色与动画、视频、文案、包装、舞台执行）。气韵、风格、高级感的最终裁决不在本 skill 的职责内。

## 何时使用 / 何时不用

**用**：用户明确要求评审、检查、挑错；或产物已到“交付前”——要交给客户、要发上线、要进入下一里程碑。

**不用**：草稿与探索阶段（必须野）；用户要的是“帮我想方向 / 生成设计”；用户只想听鼓励。不要主动对未交付的探索性产物出判词。

判断模式前先问自己：**这份东西现在是要“被交付”，还是还在“被探索”？** 不确定就问用户，不要猜。

## 两档模式

- **草稿 / 探索模式**：不判卷、不引条款。可以聊天、可以给素材参考，但不许把及格线端出来压创意。
- **交付模式**：执行完整判卷；红线未清零不许交付。

## 流程

0. **判模式**：确认是交付模式；不是就停，说明本 skill 不适用于草稿。
1. **选域**：按产物类型选条款域（当前：A 美术场景 / B UI 版式 / C 角色与动画 / D 文案 / E 网页 / F PPT 与文档 / G 视频与动效 / H 像素画；见 `references/clauses/`）。
2. **取参数**：项目是否提供度量表、色卡、字号、材质、角色规格卡、文案声音、网页断点、画幅与导出规格（见 `references/clauses/project-params.md`）。没有就用默认值，并在报告开头声明“参数来源：默认值”。
3. **取证**：按 `references/evidence-kit.md` 采集证据；能自动化的用脚本——`scripts/evidence.py`（灰度 / 模糊 / 剪影墙 / 缩略墙 / 主色 / 网格 / 对比度 / 色板 / 明度）与 `scripts/copy_lint.py`（标点 / 空格 / 句长 / 黑名单）。**先一次性跑 `kit` 与 `contrast`/`palette` 拿数据，再判；不要逐像素手算**（慢且容易错）。证据不足（低清截图、无原图、无关键帧）时先要求补图，不硬判。
4. **判卷**：逐条三态判定——**通过 / 存疑 / 违规**。违规必须附证据；拿不准的进“存疑”，不擅自拍板。
5. **出判词**：按 `references/verdict-format.md` 的四段式输出，末尾给汇总表与修复优先级。
6. **复判**：修复后在同一位置复拍，逐条核对，输出清零表。
7. **否决立法**：用户否决的判词，回写条款修订记录——否决本身是学习数据。

## 判词格式（最小版）

**【条款号】【判定：通过/存疑/违规】【证据：指得准】【修法】**

规则：

- 证据必须指得出位置（哪件资产、哪块区域、坐标或裁剪、放大倍数、哪个关键帧、哪页哪句文案），不许“感觉不对”。
- 只判“不及格”，不说“美不美”；不给风格主张。
- 红线（R）违规未清零，报告结论必须是“不许交付”。
- 倾向（T）违规可商量，但要记账（下不为例）。

完整规则见 `references/verdict-format.md`。

## 边界

- 本 skill 只保下限。全部通过 = “不过不失”，不等于“高级”；上限只能由人拍板。
- 不替用户定义美，不猜测用户意图，不把“我喜欢”写成判据。
- 不为通过而通过：没有证据就不判“通过”，标“未检”。

## 文件导航

- `references/evidence-kit.md` — 取证工具箱（首眼 / 眯眼 / 灰度 / 剪影 / 64px / 切线 / 抽帧 / 字幕 / 文案……）
- `references/verdict-format.md` — 判词格式、三态、复判、否决立法
- `references/clauses/art-scene-props.md` — A 域：道具与场景
- `references/clauses/ui-layout.md` — B 域：UI 与版式
- `references/clauses/character-animation.md` — C 域：角色与动画
- `references/clauses/copywriting.md` — D 域：文案
- `references/clauses/web-pages.md` — E 域：网页
- `references/clauses/slides-docs.md` — F 域：PPT 与文档版式
- `references/clauses/video-motion.md` — G 域：视频与动效
- `references/clauses/pixel-art.md` — H 域：像素画
- `references/clauses/project-params.md` — 项目参数槽
- `scripts/evidence.py` — 图像取证（剪影 / 缩略 / 灰度 / 模糊 / 裁剪 / 主色 / 网格 / 对比度）
- `scripts/copy_lint.py` — 文案检查（标点 / 空格 / 句长 / 黑名单）
- `examples/` — 匿名化判卷样例
- `cases/` — 否决立法案例库（模板 + 真实案例）
- `evals/evals.json` — 触发与行为用例
