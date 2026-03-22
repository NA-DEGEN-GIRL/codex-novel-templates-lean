# {{NOVEL_TITLE}} - Codex Writing Constitution

> This is the top-level ruleset for the novel "{{NOVEL_TITLE}}".
> All writing, editing, audit, and batch-supervision operations follow this document.

## Language Contract

- 운영 문서는 영어 또는 한국어 혼용 가능.
- 소설 본문, 대사, 요약, 리뷰 로그, 수정 제안은 모두 한국어로 작성한다.
- 한국어 예시는 규범적 스타일 타깃이다.
- 장르/시대 어휘, 존댓말/반말, 호칭 위계는 한국어 표면 실현에서 추상 규칙보다 우선한다.

---

## 1. Project Overview

- **Title**: {{NOVEL_TITLE}}
- **Subtitle**: {{SUBTITLE}} (없으면 삭제)
- **Genre**: {{GENRE}}
- **Tone & Mood**: {{TONE}}
- **Keywords**: {{KEYWORDS}}
- **Target Audience**: {{TARGET_AUDIENCE}}
- **One-line Summary**: {{ONE_LINE_SUMMARY}}
- **Codex-only default**: true
- **External AI review**: false  <!-- 필요할 때만 사용자가 명시적으로 활성화 -->
- **Illustration**: false

### 1.1 Core Promises

1. {{PROMISE_1}}
2. {{PROMISE_2}}
3. {{PROMISE_3}}

### 1.2 Thematic Statement

- **주 주제**: {{MAIN_THEME}}
- **부 주제**: {{SUB_THEMES}}

> 최근 3화 이상이 주제와 완전히 무관하게 흘러가면, 다음 집필 전 WHY/HOW와 아크 목적을 재점검한다.

---

## 2. Folder Structure

```
{{NOVEL_ID}}/
├── CODEX.md                ← This file
├── batch-supervisor.md     ← tmux writing supervision rules
├── batch-supervisor-audit.md
├── ARC-BOUNDARY-CHECKLIST.md
├── settings/
├── chapters/
├── plot/
├── summaries/
├── reference/
├── scripts/
└── skills/
```

기존 Claude 프로젝트에서 옮겨온 경우:

- `CLAUDE.md`와 `.claude/`는 reference-only로 남겨도 된다.
- Codex 런타임은 `CODEX.md`, `scripts/`, `batch-supervisor*.md`, `skills/`를 기준으로 동작한다.

---

## 3. Writing Workflow

### 3.1 Preparation

1. 먼저 `novel-editor` MCP의 `compile_brief(novel_dir="<novel_dir>", episode_number=<episode_number>)`를 호출한다.
2. 직전 화 마지막 2~3문단을 확인한다.
3. 현재 아크의 `plot/arc-XX.md` 또는 `plot/prologue.md`를 확인한다.
4. 필요 시 `plot/foreshadowing.md`, `summaries/character-tracker.md`, `summaries/promise-tracker.md`를 본다.
5. review-only 작업이면 필요한 범위만 읽고, 프로젝트 전체를 무의식적으로 훑지 않는다.
6. MCP가 일시적으로 불가할 때만 `scripts/compile-brief`를 fallback으로 쓴다.

### 3.2 Planning Gate

집필 전에 최소 아래를 정리한다.

- 이번 화의 기능
- 주요 장면 3~6개
- 감정 앵커
- 이번 화의 WHY/HOW 질문
- 최근 3~5화 반복 패턴 회피 여부
- 엔딩 훅 유형
- planning flags
  - `flashback_present`
  - `new_danger`
  - `new_setting_claim`
  - `calc_used`

### 3.3 Draft

1. `settings/02-episode-structure.md`를 따른다.
2. `settings/01-style-guide.md`를 따른다.
3. 목표 분량은 {{TARGET_LENGTH}}를 기준으로 하되, 장면 밀도를 위해 필요한 길이를 확보한다.
4. `novel-calc` MCP는 **검증용**이다. 수치를 서사의 엔진처럼 쓰지 않는다.
5. 무협/역사/한자어 기반 작품이면 `novel-hanja` MCP를 사용한다. LLM 추정 한자 조립 금지.
6. 한자 병기는 첫 등장 또는 재등장 간격이 충분할 때만 쓴다. 이후에는 한국어 표기로 유지한다.
7. 시대에 맞는 단위/수사/어휘를 쓴다. 비현대 배경이면 아라비아 숫자를 본문에서 피한다.
8. 각주가 필요하면 `[^N]` 형식을 쓴다.
9. naming variant 검사가 필요하면 `novel-naming` MCP를 사용한다.

### 3.4 Review Stack

Codex lean의 리뷰는 "한 번 보고 끝"이 아니라 층별 점검이다.

#### Review Floors

- `continuity`
  - 연속성
  - summary 정합성
  - 명백한 문장/호응 오류
- `standard`
  - continuity
  - 서사 기능
  - 반복 패턴
  - 최근 장면 전환 자연스러움
- `full`
  - standard
  - 설정/복선/아크 정합성
  - WHY/HOW 설명 충분성
  - 동기/행동 갭 재점검

#### Review Roles

- `continuity-reviewer`
- `narrative-reviewer`
- `korean-reviewer`
- `plot-checker`

Codex가 서브에이전트를 쓸 수 있으면 역할을 분리하고, 아니면 한 세션에서 순차적으로 수행한다.

#### Mandatory Review Order

1. continuity
2. Korean naturalness
3. narrative function
4. repeated-pattern risk
5. WHY/HOW or motivation-action gap when relevant

### 3.5 Arc Boundary Audit

아크 마지막 화가 끝나면 반드시 [ARC-BOUNDARY-CHECKLIST.md](/root/novel/codex-novel-templates-lean/ARC-BOUNDARY-CHECKLIST.md)를 수행한다.

핵심 원칙:

- patch-feasible 항목은 즉시 수정
- 구조 수정이 필요한 항목은 `HOLD`로 남김
- 본문 수정 후 summary/plot 정합성을 다시 맞춤
- 다음 아크 진입 전 런웨이를 `running-context.md`에 명시

### 3.6 Post-Processing

매 화 후 최소 아래를 갱신한다.

- `summaries/running-context.md`
- `summaries/episode-log.md`
- `summaries/character-tracker.md`

조건부:

- `summaries/promise-tracker.md`
- `summaries/knowledge-map.md`
- `summaries/relationship-log.md`
- `summaries/decision-log.md`
- `plot/foreshadowing.md`
- `summaries/repetition-watchlist.md`

추가 규칙:

1. `EPISODE_META`를 각 화 끝에 삽입한다.
2. 주요 작업 완료 시 `summaries/action-log.md`에 한 줄 append한다.
3. 중요한 리뷰 결과는 `summaries/review-log.md`에 남긴다.
4. 어휘 치환 규칙이 채택되면 `summaries/style-lexicon.md`에 기록한다.
5. 본문+summary가 정합해진 뒤에만 commit한다.

### 3.7 Periodic Checks

정기 점검은 `settings/07-periodic.md`를 따른다.

기본값:

- 5화 단위
- 최대 8화 초과 금지
- 아크 경계에서는 회수와 무관하게 강제 실행

---

## 4. Codex-Only Execution Model

Codex lean은 Claude lean과 달리 아래를 기본 전제로 하지 않는다.

- `.claude/commands/*`
- external reviewer MCP mandatory path
- Claude-specific agent files

대신 아래를 전제로 한다.

- 로컬 파일 읽기
- Codex native MCP (`novel-editor`, `novel-calc`, `novel-hanja`, `novel-naming`)
- `scripts/compile-brief`, `scripts/novel-calc`, `scripts/novel-hanja` fallback
- tmux writer/supervisor/auditor 세션
- Codex self-review + Codex audit logs

외부 AI 참고는 예외 경로다. 기본 품질 체계는 Codex 내부에서 닫혀 있어야 한다.

---

## 5. File Reference Priority

1. `CODEX.md`
2. `settings/`
3. 최신 본문
4. `plot/`
5. `summaries/`
6. `CLAUDE.md` 및 `.claude/` reference-only assets

`settings/`가 이 문서의 일반 원칙보다 더 구체적이면 `settings/`가 우선한다.

---

## 6. Prohibitions

1. 설정 충돌 금지
2. 갑작스러운 성격 변조 금지
3. 대가 없는 승리 금지
4. 설명 없이 갑자기 해결되는 장면 금지
5. 메타 발화 금지
6. 고유명사 임의 개명 금지
7. 본문 속 `몇 화에서`, `프롤로그에서`, `1부에서` 식 메타 참조 금지
8. POV 지식 범위를 넘는 설명 금지
9. 장면 물리 논리 무시 금지
10. 최근 2~3화와 동일한 엔딩 훅/감정 처리 반복 금지

### 6.1 Intentional Mysteries

> WHY/HOW 점검 시 아래는 실수가 아니라 의도적 미스터리로 취급한다.

| 비밀 | 공개 예정 시점 | 왜 숨기는가 |
|---|---|---|
| {{MYSTERY_1}} | {{아크/화수}} | {{서사적 이유}} |

### 6.2 AI Execution Guardrails

| # | 가드레일 | 위반 예시 | 올바른 접근 |
|---|---|---|---|
| G1 | {{GUARDRAIL_1}} | {{위반 예시}} | {{올바른 접근}} |
| G2 | {{GUARDRAIL_2}} | {{위반 예시}} | {{올바른 접근}} |
| G3 | {{GUARDRAIL_3}} | {{위반 예시}} | {{올바른 접근}} |

---

## 7. Episode Metadata

각 화 말미에 아래 형식을 유지한다.

````markdown
---

### EPISODE_META
```yaml
episode: {{NUMBER}}
title: "{{TITLE}}"
summary: "{{SUMMARY}}"
date: "{{DATE}}"
pov: "{{POV_CHARACTER}}"
location: "{{LOCATION}}"
timeline: "{{TIMELINE_POSITION}}"
characters_appeared:
  - {{CHARACTER_1}}
new_elements:
  - "{{NEW_ELEMENT}}"
unresolved:
  - "{{UNRESOLVED_THREAD}}"
next_episode_hook: "{{HOOK}}"
thematic_function: "{{이번 화의 주제적 역할}}"
review_mode: "{{continuity|standard|full}}"
review_floor: "{{continuity|standard|full}}"
external_review: "none"
intentional_deviations: []
planning_flags:
  flashback_present: false
  new_danger: false
  new_setting_claim: false
  calc_used: false
```
````

---

## 8. Operating Standard

Codex lean의 목표는 "Claude 기능을 이름만 베끼는 것"이 아니다.

목표는 아래 네 가지다.

1. 한 화를 안정적으로 쓴다.
2. summary와 plot을 깨뜨리지 않는다.
3. 아크 경계 감사를 누락하지 않는다.
4. tmux batch supervision과 audit supervision까지 실제로 굴러가게 한다.

이 네 가지가 돌아가면, Codex lean은 더 이상 얕은 포팅본이 아니라 독립 운영 템플릿이다.
