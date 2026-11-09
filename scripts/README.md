# 采集脚本

确定性、离线的取证工具。只读本地文件，不联网、不需要 API key。

依赖：Python 3.9+ 与 Pillow。

```bash
pip install pillow
```

## 一条命令出全套图

```bash
python scripts/evidence.py kit ui.png renders/ -o evidence
```

产出：

```
evidence/
├── manifest.md                  # 输入清单、尺寸、饱和面积、主色（判卷报告可直接引用）
├── wall_thumbs_64.png           # 64px 缩略墙（A-R7）
├── wall_silhouette.png          # 剪影墙（A-R7 / C-R2）
├── ui_gray.png                  # 灰度图（A-R6）
├── ui_blur.png                  # 眯眼/模糊图（A-R5、B-R1）
├── renders_burger_silhouette.png
└── renders_burger_gray.png …
```

## 图像子命令（evidence.py）

| 命令 | 作用 | 主要对应条款 |
| --- | --- | --- |
| `kit` | 标准取证包：灰度、模糊、剪影、缩略墙、主色统计、manifest | 全部 |
| `silhouette` | 纯黑剪影（有 alpha 用 alpha，否则按亮度阈值） | A-R7、C-R2 |
| `thumbs` | 指定尺寸缩略墙（默认 64px） | A-R7 |
| `gray` | 灰度图 | A-R6 |
| `blur` | 眯眼测试（默认半径 = 短边 1.2%） | A-R5、B-R1 |
| `crop` | 区域放大（切线检查） | A-R9 |
| `colors` | 主色占比 + 饱和面积占比 | A-R6、B-R7 |
| `grid` | 网格 + 5% 边距参考线 | B-R5、B-R6、E-R3 |
| `contrast` | 两点 WCAG 对比度 | E-R5 |
| `palette` | 全图不同颜色数（可 `--box` 查局部） | H-R4 |
| `lightness` | 两点 Lab L* 差 | H-R7 |

## 文案检查（copy_lint.py）

```bash
python scripts/copy_lint.py 文案.md
python scripts/copy_lint.py src/ --max-sentence 40 --strict
python scripts/copy_lint.py --text "好的,我马上来."
```

检查项（D 域）：

| 检查 | 条款 | 级别 |
| --- | --- | --- |
| 中文语境半角标点 | D-R5 | 违规 |
| 直引号混排 | D-R5 | 违规 |
| `...` / `。。。` | D-R5 | 违规 |
| 连续标点、空括号 | D-R5 | 违规 |
| 中西文缺空格、连续空格 | D-R5 | 提示 |
| 句长超上限 | D-T1 | 提示 |
| AI 味黑名单词 | D-R8 | 提示（需人工复核） |

`--json` 输出机器可读结果；有违规时退出码为 1，可接 CI。

## 常用示例

```bash
# 剪影墙（透明 PNG 资产最准）
python scripts/evidence.py silhouette assets/ -o evidence

# 64px 缩略墙
python scripts/evidence.py thumbs renders/ --size 64 -o evidence

# 切线检查：把交界处放大 3 倍
python scripts/evidence.py crop ui.png --box 900,380,1060,500 --zoom 3

# 数饱和面积与主色（A-R6 的“饱和面积 ≤15%”）
python scripts/evidence.py colors ui.png --top 8

# 8pt 网格 + 5% 边距线
python scripts/evidence.py grid ui.png --step 8 --margin 5

# 文字对比度
python scripts/evidence.py contrast ui.png --fg 300,640 --bg 200,700

# 像素色板与明度差
python scripts/evidence.py palette sprite.png
python scripts/evidence.py lightness sprite.png --a 940,470 --b 1150,300
```

## 说明

- 只支持栅格图（PNG / JPG / WebP / BMP / GIF）；GLB、SVG、PDF 请先导出图片。
- 有透明通道的资产，剪影直接用 alpha，最准；无透明通道时自动估计背景亮度（四角采样）做阈值，复杂背景可用 `--threshold` 或 `--invert` 调整。
- `colors` 的“饱和面积”按 HSV 饱和度 ≥0.35 统计，是判卷参考值，不是色彩科学结论。
- 所有输出都是确定性的：同一张图、同一参数，结果一致，便于复判对照。

## 版本

- 0.3.0：新增 `copy_lint.py`（D 域文案检查）。
- 0.2.0：`evidence.py` 首个版本，覆盖 16 项取证工具中的 8 项（首眼以外的自动化部分）。
