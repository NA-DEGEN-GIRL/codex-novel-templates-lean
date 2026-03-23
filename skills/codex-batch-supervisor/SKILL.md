---
name: codex-batch-supervisor
description: Use when supervising a tmux-based Codex writing session for a novel project, including checking session state, sending the next episode prompt, verifying chapter completion, handling arc transitions, and running Codex-only batch supervision for codex-novel-templates-lean projects.
---

# Codex Batch Supervisor

Use this skill when Codex is acting as the supervisor of another Codex writer session.

## When To Use

Trigger this skill when the task involves:

- monitoring a tmux writing session
- sending the next episode prompt to a writer session
- checking whether an episode finished correctly
- handling stalled or errored writer sessions
- forcing arc-transition checks and summary maintenance
- running a batch writing session over many episodes

## Required Inputs

Before supervising, identify:

- novel directory
- tmux session name
- episode range
- arc mapping
- writer launch command

If these are not explicitly provided, discover them from the project before acting.

## Source Files

Read these first:

1. `batch-supervisor.md`
2. `CODEX.md`
3. `settings/07-periodic.md`
4. `ARC-BOUNDARY-CHECKLIST.md`
4. `plot/arc-XX.md` for the current episode when needed

Only read more if blocked.

## Core Loop

### 1. Check session state

Use tmux capture to classify the writer session:

- working
- waiting
- error
- stalled
- completed

Do not assume a visible prompt means success. Verify artifacts.

### 2. Send writing prompt

When the writer is ready for the next episode:

- send the episode prompt
- require context loading via `novel-editor` MCP `compile_brief`
- determine and inject the correct review floor
- require summary updates
- require action-log append

### 3. Verify completion

Treat an episode as complete only when all are true:

1. chapter file exists
2. required summaries were updated
3. `summaries/action-log.md` records the work

If one is missing, do not advance blindly.

### 4. Handle arc transitions

At arc boundaries, require:

- completed arc re-read
- WHY/HOW and motivation-action gap check
- POV / era / scene-logic check
- repetition and Korean naturalness check
- minimal patching or HOLD classification
- next arc readiness check
- review-log and action-log updates

### 5. Keep the pipeline Codex-only

Do not require external AI review.
Use native MCP and direct file verification instead.

## Commands And Tools

Prefer:

- `tmux capture-pane`
- `tmux send-keys`
- `novel-editor` MCP `compile_brief`
- direct reads of `summaries/`, `plot/`, and `chapters/`

Use `novel-calc` or `novel-hanja` only if the writer task genuinely needs them.

## Failure Handling

If the writer session stalls:

- verify whether the model is still producing output
- check if it is waiting for input
- send a short continuation or recovery prompt
- avoid resetting context unless clearly necessary

If the session crashed:

- recreate the tmux session
- determine the last completed episode from files, not memory
- resume from the next unfinished episode

If the writer finished the last episode of an arc but stopped before the checklist:

- do not advance
- send the arc-boundary audit prompt
- verify `review-log.md` and next-arc runway before marking complete

## Constraint

The supervisor is an orchestrator, not the primary writer.

- It may inspect files and send prompts.
- It should not silently rewrite large parts of the novel itself unless the user explicitly changes the task.
