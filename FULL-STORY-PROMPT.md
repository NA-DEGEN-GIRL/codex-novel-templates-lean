# Codex Full Story Prompt

> `/root/novel/`에서 Codex를 열고, 이미 셋업된 소설 프로젝트 안에서 아래 프롬프트를 붙여넣는다.
> 목표는 `plot/`과 `settings/`를 바탕으로 프로젝트 전용 `full_story.md`를 생성하거나 갱신하는 것이다.

## Usage

```bash
cd /root/novel/[project] && codex
```

Paste the prompt below and replace only the bracketed value.

## Prompt

```text
현재 소설 프로젝트의 `plot/`과 `settings/`를 전부 읽고, 작품 전체 줄거리를 정리한 `full_story.md`를 작성해줘.

## Target

- project: [no-title-XXX]

## Goal

- `plot/`과 `settings/`만으로도 전체 이야기를 추적할 수 있는 통합 줄거리 문서를 만든다.
- 결과물은 짧은 홍보 문구가 아니라, 집필 전에 전체 구조와 감정선을 한 번에 떠올릴 수 있는 상세한 story brief 여야 한다.
- 문서는 재미있게 읽히되, 설정 문서로도 바로 쓸 수 있어야 한다.
- The result should be detailed enough that someone who has not read the novel itself can still understand the full plot, major reversals, relationship changes, and ending.

## Files to read first

- `CODEX.md`
- `plot/prologue.md` (if present)
- `plot/master-outline.md`
- `plot/arc-*.md`
- `plot/foreshadowing.md`
- `plot/timeline.md` (if present)
- `settings/01-style-guide.md`
- `settings/02-episode-structure.md`
- `settings/03-characters.md`
- `settings/04-worldbuilding.md`
- `settings/05-continuity.md`
- `settings/06-humor-guide.md` (if present)
- `settings/07-periodic.md`

## Rules

- If `full_story.md` already exists, read it first and replace it with a stronger version.
- Do not invent concrete facts that are not supported by `plot/` or `settings/`.
- Do not write this as a bullet-only outline. Use readable Korean prose paragraphs.
- However, keep it as a project document, not as novel prose.
- Make the arc progression clear: what changes, what escalates, what is revealed, what each major character does.
- Integrate theme, emotion, and worldbuilding instead of treating them as separate checklists.
- When explaining twists or foreshadowing payoffs, focus on causality and narrative effect.
- Do not stop at listing events; explain why events matter, how they change the characters, and why the final choice lands.
- Do not include an explanatory lead-in or quote block such as:
  `plot/`, `settings/`, `CLAUDE.md`를 바탕으로 정리한 작품 전체 줄거리.
  단순 시놉시스가 아니라, 작품의 장르적 재미, 정체성 미스터리, 감정축, 우주적 스케일, 마지막 선택까지 모두 한 번에 읽히도록 상세하게 서술한다.
- Start the file directly with the title or first real section.

## Recommended structure

1. 작품 개요
2. 프롤로그
3. 1부 전체 줄거리
4. 2부 전체 줄거리
5. 3부 전체 줄거리
6. 에필로그
7. 이 이야기의 재미 포인트

## Final task

- Write the result to `full_story.md` in the project root.
- Overwrite the existing file if needed.
- Do not modify other files unless the user explicitly asks for setting/plot updates.
- If you notice major structural gaps while reading, mention them briefly after writing the file, but keep the main task focused on `full_story.md`.
```
