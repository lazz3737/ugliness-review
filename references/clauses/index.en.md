# Clause index (English)

> The clauses themselves are written in Chinese in the linked files. This index gives every clause ID and a one-line summary so English readers can navigate the system and ask an agent to translate any specific clause on demand.
> **Clause IDs are stable since v1.0** — they are never renumbered or reused. Deprecated clauses are marked `(deprecated)` instead of removed.

## A · Props & scenes — `art-scene-props.md`

- **A-R1** One ruler: all assets normalized to a project metrics table (character height = 1.0).
- **A-R2** Form follows function: a prop's purpose must be guessable without its name.
- **A-R3** One material dialect: roughness / highlight / grain consistent across assets.
- **A-R4** Contact & grounding: soft contact shadows, no floating, no interpenetration, no "kissing" tangents.
- **A-R5** Detail budget 80/15/5, with visual rest areas on every screen.
- **A-R6** Color restraint: 60-30-10, saturated area ≤15%, one signal color on duty.
- **A-R7** Silhouette and 64px readability.
- **A-R8** Narrative consistency: provenance and wear.
- **A-R9** No tangents: overlap clearly or separate clearly.
- **A-T1** Clustering rhythm: no evenly spaced scatter.

## B · UI & layout — `ui-layout.md`

- **B-R1** One focal element per screen.
- **B-R2** 3–4 type sizes with ≥1.4× steps.
- **B-R3** At most two font families; no emoji as icons.
- **B-R4** Chinese typography details (line height, spacing, punctuation).
- **B-R5** Grid and alignment (8pt grid).
- **B-R6** Whitespace budget.
- **B-R7** UI colors share the world's palette.
- **B-R8** The cheap five (gradients, blurry shadows, glow text, pill soup, emoji icons): 2+ hits = rework.
- **B-R9** One layout grammar: any two screens read as two pages of one publication.
- **B-T1** Paper / print texture matches the art.

## C · Character & animation — `character-animation.md`

- **C-R1** Spec-sheet consistency (proportions, hand type, poly budget).
- **C-R2** Key-pose silhouette readability.
- **C-R3** Hand–prop contact, including mitten hands with magnetic attachment.
- **C-R4** Deformation and volume: no collapse, candy-wrap, or spikes.
- **C-R5** Anatomical reach: measure mouth–hand–prop distances before animating.
- **C-R6** Arcs, anticipation, follow-through; hands and feet lag 2–3 frames.
- **C-R7** Timing and easing: fast–hold–slow, never uniform.
- **C-R8** Squash & stretch and overshoot; squash frames on landing/sitting.
- **C-R9** Foot contact: no sliding, floating, or ground clipping.
- **C-R10** Seamless loops and living idle (breath, weight shift, gaze).
- **C-R11** No clipping or self-intersection in any frame.
- **C-R12** Expression and gaze consistency; perform to camera.
- **C-T1** Character-specific motion, not stock templates.
- **C-T2** Secondary motion for hair/accessories; no fake springs without separate parts.

## D · Copy — `copywriting.md`

- **D-R1** User language, not system language.
- **D-R2** One word per concept across the whole flow.
- **D-R3** CTA names the outcome, not "Submit".
- **D-R4** Actionable errors and empty states (what happened + what to do).
- **D-R5** Chinese punctuation, spacing, and quote style.
- **D-R6** Consistent terminology and pronouns.
- **D-R7** One voice; humor and cuteness in moderation.
- **D-R8** No filler (deletion test) and an AI-slop blacklist.
- **D-R9** Scannable hierarchy: headline carries the conclusion.
- **D-R10** Facts and numbers discipline; no fabricated data.
- **D-T1** Sentence length and jargon limits.
- **D-T2** Localization details (variants, date/unit formats).

## E · Web pages — `web-pages.md`

- **E-R1** The first screen answers what / for whom / next step within 5 seconds.
- **E-R2** One section, one claim, completed within one screen height.
- **E-R3** Responsive at 390 / 768 / 1440: no horizontal scroll, clipping, or overlap.
- **E-R4** State coverage: hover / focus / active / disabled; loading / error / empty / success.
- **E-R5** Accessibility floor: contrast, keyboard access, visible focus, alt text, reduced motion.
- **E-R6** Touch targets ≥44×44px with spacing.
- **E-R7** Real content; placeholders explicitly labeled.
- **E-R8** Stability and performance: reserved image sizes, font loading, no layout jumps.
- **E-R9** Navigation and orientation: current location visible, deep links work.
- **E-R10** Forms: persistent labels, inline errors, no data loss.
- **E-R11** Template-fingerprint blacklist; 2+ hits = rework.
- **E-T1** Motion restraint: one orchestrated moment per screen.
- **E-T2** Visuals, type, and copy share one voice.

## F · Slides & docs — `slides-docs.md`

- **F-R1** One assertion per slide; the title is the conclusion, not a topic label.
- **F-R2** Assertion–evidence pairing on every slide.
- **F-R3** Page density: one claim, ≤5 support points, ≤6 lines.
- **F-R4** Readable type sizes: projection body ≥24pt, doc body 10.5–12pt.
- **F-R5** Chart discipline: axes from zero or marked truncation; no 3D pies or dual-axis tricks.
- **F-R6** Master and grid: four page types, consistent margins and footers.
- **F-R7** Hierarchy and emphasis: three levels, ≤2 emphases per slide.
- **F-R8** Facts and sources on every number.
- **F-R9** Delivery readiness: fonts embedded or PDF backup, images embedded, clean naming.
- **F-T1** Speaker notes: cues, not a script.
- **F-T2** Chinese typography follows D-R5.

## G · Video & motion — `video-motion.md`

- **G-R1** Every animation has a motive (feedback / guidance / relation / status).
- **G-R2** Restrained parameters: duration tiers, small distances, deliberate easing, no default linear.
- **G-R3** One hero motion per screen; staggered entrances only with a logic.
- **G-R4** Accessibility and performance: reduced motion, transform/opacity only, keyboard parity.
- **G-R5** The first 3 seconds state the topic; no logo intro or black frames.
- **G-R6** Pacing and cuts: an information change every 3–5 seconds; transitions serve the story.
- **G-R7** Subtitles and safe area: ≤16 characters per line, ≥1.5s dwell, clear of UI chrome, zero typos.
- **G-R8** Audio-visual sync within 1–2 frames; voice never buried by music.
- **G-R9** Frame readability: any key frame can stand alone and serve as a cover.
- **G-R10** Assets and licensing: authorized or self-made; AI assets labeled.

- **G-T1** One look across the piece: palette, type, subtitle style, transitions.
- **G-T2** Export specs per platform; no stretching across aspect ratios.

## H · Pixel art — `pixel-art.md`

- **H-R1** Integer scaling and pixel grid; nearest-neighbor only.
- **H-R2** One pixel density (PPU) across assets and UI.
- **H-R3** One outline strategy: all / selective / none; 1px, palette colors.
- **H-R4** Fixed palette (e.g. ≤32 colors); dithering instead of gradients.
- **H-R5** No anti-aliasing or sub-pixel movement.
- **H-R6** Pixel font at integer multiples of its native size.
- **H-R7** Silhouette and ≥15% luminance contrast; readable at 64px.
- **H-R8** One frame rate and frame count; integer-pixel motion.
- **H-T1** Consistent dithering patterns.
- **H-T2** Style purity: no vector / 3D / photo assets mixed in.
