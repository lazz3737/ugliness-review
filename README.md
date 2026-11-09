# 审丑评审 · ugliness-review

**An agent skill that reviews visual work negatively: it finds what fails, never decides what is beautiful.**

> 美归人判，丑归 AI 判；上限归拍板，下限归检查。

[![License: MIT](https://img.shields.io/badge/license-MIT-24292f.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-7c3aed.svg)](https://agentskills.io)

## 这是什么

一个**交付前的质检门**，不是审美顾问。它对视觉产物（游戏美术、UI、版式、网页、PPT、角色动画）逐条找出**可列举的缺陷**，输出带条款、证据位置和修法的判词；"美不美"的裁决永远留给使用者。

适合：缺陷可以逐条列举的领域。不适合：气韵、风格、高级感的最终裁决——那部分本 skill 明确不碰。

## 为什么是"审丑"不是"审美"

- **不对称性**：美是稀缺的、主观的、人际共识低；丑是普遍的、可列举的、共识高。人想不出"什么是好"时，几乎总能指出"哪里不对劲"。
- **可审计**：负向判词指得出位置、对得上条款、复得了判；"这很美"既不可辩驳，也不可执行。
- **只保下限**：防丑做到极限，得到的是"不过不失"，不等于"高级"。上限只能由人做冒险的选择。

## 它怎么工作

1. **判模式**：只在交付模式判卷；草稿与探索模式免检（草稿必须野）。
2. **选域取参数**：按产物类型选条款域（A 美术场景 / B UI 版式 / C 角色与动画），再取项目自己的度量表 / 色卡 / 字号 / 材质 / 角色规格卡。
3. **取证**：首眼、眯眼、灰度、剪影墙、64px 缩略、切线放大、取色器、抽帧……（见 `references/evidence-kit.md`）。
4. **三态判卷**：通过 / 存疑 / 违规；违规必须附证据，红线未清零不许交付。
5. **复判与立法**：修复后同位置复拍逐条核对；使用者否决的判词回写条款——**否决本身是学习数据**。

判词样例：

```
【A-R3】【违规】
【证据】BURGER 高光锐利、表面无磨损，与哑光家具并排；见 evidence/batch2/burger_3x.png
【修法】统一 roughness ≥ 0.75，与基准件三件套并排复核后再入库
```

## 取证脚本

`scripts/evidence.py` 把能自动化的取证做成了一条命令（Python 3.9+，只需 Pillow）：

```bash
pip install pillow
python scripts/evidence.py kit ui.png renders/ -o evidence
```

产出：灰度图、眯眼模糊、剪影墙、64px 缩略墙、主色与饱和面积统计、`manifest.md`。另有 `silhouette` / `thumbs` / `gray` / `blur` / `crop` / `colors` / `grid` / `contrast` 子命令，用法见 `scripts/README.md`。

## 安装

作为 Agent Skill 安装（Claude Code / Codex / Cursor 等兼容）：

```bash
npx skills add https://github.com/lazz3737/ugliness-review --skill ugliness-review
```

或手动放进技能目录：

```bash
git clone https://github.com/lazz3737/ugliness-review.git
cp -r ugliness-review ~/.claude/skills/ugliness-review
```

## 目录结构

```
ugliness-review/
├── SKILL.md                        # 薄入口：触发、两档模式、流程、判词格式
├── references/
│   ├── evidence-kit.md             # 取证工具箱
│   ├── verdict-format.md           # 判词格式、复判、否决立法
│   └── clauses/
│       ├── README.md               # 如何新增条款域
│       ├── art-scene-props.md      # A 域：道具与场景
│       ├── ui-layout.md            # B 域：UI 与版式
│       ├── character-animation.md  # C 域：角色与动画
│       └── project-params.md       # 项目参数槽
├── scripts/
│   ├── evidence.py                 # 取证自动化
│   └── README.md
├── examples/                       # 匿名化判卷样例
├── evals/evals.json                # 触发与行为用例
├── CHANGELOG.md
└── LICENSE
```

## 适合谁

- 独立开发者 / 小团队：没有专职美术指导，交付前需要一道稳定的及格线。
- AI 辅助创作：让 agent 在"交付前"自查，而不是在探索期就把创意勒死。
- 任何"缺陷可列举"的视觉交付：游戏资产、角色动画、UI、落地页、PPT、包装、舞台执行。

## 路线图

- [x] v0.1：概念、A/B 两域条款、取证工具箱、判词格式、evals 骨架
- [x] v0.2：取证采集脚本（剪影 / 缩略 / 灰度 / 模糊 / 裁剪 / 主色 / 网格 / 对比度）
- [x] v0.2.1：C 域角色与动画（12 R + 2 T，含解剖可达性与持具接触条款）
- [ ] v0.3：D 域文案、E 域网页；示例库扩充（含"否决立法"案例）
- [ ] v1.0：稳定条款编号；中英双语；发布到技能市场

## 贡献

欢迎新增条款域、补充"违反的样子"、贡献匿名化案例。新增域的最低要求见 `references/clauses/README.md`。

原则只有一条：**只加"什么算不及格"，不加"什么是好"。**

## 许可

[MIT](LICENSE)
