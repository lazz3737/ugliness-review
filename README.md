# ugliness-review

**An agent skill that reviews visual work negatively: it finds what fails, never decides what is beautiful.**

> 美归人判，丑归 AI 判 — beauty is judged by humans; ugliness is checked by AI.

[![License: MIT](https://img.shields.io/badge/license-MIT-24292f.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-7c3aed.svg)](https://agentskills.io)

**Language: English | [简体中文](README.zh-CN.md)**

## What it is

A **pre-delivery quality gate**, not a taste consultant. It walks visual work (game art, UI, layout, web pages, slides, character animation, video, copy) and finds **enumerable defects**, returning verdicts with clause, evidence location, and fix. The final call on beauty always stays with the human.

Works where defects can be enumerated. Does not touch the final judgment of mood, style, or "premium feel" — that part is explicitly out of scope.

## Why "ugliness review" instead of "taste review"

- **Asymmetry**: beauty is scarce, subjective, and weakly shared; ugliness is common, enumerable, and broadly agreed on. When a person cannot say what is good, they can almost always point at what is off.
- **Auditability**: a negative verdict points to a location, maps to a clause, and can be re-checked. "This is beautiful" is neither refutable nor executable.
- **Floor, not ceiling**: eliminating ugliness yields "inoffensive" — not "excellent". The last step up is a human bet, not a checklist.

## How it works

1. **Mode check**: review only in delivery mode; drafts and exploration are exempt (drafts must stay wild).
2. **Pick a domain and parameters**: A art/scene · B UI/layout · C character/animation · D copy · E web · F slides/docs · G video/motion · H pixel art — plus the project's own metrics table, palette, type scale, material tiers, spec sheet, breakpoints, export specs.
3. **Collect evidence**: first-glance, squint, grayscale, silhouette wall, 64px thumbnails, tangent zoom, color sampling, frame extraction, subtitles, copy lint (see `references/evidence-kit.md`).
4. **Three-state verdict**: pass / uncertain / violation. Violations require evidence; red lines must be at zero before delivery.
5. **Re-review and legislate**: re-shoot from the same position and check item by item; verdicts the user rejects are written back into the clauses — **a rejection is training data**.

Verdict sample:

```
【A-R3】【Violation】
【Evidence】BURGER highlights are sharp and the surface shows no wear next to matte furniture; see evidence/batch2/burger_3x.png
【Fix】Unify roughness ≥ 0.75; re-check side by side with the three reference assets before intake.
```

## Scripts

Two offline, deterministic tools (Python 3.9+; the image tool needs Pillow):

```bash
pip install pillow

# Images: grayscale / blur / silhouette wall / 64px wall / dominant colors / grid / contrast
python scripts/evidence.py kit ui.png renders/ -o evidence

# Copy: punctuation / quotes / spacing / sentence length / AI-slop blacklist
python scripts/copy_lint.py copy.md
```

Evale runner: `python scripts/run_evals.py --check` validates the case file; `--sheet` generates a manual run sheet. See `scripts/README.md`.

## Install

As an Agent Skill (Claude Code / Codex / Cursor and compatible agents):

```bash
npx skills add https://github.com/lazz3737/ugliness-review --skill ugliness-review
```

As a Claude Code plugin:

```
/plugin marketplace add lazz3737/ugliness-review
/plugin install ugliness-review@ugliness-review
```

Or manually into your skills directory:

```bash
git clone https://github.com/lazz3737/ugliness-review.git
cp -r ugliness-review ~/.claude/skills/ugliness-review
```

**Claude desktop app:** the app keeps its own skill directory and does not read `~/.claude/skills`. Add the skill once through the app's skill settings; the saved entry points at this repo's absolute paths for clauses and scripts, so repo updates are picked up automatically (re-save only when `SKILL.md` itself changes).

## Repository layout

```
ugliness-review/
├── SKILL.md                        # thin entry: triggers, modes, workflow, verdict format
├── references/
│   ├── evidence-kit.md             # 19 evidence tools
│   ├── verdict-format.md           # verdict format, re-review, rejection-to-clause loop
│   └── clauses/
│       ├── README.md               # how to add a domain
│       ├── index.en.md             # English index of all clause IDs
│       ├── art-scene-props.md      # A · props & scenes
│       ├── ui-layout.md            # B · UI & layout
│       ├── character-animation.md  # C · character & animation
│       ├── copywriting.md          # D · copy
│       ├── web-pages.md            # E · web pages
│       ├── slides-docs.md          # F · slides & docs
│       ├── video-motion.md         # G · video & motion
│       ├── pixel-art.md            # H · pixel art
│       └── project-params.md       # project parameter slots
├── scripts/
│   ├── evidence.py                 # image evidence
│   ├── copy_lint.py                # copy linter
│   └── README.md
├── .claude-plugin/                 # Claude Code plugin manifests
├── examples/                       # anonymized review samples
├── cases/                          # rejection-to-clause case library
├── evals/evals.json                # trigger and behavior cases
├── CHANGELOG.md
└── LICENSE
```

## Who it's for

- Indie developers and small teams without an art director: a steady pass line before delivery.
- AI-assisted creation: let the agent self-check before delivery, instead of strangling ideas during exploration.
- Any "enumerable defects" visual deliverable: game assets, character animation, UI, web, copy, slides, video, packaging, stage production.

## Roadmap

- [x] v0.1 — concept, A/B domains, evidence kit, verdict format, eval skeleton
- [x] v0.2 — evidence scripts (silhouette / thumbnails / grayscale / blur / crop / colors / grid / contrast)
- [x] v0.2.1 — C domain: character & animation (12 R + 2 T)
- [x] v0.3 — D copy (10 R + 2 T), E web (11 R + 2 T), copy_lint
- [x] v0.4 — F slides/docs (9 R + 2 T), G video/motion (10 R + 2 T)
- [x] v0.5 — rejection case library (template + 2 seed cases)
- [x] v0.6 — Claude Code plugin marketplace packaging
- [x] v1.0 — stable clause IDs; bilingual interface; installable from the plugin marketplace
- [x] v1.1 — H pixel art (8 R + 2 T), added from the first external playtest

## Contributing

New domains, sharper "what violations look like", and anonymized cases are welcome. Minimum requirements for a new domain: `references/clauses/README.md`.

One rule: **add only "what counts as failing", never "what counts as good".**

## License

[MIT](LICENSE)
