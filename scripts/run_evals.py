#!/usr/bin/env python3
"""ugliness-review eval runner.

Modes:
  --check   validate evals/evals.json structure
  --sheet   generate a manual run sheet (Markdown) for a fresh session
  --run     run each case through the Claude CLI when it is installed

Examples:
  python scripts/run_evals.py --check
  python scripts/run_evals.py --sheet
  python scripts/run_evals.py --sheet --out evals/run_sheet.md
  python scripts/run_evals.py --run --limit 3 --timeout 180

Trigger cases must be run in a **fresh** session: skills are loaded at session
start, so a session opened before installation cannot test triggering.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

VERSION = "0.1.0"
ALLOWED_TYPES = {"should_trigger", "should_not_trigger", "behavior"}
DEFAULT_EVALS = Path(__file__).resolve().parent.parent / "evals" / "evals.json"


def die(msg: str, code: int = 2) -> "NoReturn":
    print(f"error: {msg}", file=sys.stderr)
    raise SystemExit(code)


def load_evals(path: Path) -> dict:
    if not path.is_file():
        die(f"evals file not found: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        die(f"invalid JSON in {path}: {exc}")
    return data


def validate(data: dict) -> tuple[list[str], list[dict]]:
    errors: list[str] = []
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("top-level 'cases' must be a non-empty list")
        return errors, []
    seen: set[int] = set()
    clean: list[dict] = []
    for i, case in enumerate(cases, 1):
        where = f"case #{i}"
        if not isinstance(case, dict):
            errors.append(f"{where}: not an object")
            continue
        cid = case.get("id")
        if not isinstance(cid, int):
            errors.append(f"{where}: 'id' must be an integer")
        elif cid in seen:
            errors.append(f"{where}: duplicate id {cid}")
        else:
            seen.add(cid)
        ctype = case.get("type")
        if ctype not in ALLOWED_TYPES:
            errors.append(f"{where}: type must be one of {sorted(ALLOWED_TYPES)}")
        for key in ("prompt", "expected"):
            if not isinstance(case.get(key), str) or not case[key].strip():
                errors.append(f"{where}: '{key}' must be a non-empty string")
        assertions = case.get("assertions")
        if not isinstance(assertions, list) or not assertions:
            errors.append(f"{where}: 'assertions' must be a non-empty list")
        elif any(not isinstance(a, str) or not a.strip() for a in assertions):
            errors.append(f"{where}: every assertion must be a non-empty string")
        clean.append(case)
    if not any(c.get("type") == "should_trigger" for c in clean):
        errors.append("at least one should_trigger case is required")
    if not any(c.get("type") == "should_not_trigger" for c in clean):
        errors.append("at least one should_not_trigger case is required")
    return errors, clean


def summarize(cases: list[dict]) -> str:
    counts = {t: sum(1 for c in cases if c.get("type") == t) for t in sorted(ALLOWED_TYPES)}
    return ", ".join(f"{k}={v}" for k, v in counts.items())


def build_sheet(data: dict, cases: list[dict]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Eval run sheet — {now}",
        "",
        f"- skill: `{data.get('skill', '?')}`",
        f"- evals version: {data.get('version', '?')}",
        f"- cases: {len(cases)}（{summarize(cases)}）",
        "",
        "## How to run",
        "",
        "1. **每条用例单独开一个全新会话**（skill 在会话启动时加载；连续跑时前一条会预热 skill，触发测试只能算宽松通过）。",
        "2. 逐条把 prompt 原样粘贴，**不要提示“用审丑 skill”**。",
        "3. 对照断言勾选；触发类只看“有没有按判词格式回应”，不要看它说得好不好。",
        "4. 结果填在本表；失败项写一句原因，回头修订 description 或条款。",
        "5. 建议顺序：先跑 3、4、6、8（轻，几十秒一条），再跑带图的 1、2、5，最后 7、9、10（依赖上下文）。",
        "",
        "判定提示：",
        "",
        "- `should_trigger`：应出现四段式判词（条款 / 判定 / 证据 / 修法）或明确进入交付判卷。",
        "- `should_not_trigger`：不应出现条款编号，不应主动判卷。",
        "- `behavior`：按断言逐条勾，不看措辞。",
        "",
        "## Summary",
        "",
        "| # | type | prompt | result | notes |",
        "| --- | --- | --- | --- | --- |",
    ]
    for c in cases:
        prompt = c["prompt"].replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {c['id']} | {c['type']} | {prompt} | ☐ pass ☐ fail |  |")
    lines.append("")
    for c in cases:
        lines += [
            f"## Case {c['id']} · {c['type']}",
            "",
            "**Prompt**（原样粘贴）：",
            "",
            "```text",
            c["prompt"],
            "```",
            "",
            f"**期望**：{c['expected']}",
            "",
            "**断言**：",
            "",
        ]
        lines += [f"- [ ] {a}" for a in c["assertions"]]
        lines += [
            "",
            "**结果**：☐ 通过  ☐ 失败",
            "",
            "**备注**：",
            "",
            "---",
            "",
        ]
    return "\n".join(lines)


def cmd_check(data: dict) -> int:
    errors, cases = validate(data)
    if errors:
        print("INVALID:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"OK: {len(cases)} cases（{summarize(cases)}）")
    return 0


def cmd_sheet(data: dict, out: Path) -> int:
    errors, cases = validate(data)
    if errors:
        print("INVALID:")
        for e in errors:
            print(f"  - {e}")
        return 1
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build_sheet(data, cases), encoding="utf-8")
    print(f"sheet -> {out}")
    return 0


def cmd_run(data: dict, args: argparse.Namespace) -> int:
    errors, cases = validate(data)
    if errors:
        print("INVALID:")
        for e in errors:
            print(f"  - {e}")
        return 1
    claude = shutil.which("claude")
    if not claude:
        die(
            "Claude CLI not found. Install it (`npm i -g @anthropic-ai/claude-code`) "
            "or use `--sheet` and run the cases manually in a fresh session.",
            code=2,
        )
    if args.only:
        wanted = {int(x) for x in args.only.split(",") if x.strip()}
        cases = [c for c in cases if c["id"] in wanted]
    if args.limit:
        cases = cases[: args.limit]
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    run_dir = Path(args.out_dir) / stamp
    run_dir.mkdir(parents=True, exist_ok=True)
    results = [
        f"# Eval run — {stamp}",
        "",
        f"- skill: `{data.get('skill', '?')}`",
        f"- cases run: {len(cases)}",
        "",
    ]
    for c in cases:
        print(f"running case {c['id']} ({c['type']})…")
        try:
            proc = subprocess.run(
                [claude, "-p", c["prompt"]],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=args.timeout,
            )
            output = proc.stdout.strip() or proc.stderr.strip()
            status = "ok" if proc.returncode == 0 else f"exit {proc.returncode}"
        except subprocess.TimeoutExpired:
            output = f"(timeout after {args.timeout}s)"
            status = "timeout"
        case_file = run_dir / f"case-{c['id']:02d}.md"
        case_file.write_text(
            "\n".join(
                [
                    f"# Case {c['id']} · {c['type']}",
                    "",
                    "## Prompt",
                    "",
                    "```text",
                    c["prompt"],
                    "```",
                    "",
                    "## Expected",
                    "",
                    c["expected"],
                    "",
                    "## Output",
                    "",
                    "```text",
                    output,
                    "```",
                    "",
                    "## Verdict",
                    "",
                    "☐ pass  ☐ fail",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        results += [
            f"## Case {c['id']} · {c['type']} — {status}",
            "",
            f"- prompt: `{c['prompt'][:60]}`",
            f"- output: `case-{c['id']:02d}.md`",
            "",
        ]
    (run_dir / "results.md").write_text("\n".join(results), encoding="utf-8")
    print(f"run -> {run_dir}（人工判卷后填 results.md）")
    return 0


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="run_evals.py",
        description="ugliness-review eval runner (validate / sheet / run).",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument("--evals", default=str(DEFAULT_EVALS), help="path to evals.json")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="validate evals.json")
    mode.add_argument("--sheet", action="store_true", help="generate a manual run sheet")
    mode.add_argument("--run", action="store_true", help="run cases via Claude CLI")
    parser.add_argument("--out", help="sheet output path (default: evals/run_sheet.md)")
    parser.add_argument("--out-dir", default="evals/runs", help="run output directory")
    parser.add_argument("--only", help="comma-separated case ids")
    parser.add_argument("--limit", type=int, help="run only the first N cases")
    parser.add_argument("--timeout", type=int, default=180, help="per-case timeout (s)")
    args = parser.parse_args(argv)

    data = load_evals(Path(args.evals))
    if args.check:
        raise SystemExit(cmd_check(data))
    if args.sheet:
        out = Path(args.out) if args.out else Path(args.evals).parent / "run_sheet.md"
        raise SystemExit(cmd_sheet(data, out))
    raise SystemExit(cmd_run(data, args))


if __name__ == "__main__":
    main()
