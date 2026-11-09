#!/usr/bin/env python3
"""ugliness-review copy linter (D domain).

Deterministic text checks for Chinese copy. No network, no dependencies.

Checks:
  D-R5  half-width punctuation in Chinese context, straight quotes,
        "..." / "。。。", duplicated punctuation, empty brackets,
        missing CJK/Latin spacing (advisory)
  D-R8  AI-slop phrase blacklist (advisory, human review required)
  D-T1  over-long sentences (default 60 chars)

Usage:
  python scripts/copy_lint.py copy.md
  python scripts/copy_lint.py src/ --max-sentence 40 --strict
  python scripts/copy_lint.py --text "好的,我马上来." --json

Exit code: 1 when any violation is found (or any finding with --strict).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

VERSION = "0.2.0"

CJK = re.compile(r"[㐀-䶿一-鿿]")
TEXT_EXTS = {".md", ".txt", ".srt"}

HALF_PUNCT = ",.!?;:()"
HALF_TO_FULL = {",": "，", ".": "。", "!": "！", "?": "？", ";": "；", ":": "：",
                "(": "（", ")": "）"}

DUP_PUNCT = re.compile(r"([，。！？；：、])\1+")
EMPTY_BRACKETS = ("（）", "()", "「」", "【】", '""', "“”", "‘’")
SENTENCE_SPLIT = re.compile(r"[。！？!?；;]+")

# Advisory list: template phrases that usually say nothing. Context may justify them.
DEFAULT_BANNED_ZH = [
    "赋能", "闭环", "一站式", "重塑", "引领", "开启新篇章", "致力于", "不止于",
    "解锁", "焕新", "沉浸式", "极致", "未来已来", "重新定义", "为而生", "让.*更.*",
]
DEFAULT_BANNED_EN = [
    "empower", "seamless", "revolutionize", "elevate", "unlock", "supercharge",
    "build the future of", "get started", "the future of",
]


def is_cjk(ch: str) -> bool:
    return bool(CJK.match(ch))


def iter_lines(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    return text.splitlines()


def add(findings: list[dict], path: str, line: int, col: int, rule: str,
        severity: str, message: str, snippet: str) -> None:
    findings.append({
        "file": path, "line": line, "col": col, "rule": rule,
        "severity": severity, "message": message, "snippet": snippet,
    })


def check_line(path: str, lineno: int, line: str, max_sentence: int,
               banned_zh: list[str], banned_en: list[str],
               findings: list[dict]) -> None:
    original = line
    n = len(line)
    snippet_full = original.strip()[:80]
    # Mask inline code so code snippets and YAML examples are not linted as prose.
    line = re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), line)

    for i, ch in enumerate(line):
        prev = line[i - 1] if i > 0 else ""
        nxt = line[i + 1] if i + 1 < n else ""
        col = i + 1

        if ch in HALF_PUNCT and (is_cjk(prev) or is_cjk(nxt)):
            full = HALF_TO_FULL.get(ch, ch)
            add(findings, path, lineno, col, "D-R5", "违规",
                f"中文语境使用半角“{ch}”，应为“{full}”", snippet_full)

        if ch in "\"'‘’" and (is_cjk(prev) or is_cjk(nxt)) and ch in "\"'":
            add(findings, path, lineno, col, "D-R5", "违规",
                "中文语境出现直引号，应统一为「」或“”", snippet_full)

        if line.startswith("...", i) and (is_cjk(prev) or is_cjk(nxt)):
            add(findings, path, lineno, col, "D-R5", "违规",
                "中文省略号应为“……”，不是“...”", snippet_full)

        if line.startswith("。。。", i):
            add(findings, path, lineno, col, "D-R5", "违规",
                "中文省略号应为“……”，不是“。。。”", snippet_full)

        # CJK / Latin spacing (advisory)
        if is_cjk(ch) and nxt and re.match(r"[A-Za-z0-9]", nxt):
            add(findings, path, lineno, col, "D-R5", "提示",
                f"中文与“{nxt}”之间建议留空格", snippet_full)
        if re.match(r"[A-Za-z0-9]", ch) and nxt and is_cjk(nxt):
            add(findings, path, lineno, col, "D-R5", "提示",
                f"“{ch}”与中文之间建议留空格", snippet_full)

    for m in DUP_PUNCT.finditer(line):
        add(findings, path, lineno, m.start() + 1, "D-R5", "违规",
            f"连续标点“{m.group(0)}”", snippet_full)

    for token in EMPTY_BRACKETS:
        start = 0
        while True:
            idx = line.find(token, start)
            if idx < 0:
                break
            add(findings, path, lineno, idx + 1, "D-R5", "违规",
                f"空括号/空引号“{token}”", snippet_full)
            start = idx + len(token)

    for m in re.finditer(r"  +", line):
        add(findings, path, lineno, m.start() + 1, "D-R5", "提示",
            "连续空格", snippet_full)

    pos = 0
    for m in SENTENCE_SPLIT.finditer(line):
        sentence = line[pos:m.start()].strip()
        pos = m.end()
        if sentence and len(sentence) > max_sentence:
            add(findings, path, lineno, m.start() - len(sentence) + 1, "D-T1", "提示",
                f"句子 {len(sentence)} 字，超过上限 {max_sentence}", snippet_full)

    lower = line.lower()
    for word in banned_zh:
        if word in line:
            add(findings, path, lineno, line.find(word) + 1, "D-R8", "提示",
                f"黑名单词“{word}”（需人工复核是否在说人话）", snippet_full)
    for word in banned_en:
        if re.search(rf"(?<![a-z]){re.escape(word)}(?![a-z])", lower):
            add(findings, path, lineno, max(1, lower.find(word) + 1), "D-R8", "提示",
                f"banned phrase “{word}” (human review required)", snippet_full)


def dedupe(findings: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for f in findings:
        key = (f["file"], f["line"], f["col"], f["rule"], f["message"])
        if key in seen:
            continue
        seen.add(key)
        out.append(f)
    return out


def collect_inputs(paths: list[str]) -> list[Path]:
    out: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            out.extend(sorted(q for q in p.rglob("*")
                              if q.is_file() and q.suffix.lower() in TEXT_EXTS))
        elif p.is_file():
            out.append(p)
        else:
            print(f"error: input not found: {p}", file=sys.stderr)
            raise SystemExit(2)
    if not out:
        print("error: no text files found", file=sys.stderr)
        raise SystemExit(2)
    return out


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="copy_lint.py",
        description="ugliness-review copy linter (D domain, offline, deterministic).",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument("inputs", nargs="*", help="text files or directories")
    parser.add_argument("--text", help="lint a literal string instead of files")
    parser.add_argument("--max-sentence", type=int, default=60)
    parser.add_argument("--banned", default="", help="extra banned words, comma-separated")
    parser.add_argument("--no-banned", action="store_true", help="skip the blacklist")
    parser.add_argument("--strict", action="store_true", help="exit 1 on advisories too")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv)

    if not args.text and not args.inputs:
        parser.error("give at least one input file/directory, or --text")

    banned_zh = [] if args.no_banned else list(DEFAULT_BANNED_ZH)
    banned_en = [] if args.no_banned else list(DEFAULT_BANNED_EN)
    if args.banned:
        extra = [w.strip() for w in args.banned.split(",") if w.strip()]
        banned_zh.extend(w for w in extra if CJK.search(w))
        banned_en.extend(w.lower() for w in extra if not CJK.search(w))

    findings: list[dict] = []
    if args.text:
        check_line("<text>", 1, args.text, args.max_sentence, banned_zh, banned_en, findings)
    else:
        for path in collect_inputs(args.inputs):
            lines = iter_lines(path)
            in_fence = False
            in_front = bool(lines) and lines[0].strip() == "---"
            for lineno, line in enumerate(lines, 1):
                if in_front:
                    if lineno == 1:
                        continue
                    if line.strip() == "---":
                        in_front = False
                    continue
                if line.lstrip().startswith("```"):
                    in_fence = not in_fence
                    continue
                if in_fence:
                    continue
                check_line(str(path), lineno, line, args.max_sentence,
                           banned_zh, banned_en, findings)

    findings = dedupe(findings)
    violations = [f for f in findings if f["severity"] == "违规"]

    if args.json:
        print(json.dumps({"version": VERSION, "findings": findings,
                          "violations": len(violations)}, ensure_ascii=False, indent=2))
    else:
        for f in findings:
            print(f'{f["file"]}:{f["line"]}:{f["col"]} [{f["rule"]}/{f["severity"]}] '
                  f'{f["message"]} — {f["snippet"]}')
        print(f"\n{len(findings)} finding(s), {len(violations)} violation(s).")

    if violations or (args.strict and findings):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
