# Codex Novel Templates -- Lean Edition

Codex 중심으로 한국어 웹소설 프로젝트를 운영하기 위한 템플릿.

이 템플릿은 Codex native MCP와 Codex self-review를 기준으로 바로 쓰는 운영 분기다.

## Shared Settings Layer

이 템플릿의 `settings/`는 [claude-codex-novel-templates-hybrid](/root/novel/claude-codex-novel-templates-hybrid/settings), [claude-novel-templates-lean](/root/novel/claude-novel-templates-lean/settings)와 **동일한 공통 집필 레이어**다.

- `settings/`는 일반 소설과 웹소설 모두에 적용되는 문체, 캐릭터, 연속성, 정기 점검 규약을 담는다.
- `CODEX.md`와 `batch-supervisor.md`는 Codex 런타임의 실행 방식만 정의한다.
- 문학 규칙은 세 템플릿이 공유하고, 런타임 차이만 상위 문서에서 갈라진다.

## What This Is

- 한국어 웹소설용 프로젝트 스캐폴드
- Codex 기준 운영 문서 세트
- Codex-only self-review / audit / supervisor workflow
- Codex native MCP workflow
- fresh session / auto-compact에도 버티는 carry-forward continuity workflow
- Codex skill 기반 보조 워크플로

## What This Is Not

- 특정 에디터 전용 command 체계의 1:1 복제품
- 외부 AI 리뷰를 기본 전제로 하는 파이프라인
- wrapper script를 기본 경로로 두는 템플릿

## Design Principles

1. `settings/`는 세 템플릿이 공유하는 집필 규약이고, `CODEX.md`와 `batch-supervisor.md`는 Codex 런타임 레이어다.
2. 집필, 정기 점검, 아크 경계 감사를 Codex 내부에서 닫힌 루프로 돌린다.
3. 모든 MCP가 등록되어 있다고 가정하고 native MCP를 기본 경로로 사용한다.
4. 역할은 문서와 체크리스트로 압축하고, 과도한 agent 분해를 피한다.
5. supervisor와 auditor가 파일 기반으로 완료를 검증한다.
6. 다음 화 오프닝 continuity를 위해 `compile_brief`와 `running-context`의 carry-forward 앵커를 강하게 유지한다.

## Repository Layout

- `CODEX.md`
  - Codex용 최상위 운영 규약
- `ARC-BOUNDARY-CHECKLIST.md`
  - 아크 종료 후 필수 감사 절차
- `batch-supervisor.md`
  - tmux writer 감독 문서
- `batch-supervisor-audit.md`
  - tmux auditor 감독 문서
- `INIT-PROMPT.md`
  - 새 프로젝트 시작 프롬프트
- `PLOT-REINFORCEMENT-PROMPT.md`
  - 초기 `plot/`을 집필 직전 수준으로 강화하는 프롬프트
- `FULL-STORY-PROMPT.md`
  - `plot/`과 `settings/`를 바탕으로 전체 줄거리를 정리하는 프롬프트
- `AGENT-MAP.md`
  - 참고용 역할 압축 메모
- `skills/`
  - Codex skill 정의
- `settings/`, `plot/`, `summaries/`, `chapters/`, `reference/`
  - 소설 자산 구조

## Workflow

기본 집필 흐름:

1. `novel-editor` MCP의 `compile_brief`로 맥락 로드
2. `직전 화 직결 앵커` + 마지막 장면 확인
3. planning flags + WHY/HOW 질문 정리
4. 초안 작성
5. review floor에 맞는 self-review
6. `Immediate Carry-Forward` 포함 summary / plot / action-log 갱신
7. `dialogue-log`와 `knowledge-map`으로 보이스/정보 continuity 보강
8. supervisor가 `/root/novel/config.json`에 화 정보를 반영

정기 점검 흐름:

1. 최근 5화 재독
2. summary consistency
3. WHY/HOW + motivation-action gap
4. POV / era / scene logic
5. repetition
6. Korean naturalness
7. summary 재정합 + 로그

아크 경계 흐름:

1. [ARC-BOUNDARY-CHECKLIST.md](/root/novel/codex-novel-templates-lean/ARC-BOUNDARY-CHECKLIST.md) 수행
2. patch-feasible를 repair batch로 즉시 수정
3. HOLD를 `retro-fix / forward-fix / plot-repair / user-escalation`으로 분류
4. 다음 아크 런웨이 정리

## Skills

포함된 skill:

- [skills/codex-novel-lean/SKILL.md](/root/novel/codex-novel-templates-lean/skills/codex-novel-lean/SKILL.md)
- [skills/codex-batch-supervisor/SKILL.md](/root/novel/codex-novel-templates-lean/skills/codex-batch-supervisor/SKILL.md)

현재 skill은 아래 작업을 포괄한다.

- 에피소드 집필
- 부분 재작성
- continuity / narrative / Korean review
- WHY/HOW / motivation-action / OAG 점검
- tmux batch supervision

`skills`는 실제 Codex skill 시스템을 쓰는 환경에서 유효하다. 반대로 [AGENT-MAP.md](/root/novel/codex-novel-templates-lean/AGENT-MAP.md)는 런타임 필수 문서가 아니라 참고 문서다.

## Supported MCP

- `novel-editor`
- `novel-calc`
- `novel-hanja`
- `novel-naming`

native MCP 예시:

- `compile_brief(novel_dir="/root/novel/no-title-001-gpt", episode_number=7)`
- `calculate(expression="1250 * 1.35")`
- `hanja_lookup(text="天外歸還")`
- `naming_check(novel_dir="/root/novel/no-title-001-gpt", episode_range="1-10")`

## MCP Assumption

현재 lean은 Codex에서 필요한 MCP를 등록한 환경을 기본 전제로 둔다.

- `novel-editor`
- `novel-calc`
- `novel-hanja`
- `novel-naming`

등록만 되어 있으면 writer와 supervisor는 native MCP를 직접 사용할 수 있다.

## Quick Start

1. 이 레포를 `/root/novel/no-title-XXX` 형식의 새 프로젝트 폴더로 복사한다.
   - `XXX`는 3자리 숫자다. 이미 존재하면 다음 사용 가능한 번호를 쓴다.
2. `INIT-PROMPT.md`를 기준으로 `CODEX.md`와 `settings/`를 채운다.
   - 특히 `settings/01-style-guide.md`, `settings/03-characters.md`, `settings/05-continuity.md`, `settings/07-periodic.md`를 먼저 채운다.
   - `INIT-PROMPT.md`는 먼저 컨셉 3안을 제시하고, 사용자가 하나를 고른 뒤에만 프로젝트 생성으로 넘어가게 한다.
   - 이 단계에서 `/root/novel/config.json`의 새 소설 entry와 빈 `parts`도 함께 만든다.
3. `PLOT-REINFORCEMENT-PROMPT.md`로 `plot/`을 집필 직전 수준으로 강화한다.
4. 필요하면 `FULL-STORY-PROMPT.md`로 `full_story.md`를 생성해 전체 구조를 한 번 더 고정한다.
5. `codex mcp list`로 필요한 MCP가 등록되어 있는지 확인한다.
6. writer runtime preflight를 한다.
   - `01-style-guide.md` → `03-characters.md` → `02-episode-structure.md` 순으로 읽고, 실제 Codex writer 기준으로 GO/REVISE를 점검한다.
   - `plot`의 고위험 화수에는 optional `risk:` 태그(`why`, `oag`, `pov-era`, `scene-logic`)를 붙인다.
7. `batch-supervisor.md` 기준으로 writer 세션을 띄운다.

## config.json 운영

lean도 상위 카탈로그 `/root/novel/config.json`을 운영 대상에 포함한다.

초기화 시:

- 새 소설 entry를 등록한다.
- 최소 필드는 `id`, `title`, `author`, `genre`, `description`, `cover`, `fullStory`, `status`, `totalEpisodes`, `parts`다.
- `parts` 배열 순서는 반드시 `batch-supervisor.md`의 `ARC_MAP` 순서와 맞춘다.
- 각 part는 최소 `{ "name": "표시명", "episodes": [] }` 구조를 가진다.

화별 집필 후:

- writer가 아니라 supervisor가 `/root/novel/config.json`을 갱신한다.
- 현재 화의 `EPISODE_META.title`을 읽어 해당 part의 `episodes` 배열에 upsert 한다.
- episode 객체는 `{ "number": N, "title": "...", "file": "no-title-XXX/chapters/{arc}/chapter-{NN}.md" }` 형식을 따른다.
- 중복 번호는 덮어쓰고, 배열은 화수 순으로 유지하며, `totalEpisodes`는 실제 등록된 episode 수와 맞춘다.

운영 원칙:

- `parts` 표시명은 사람이 읽는 제목이고, 매핑 기준은 `ARC_MAP` 순서다.
- `prologue` / `arc-01` / `interlude-01` / `epilogue` 같은 arc key와 `config.json.parts` 순서를 어긋나게 두지 않는다.
- `/root/novel` 자체가 git 관리 중이면 `config.json` 변경은 상위 워크스페이스에서 따로 커밋한다.

## Scope Decisions

여전히 일부는 하지 않는다.

- 외부 AI 리뷰 자동화 기본화
- 특정 도구 전용 command 체계 재현
- 초대형 보조 시스템 선구축

하지만 Codex 내부에서 확실히 하는 것은 많다.

- review floor 강제
- periodic check 강제
- arc-boundary audit 강제
- batch writing supervision
- batch audit supervision

이 템플릿은 Codex를 기준으로 바로 쓰는 운영 분기다.
