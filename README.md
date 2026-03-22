# Codex Novel Templates -- Lean Edition

Codex 중심으로 한국어 웹소설 프로젝트를 운영하기 위한 경량 템플릿.

이 레포는 `claude-novel-templates-lean`의 소설 구조와 집필 습관을 유지하면서, Claude 전용 런타임 의존성을 제거하고 Codex에서 바로 쓸 수 있는 형태로 얇게 재구성한 시작점이다.

## What This Is

- 한국어 웹소설용 프로젝트 스캐폴드
- Codex 기준 운영 문서 세트
- `compile_brief`, `novel-calc`, `novel-hanja`를 로컬에서 호출할 수 있는 래퍼 포함
- Claude 프로젝트를 Codex 프로젝트로 옮기기 위한 마이그레이션 프롬프트 포함

## What This Is Not

- Claude `.claude/commands` 체계의 1:1 복제품
- 외부 AI 리뷰를 기본 전제로 하는 파이프라인
- 완성형 자동 집필 플랫폼

기본 원칙은 단순하다. 먼저 Codex에서 실제로 굴러가는 최소 집필 템플릿을 만들고, 반복 비용이 큰 부분만 나중에 자동화한다.

## Design Principles

1. `settings/`, `plot/`, `summaries/`, `chapters/` 구조는 최대한 유지한다.
2. 외부 AI 참고는 기본 파이프라인에서 제외한다. Codex 단독 운영이 기본값이다.
3. Claude 전용 에이전트 파일 대신 Codex용 운영 문서와 역할 맵으로 치환한다.
4. MCP 직접 연결이 없어도 로컬 래퍼로 핵심 기능을 쓸 수 있어야 한다.
5. 기능 확장보다 먼저 "다음 화를 쓸 수 있는 상태"를 확보한다.

## Repository Layout

- `CODEX.md`
  - Codex용 최상위 운영 규약
- `INIT-PROMPT.md`
  - 새 프로젝트 생성용 시작 프롬프트
- `MIGRATION-CLAUDE-TO-CODEX.md`
  - 기존 Claude 프로젝트를 Codex 방식으로 옮기는 프롬프트
- `AGENT-MAP.md`
  - Claude 역할을 Codex 역할로 압축한 매핑표
- `settings/`, `plot/`, `summaries/`, `chapters/`, `reference/`
  - Lean 템플릿의 소설 구조 자산
- `compile_brief.py`
  - 집필용 압축 브리프 생성기
- `scripts/`
  - `compile-brief`, `novel-calc`, `novel-hanja` 로컬 래퍼

## Current Workflow

Codex lean의 기본 흐름은 아래다.

1. `compile_brief` 또는 폴백 파일 읽기로 맥락 로드
2. 이번 화의 기능, 장면 개요, WHY/HOW 질문 정리
3. 본문 작성
4. 연속성, 한국어 자연스러움, 서사 기능 점검
5. `summaries/`와 `plot/foreshadowing.md` 갱신

필요하면 Codex 서브에이전트를 아래 역할로 나눌 수 있다.

- `writer`
- `continuity-reviewer`
- `narrative-reviewer`
- `korean-reviewer`
- `plot-checker`

자세한 원칙은 [CODEX.md](/root/novel/codex-novel-templates-lean/CODEX.md)에 있다.

## Supported Local Tools

현재 우선 지원하는 도구는 3개다.

- `scripts/compile-brief`
- `scripts/novel-calc`
- `scripts/novel-hanja`

이 스크립트들은 MCP 세션 연결 없이 로컬 import 방식으로 동작한다. 사용 예시는 [scripts/README.md](/root/novel/codex-novel-templates-lean/scripts/README.md)에 정리했다.

예시:

```bash
scripts/compile-brief /root/novel/no-title-001-gpt 7
scripts/novel-calc calculate expression='1250 * 1.35'
scripts/novel-hanja hanja_lookup text='天外歸還'
```

## Quick Start

새 프로젝트를 만들 때:

1. 이 레포를 복사한다.
2. Codex에서 [INIT-PROMPT.md](/root/novel/codex-novel-templates-lean/INIT-PROMPT.md)의 프롬프트를 사용한다.
3. 생성된 프로젝트의 `CODEX.md`, `settings/`, `plot/`을 채운다.
4. 첫 집필 전 `scripts/compile-brief`로 맥락 로딩이 되는지 확인한다.

기존 Claude 프로젝트를 옮길 때:

1. 프로젝트 본문은 건드리지 않는다.
2. [MIGRATION-CLAUDE-TO-CODEX.md](/root/novel/codex-novel-templates-lean/MIGRATION-CLAUDE-TO-CODEX.md)를 사용해 운영 문서를 이식한다.
3. Claude 전용 구조를 reference-only로 남기고, Codex가 독립적으로 작업 가능한 상태를 만든다.

## Scope Decisions

현재 이 레포는 의도적으로 몇 가지를 하지 않는다.

- 외부 AI 리뷰 자동화
- Claude command 체계 재현
- 거대한 스킬/MCP 생태계 선구축

이건 빠뜨린 게 아니라 설계 선택이다. Codex에서 먼저 검증해야 할 건 "한 화를 안정적으로 쓰고 갱신할 수 있는가"이지, "모든 보조 시스템이 동시에 붙어 있는가"가 아니다.

## Recommended Next Steps

1. 이 템플릿으로 빈 실험 프로젝트 하나 생성
2. 기존 작품 하나를 얕게 마이그레이션
3. 실제 집필 또는 부분 재작성 테스트
4. 그 다음에 반복 작업만 자동화

이 순서를 지키는 편이 실제 운영 비용이 가장 낮다.
