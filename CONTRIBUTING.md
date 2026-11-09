# Contributing

感谢愿意帮忙。这个项目只守一条原则：**只加“什么算不及格”，不加“什么是好”。**

## 可以贡献什么

- **新条款域**：例如包装、舞台执行。按 `references/clauses/README.md` 的最低要求来。
- **补充“违反的样子”**：给现有条款加真实、可指位的反例。
- **匿名化案例**：真实判卷或否决记录，按 `cases/TEMPLATE.md` 写。
- **工具改进**：`scripts/` 下的取证或文案检查。
- **英文翻译**：条款正文目前中文单源，英文索引在 `references/clauses/index.en.md`。

## 开发环境

```bash
pip install pillow
python scripts/copy_lint.py .          # 文案检查（应为 0 违规）
python scripts/run_evals.py --check    # eval 题库校验
python scripts/evidence.py kit <img>   # 图像取证冒烟
```

提交前跑一遍上面的检查；CI 也会跑。

## 提 Issue

- Bug / 判词不对：用 `bug_report` 模板，附上原图或可复现的输入。
- 新条款提案：用 `clause_proposal` 模板，写清判据、违反的样子、修法。

## 隐私

公开材料必须匿名化：项目名、角色、剧情、商业信息一律替换。证据图同理。

## 提交约定

- 一个 PR 一件事。
- 条款编号自 v1.0 起冻结：新增用新号，弃用标 `(deprecated)`，不改号、不复用。
- 改动条款时同步更新 `CHANGELOG.md` 与英文索引（如涉及编号）。

## 行为准则

讨论以证据为准，不以“我觉得好看/不好看”为准。评审别人的条款时，同样只判“这条判据能不能判定、证据指不指得准”。
