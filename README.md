# Codex Novel Templates -- Lean Edition

Codex 중심으로 한국어 웹소설 프로젝트를 운영하기 위한 템플릿.

이 레포는 이제 단순한 "얇은 포팅본"이 아니라, `claude-novel-templates-lean`의 집필/정기 점검/아크 경계 감사 습관을 Codex 방식으로 재구성한 운영 베이스다.

## What This Is

- 한국어 웹소설용 프로젝트 스캐폴드
- Codex 기준 운영 문서 세트
- Codex-only self-review / audit / supervisor workflow
- `compile_brief`, `novel-calc`, `novel-hanja`를 로컬에서 호출하는 래퍼 포함
- Claude 프로젝트를 Codex 프로젝트로 옮기는 마이그레이션 프롬프트 포함

## What This Is Not

- Claude `.claude/commands`의 1:1 복제품
- 외부 AI 리뷰를 기본 전제로 하는 파이프라인
- 거대한 MCP 생태계를 먼저 가정하는 플랫폼

기본 철학은 유지한다. Codex에서 실제로 굴러가게 만들고, 그 위에 품질 게이트를 얹는다.

## Design Principles

1. `settings/`, `plot/`, `summaries/`, `chapters/` 구조는 유지한다.
2. 집필뿐 아니라 정기 점검과 아크 경계 감사까지 Codex 내부에서 닫힌 루프로 돌린다.
3. 외부 AI는 예외 경로다. 기본 품질 체계는 Codex self-review와 audit 문서로 해결한다.
4. Claude 전용 agent matrix는 복제하지 않고, Codex 역할과 체크리스트로 압축한다.
5. supervisor와 auditor가 파일 기반으로 완료를 검증하도록 설계한다.

## What's New In The Upgraded Lean

이전 Codex lean이 "다음 화를 쓸 수 있는 최소 상태"였다면, 현재 버전은 아래를 추가로 보장한다.

- `CODEX.md`에 상세한 운영 헌법, review floors, 금지 규칙, EPISODE_META 규약
- [ARC-BOUNDARY-CHECKLIST.md](/root/novel/codex-novel-templates-lean/ARC-BOUNDARY-CHECKLIST.md)로 아크 경계 감사 강제
- [batch-supervisor.md](/root/novel/codex-novel-templates-lean/batch-supervisor.md)의 강화된 review floor / completion check
- [batch-supervisor-audit.md](/root/novel/codex-novel-templates-lean/batch-supervisor-audit.md)로 기존 원고 감사 감독
- `settings/07-periodic.md`의 Codex 전용 정기 점검 스택

즉, Claude lean 대비 가장 약했던 "감사 절차 누락"을 메운 버전이다.

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
- `MIGRATION-CLAUDE-TO-CODEX.md`
  - Claude 프로젝트 마이그레이션 프롬프트
- `AGENT-MAP.md`
  - Claude 역할을 Codex 역할로 매핑
- `skills/`
  - Codex용 skill 정의
- `scripts/`
  - `compile-brief`, `novel-calc`, `novel-hanja`
  - `run-codex-writer`, `run-codex-supervisor`, `run-codex-auditor`
- `settings/`, `plot/`, `summaries/`, `chapters/`, `reference/`
  - 소설 자산 구조

## Workflow

기본 집필 흐름:

1. `scripts/compile-brief`로 맥락 로드
2. planning flags + WHY/HOW 질문 정리
3. 초안 작성
4. review floor에 맞는 self-review
5. summary / plot / action-log 갱신

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
2. patch-feasible 즉시 수정
3. HOLD 기록
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
- Claude 프로젝트의 Codex 마이그레이션

## Supported Local Tools

- `scripts/compile-brief`
- `scripts/novel-calc`
- `scripts/novel-hanja`
- `scripts/run-codex-writer`
- `scripts/run-codex-supervisor`
- `scripts/run-codex-auditor`

예시:

```bash
scripts/compile-brief /root/novel/no-title-001-gpt 7
scripts/novel-calc calculate expression='1250 * 1.35'
scripts/novel-hanja hanja_lookup text='天外歸還'
scripts/run-codex-writer
```

## Quick Start

새 프로젝트:

1. 이 레포를 복사한다.
2. `INIT-PROMPT.md`를 기준으로 `CODEX.md`와 `settings/`를 채운다.
3. `scripts/compile-brief`가 동작하는지 확인한다.
4. `batch-supervisor.md` 기준으로 writer 세션을 띄운다.

기존 Claude 프로젝트 마이그레이션:

1. 본문은 건드리지 않는다.
2. `MIGRATION-CLAUDE-TO-CODEX.md`로 운영 문서를 이식한다.
3. `CLAUDE.md`와 `.claude/`는 reference-only로 남긴다.
4. 아크 하나를 대상으로 Codex audit를 먼저 돌려 정합성을 확인한다.

## Scope Decisions

여전히 일부는 하지 않는다.

- 외부 AI 리뷰 자동화 기본화
- Claude command 체계 재현
- 초대형 보조 시스템 선구축

하지만 이제는 하지 않는 것보다, Codex 내부에서 확실히 하는 것이 더 많다.

- review floor 강제
- periodic check 강제
- arc-boundary audit 강제
- batch writing supervision
- batch audit supervision

이 정도면 Codex lean은 Claude lean의 경량 대체재가 아니라, Codex용 운영 분기라고 볼 수 있다.
