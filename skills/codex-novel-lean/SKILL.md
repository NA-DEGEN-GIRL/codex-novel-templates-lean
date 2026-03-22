---
name: codex-novel-lean
description: Use when working on a Korean web novel project built from codex-novel-templates-lean, including writing an episode, updating summaries, checking continuity, reviewing prose, running plot-gap checks, or migrating a Claude novel project to the Codex lean workflow.
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
- migrating a Claude-based novel project to Codex lean
- using `compile_brief`, `novel-calc`, or `novel-hanja` in this template

## Required Project Shape

Assume the project uses these folders when present:

- `settings/`
- `plot/`
- `summaries/`
- `chapters/`
- `reference/`

Treat `CODEX.md` as the highest-level runtime guide. If the project still has `CLAUDE.md`, use it as reference only unless the user explicitly says the project is still Claude-driven.

## Core Workflow

### 1. Load context

Prefer this order:

1. `scripts/compile-brief <novel_dir> <episode_number>`
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

Do not recreate the full Claude agent matrix. Use the smallest role set that covers the task.

### 3. Write or review

For writing:

- follow `settings/01-style-guide.md`
- follow `settings/02-episode-structure.md`
- write narrative output in Korean
- use `scripts/novel-calc` only for verification, not to drive prose
- use `scripts/novel-hanja` when Hanja naming or verification matters

For review:

- check continuity first
- then Korean naturalness
- then narrative function and repeated patterns

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

## Local Tools

Use the bundled wrappers instead of assuming MCP is attached.

### compile brief

```bash
scripts/compile-brief /root/novel/no-title-001-gpt 7
```

### calc

```bash
scripts/novel-calc calculate expression='1250 * 1.35'
scripts/novel-calc date_calc --json '{"date_str":"2026-03-22","operation":"add","days":3}'
```

### hanja

```bash
scripts/novel-hanja hanja_lookup text='天外歸還'
scripts/novel-hanja hanja_search reading='검' meaning_hint='칼'
```

## Migration Rule

When migrating from a Claude project:

- do not modify `chapters/` unless the user asked for text changes
- preserve worldbuilding meaning and character rules
- translate runtime guidance into Codex workflow rather than copying `.claude/commands`
- prefer shallow migration first, automation later

## Important Constraints

- default to Codex-only workflow; external AI review is not part of the base path
- do not assume `.claude/agents/*.md` are executable in Codex
- do not bulk-read the whole project when `compile-brief` and targeted reads are enough
- do not change plot or summaries casually during review-only tasks
