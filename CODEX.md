# Codex Writing Constitution

> Codex 기반 한국어 웹소설 운영용 최상위 규약.
> 이 문서는 `claude-novel-templates-lean/CLAUDE.md`의 Codex 버전 시작점이다.

## Language Contract

- 운영 지시문은 영어 또는 한국어 혼용 가능.
- 소설 본문, 대사, 요약, 리뷰 결과물은 기본적으로 한국어로 작성한다.
- 한국어 예시는 규범적 스타일 타깃으로 취급한다.

## Core Principle

Codex는 Claude처럼 프로젝트 내부 `.claude/commands`를 실행하는 엔진이 아니다. 따라서 이 템플릿은 다음 방식으로 작동한다.

1. 파일 구조와 규칙은 템플릿이 담당한다.
2. 집필 절차는 `CODEX.md`와 프롬프트 파일이 담당한다.
3. 역할 분리는 Codex의 서브에이전트 또는 순차 작업으로 대체한다.
4. MCP는 선택적 가속기이며, 없어도 폴백 워크플로가 돌아가야 한다.
5. 외부 AI 리뷰는 기본 절차에 넣지 않는다. 필요하면 사용자가 명시적으로 요청할 때만 별도 참고 자료로 쓴다.

## Standard Workflow

### 1. Context Load

우선순위:

1. `compile_brief.py` 또는 동등한 `compile_brief` 도구
2. `summaries/running-context.md`
3. 현재 아크의 `plot/arc-XX.md`
4. `plot/foreshadowing.md`
5. `summaries/character-tracker.md`
6. 직전 화 마지막 2~3문단

### 2. Planning

집필 전에 최소한 아래를 정리한다.

- 이번 화의 기능
- 장면 개요
- 감정 앵커
- 엔딩 훅 유형
- 최근 3~5화 반복 패턴 회피 여부
- WHY/HOW 질문 1~3개

### 3. Draft

- 목표 분량과 `settings/01-style-guide.md`를 따른다.
- `settings/02-episode-structure.md`를 따른다.
- 숫자 검증이 필요할 때만 계산 도구를 쓴다.
- 한자어 검증이 필요할 때만 한자 도구를 쓴다.

### 4. Review

최소 3가지 축으로 점검한다.

1. 연속성
2. 한국어 자연스러움
3. 서사 기능

Codex에서 가능하면 서브에이전트를 분리하고, 아니면 한 세션에서 순차적으로 검토한다.

기본 원칙:

- Codex가 스스로 초안 작성과 검토를 모두 수행한다.
- 외부 모델 의견을 전제한 검토 로그나 피드백 파일은 필수 아티팩트가 아니다.

### 5. Update

매 화 후 최소한 아래를 갱신한다.

- `summaries/running-context.md`
- `summaries/episode-log.md`
- `summaries/character-tracker.md`

조건부:

- `summaries/promise-tracker.md`
- `summaries/knowledge-map.md`
- `summaries/relationship-log.md`
- `summaries/decision-log.md`
- `plot/foreshadowing.md`

## Codex Role Map

Claude의 전용 agent 파일을 그대로 이식하는 대신, 아래 역할로 압축한다.

- `writer`
  - 에피소드 초안, 부분 재작성
- `continuity-reviewer`
  - 설정/연속성/사실관계/훅 연결
- `narrative-reviewer`
  - 구조, 감정, 훅, 반복 패턴
- `korean-reviewer`
  - 번역투, 어색한 표현, 문장 호응
- `plot-checker`
  - WHY/HOW, OAG, 동기 갭

## Migration Rule

기존 Claude 프로젝트를 옮길 때는 아래 원칙을 지킨다.

1. `chapters/` 본문은 함부로 손대지 않는다.
2. 세계관 의미와 캐릭터 설정을 바꾸지 않는다.
3. `.claude` 전용 구조는 Codex 운영 문서로 치환한다.
4. 먼저 얕은 마이그레이션을 하고, 자동화는 나중에 붙인다.

## Practical Advice

Codex 버전의 1차 목표는 "Claude 템플릿의 모든 기능을 1:1 복제"가 아니다.

1. 같은 폴더 구조를 쓴다.
2. 같은 검토 습관을 유지한다.
3. 같은 브리프 압축기를 재사용한다.
4. 필요한 자동화만 추가한다.

그게 실제로 운영 가능한 최소 단위다.
