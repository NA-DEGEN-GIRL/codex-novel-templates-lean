---
name: codex-novel-lean
description: Use when working on a Korean web novel project built from codex-novel-templates-lean, including writing an episode, updating summaries, checking continuity, reviewing prose, or running plot-gap checks.
---

# Codex Novel Lean

Use this skill for projects that follow the `codex-novel-templates-lean` structure.

## When To Use

Trigger this skill when the task involves any of the following:

- writing a new episode
- partially rewriting an existing episode
- updating `summaries/` after manuscript changes
- checking continuity, prose quality, or Korean naturalness
- checking plot gaps, WHY/HOW gaps, or motivation/action gaps
- using `compile_brief`, `novel-calc`, or `novel-hanja` in this template

## Required Project Shape

Assume the project uses these folders when present:

- `settings/`
- `plot/`
- `summaries/`
- `chapters/`
- `reference/`

Treat `CODEX.md` as the highest-level runtime guide.

If present, also load:

- `ARC-BOUNDARY-CHECKLIST.md` for arc-end work
- `settings/07-periodic.md` for periodic review cadence
- `batch-supervisor-audit.md` when the task is audit-oriented

## Core Workflow

### 1. Load context

Prefer this order:

1. `novel-editor` MCP의 `compile_brief`
2. `summaries/running-context.md`
3. `plot/arc-XX.md`
4. `plot/foreshadowing.md`
5. `summaries/character-tracker.md`
6. previous episode ending

If the task is review-only, load only the files needed for that review.

### 2. Choose the role

Map the task to one of these roles:

- `writer`
- `continuity-reviewer`
- `narrative-reviewer`
- `korean-reviewer`
- `plot-checker`

Use the smallest role set that covers the task.

For audit or arc-end work, the minimum role bundle is usually:

- `continuity-reviewer`
- `plot-checker`
- `korean-reviewer`

### 3. Write or review

For writing:

- follow `settings/01-style-guide.md`
- follow `settings/02-episode-structure.md`
- write narrative output in Korean
- use `novel-calc` only for verification, not to drive prose
- use `novel-hanja` when Hanja naming or verification matters

For review:

- check continuity first
- then Korean naturalness
- then narrative function and repeated patterns
- then WHY/HOW and motivation-action gaps when relevant
- at arc boundaries, follow `ARC-BOUNDARY-CHECKLIST.md` in order

### 4. Update project state

After manuscript changes, update at minimum:

- `summaries/running-context.md`
- `summaries/episode-log.md`
- `summaries/character-tracker.md`

Update these only if relevant:

- `summaries/promise-tracker.md`
- `summaries/knowledge-map.md`
- `summaries/relationship-log.md`
- `summaries/decision-log.md`
- `plot/foreshadowing.md`

If a major action is completed, append one line to `summaries/action-log.md`.

If the task crosses a 5-episode boundary or arc boundary:

- update `summaries/review-log.md`
- update `summaries/repetition-watchlist.md` when repetition patterns are found
- make next-arc runway explicit in `summaries/running-context.md`

## Native MCP

Use native MCP directly.

- `compile_brief(novel_dir="/root/novel/no-title-001-gpt", episode_number=7)`
- `calculate(expression="1250 * 1.35")`
- `hanja_lookup(text="天外歸還")`

## Important Constraints

- default to Codex-only workflow; external AI review is not part of the base path
- do not bulk-read the whole project when `compile-brief` and targeted reads are enough
- do not change plot or summaries casually during review-only tasks
- do not stop at a vague "looks fine" when the task is audit or arc-boundary review; classify findings into patch-feasible vs HOLD
