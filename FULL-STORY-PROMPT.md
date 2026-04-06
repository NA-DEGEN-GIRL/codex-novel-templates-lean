# Codex Full Story Prompt

> `/root/novel/`에서 Codex를 열고, 이미 셋업된 소설 프로젝트 안에서 아래 프롬프트를 붙여넣는다.
> 목표는 `plot/`과 `settings/`를 바탕으로 프로젝트 전용 `full_story.md`를 생성하거나 갱신하는 것이다.
> 이 작업은 초기 설계 품질에 직접 영향을 주므로 `high` 이상, 가능하면 `xhigh` effort를 권장한다.

## Usage

```bash
cd /root/novel/no-title-XXX && codex
```

Paste the prompt below and replace only the bracketed value.

## Prompt

```text
현재 `/root/novel/no-title-XXX` 소설 프로젝트의 `plot/`과 `settings/`를 전부 읽고, 집필용 통합 줄거리 문서 `full_story.md`를 작성해줘.

## Target

- project: [no-title-XXX]

## Priority

- `CODEX.md`가 있으면 최우선으로 반영한다.
- `CODEX.md`가 없고 `CLAUDE.md`만 있으면 그것을 fallback 기준으로 쓴다.
- 이 문서는 홍보용 시놉시스가 아니라, 집필 전에 전체 구조와 감정선을 다시 붙잡기 위한 writer-facing story brief다.

## Goal

- `plot/`과 `settings/`만으로도 전체 이야기를 추적할 수 있는 통합 줄거리 문서를 만든다.
- 결과물은 짧은 홍보 문구가 아니라, 집필 전에 전체 구조와 감정선을 한 번에 떠올릴 수 있는 충분히 상세한 story brief 여야 한다.
- 문서는 재미있게 읽히되, 설정 문서로도 바로 쓸 수 있어야 한다.
- 결과물만 읽어도, 소설 본문을 읽지 않은 사람이 전체 줄거리, 주요 반전, 관계 변화, 결말의 의미를 이해할 수 있어야 한다.

## Files to read first

- `CODEX.md`
- `CLAUDE.md` (if present and `CODEX.md` is missing or supplementary)
- `full_story.md` (if already present)
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

## Work sequence

1. 먼저 작품의 중심축을 정리한다.
   - 주인공의 출발 상태와 결핍
   - 핵심 갈등과 장르적 약속
   - 각 아크가 무엇을 확대하는지
   - 결말에서 무엇이 바뀌는지
2. 아크별 인과 사슬을 정리한다.
   - 시작 상태
   - 압박과 에스컬레이션
   - 반전/폭로
   - 관계 변화
   - 다음 아크로 이어지는 런웨이
3. 비어 있거나 불확실한 구간은 추측으로 메우지 말고, plot이 허용하는 범주 안에서 정리한다.
4. 그 결과를 `full_story.md`로 통합 작성한다.
5. 구조적 공백이 보이면 마지막에 짧게 메모한다.

## Rules

- If `full_story.md` already exists, read it first and replace it with a stronger version. 이어붙이지 말고 전면 갱신하라.
- Do not invent concrete facts that are not supported by `plot/` or `settings/`.
- 불확실한 대목은 없는 사실을 확정하지 말고, "이 축으로 전개된다", "이 시점부터 압박이 커진다" 같은 범주형 표현으로 낮춰라.
- Do not write this as a bullet-only outline. Use readable Korean prose paragraphs.
- However, keep it as a project document, not as novel prose.
- 실제 `plot` 구조에 맞춰 써라. 억지로 3부 구조를 고정하지 말고, 있는 프롤로그/아크/에필로그를 기준으로 섹션을 잡아라.
- 각 아크/부 섹션에서는 반드시 아래가 보여야 한다.
  - 주인공이 무엇을 원했는가
  - 무엇이 그것을 막는가
  - 어떤 반전/폭로가 상황을 바꾸는가
  - 누가 어떻게 변하는가
  - 왜 다음 단계로 넘어갈 수밖에 없는가
- Make the arc progression clear: what changes, what escalates, what is revealed, what each major character does.
- Integrate theme, emotion, and worldbuilding instead of treating them as separate checklists.
- When explaining twists or foreshadowing payoffs, focus on causality and narrative effect.
- Do not stop at listing events; explain why events matter, how they change the characters, and why the final choice lands.
- 인물 관계 변화는 라벨만 적지 말고, 무엇이 그 변화를 촉발했고 이후 장면에 어떤 압력을 만드는지까지 쓴다.
- 화수 나열식 요약으로 흐르지 마라. 꼭 필요한 경우가 아니면 episode-by-episode summary 대신 arc-level causal narrative를 우선한다.
- 복선은 표처럼 건조하게 모으지 말고, 어디에 심기고 어떻게 정서적/서사적으로 회수되는지 설명하라.
- 문서는 한국어로 쓴다.
- Do not include an explanatory lead-in or quote block such as:
  `plot/`, `settings/`, `CLAUDE.md`를 바탕으로 정리한 작품 전체 줄거리.
  단순 시놉시스가 아니라, 작품의 장르적 재미, 정체성 미스터리, 감정축, 우주적 스케일, 마지막 선택까지 모두 한 번에 읽히도록 상세하게 서술한다.
- Start the file directly with the title or first real section.

## Recommended structure

1. 작품 개요
2. 핵심 갈등과 감정축
3. 프롤로그 또는 도입부
4. 아크별 전체 줄거리
5. 결말 또는 에필로그
6. 복선과 회수의 큰 흐름
7. 이 이야기의 재미 포인트

## Output quality bar

- 결과물만 읽어도 다음이 바로 보여야 한다.
  - 이 작품은 무엇을 약속하는가
  - 어디서 판이 커지는가
  - 어떤 관계가 핵심으로 변하는가
  - 어떤 진실이 언제 드러나는가
  - 마지막 선택이 왜 중요한가
- 읽고 나면 집필자가 "전체 구조를 다시 머리에 올렸다"는 느낌이 들어야 한다.
- generic synopsis나 메모 묶음처럼 보이면 실패다.

## Final task

- Write the result to `full_story.md` in the project root.
- Overwrite the existing file if needed.
- Do not modify other files unless the user explicitly asks for setting/plot updates.
- If you notice major structural gaps while reading, mention them briefly after writing the file, but keep the main task focused on `full_story.md`.
```
