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
└── skills/
```

Codex 런타임은 `CODEX.md`, `batch-supervisor*.md`, `skills/`를 기준으로 동작한다.
`settings/`는 hybrid, Claude lean과 공유하는 공통 집필 레이어이며, 이 문서와 `batch-supervisor.md`는 Codex 런타임 규칙만 정의한다.

---

## 3. Writing Workflow

### 3.1 Preparation

1. 먼저 `novel-editor` MCP의 `compile_brief(novel_dir="<novel_dir>", episode_number=<episode_number>)`를 호출한다. 브리프에 `직전 화 직결 앵커`가 있으면 현재 화 오프닝의 1차 기준으로 사용한다.
2. 직전 화 마지막 2~3문단을 확인하되, 가능하면 마지막 장면 전체 또는 마지막 8~12문단을 읽어 hook connection과 opening carry-forward facts를 확인한다.
3. 현재 아크의 `plot/arc-XX.md` 또는 `plot/prologue.md`를 확인한다.
4. 이번 화의 핵심 인물이 분명하면 `settings/03-characters.md`를 보고 대표 대사, 관계 상태, 운용 앵커를 확인한다.
5. 회상, 명시적 경과일수, 이동 시간, 부상 회복, 수련 기간, 약속 만기, 나이/연령대 단서, carry-forward promises가 나오면 `settings/05-continuity.md`를 직접 확인한다.
6. 필요 시 `plot/foreshadowing.md`, `summaries/character-tracker.md`, `summaries/promise-tracker.md`를 본다.
7. review-only 작업이면 필요한 범위만 읽고, 프로젝트 전체를 무의식적으로 훑지 않는다.
8. native MCP를 기본 경로로 사용한다.

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
  - `time_check_required`
  - `new_danger`
  - `new_setting_claim`
  - `calc_used`

### 3.3 Draft

1. `settings/02-episode-structure.md`를 따른다.
2. `settings/01-style-guide.md`를 따르고, 대화와 관계 장면은 `settings/03-characters.md`의 운용 앵커를 기준으로 변주한다. **규칙이 충돌하면 §0.8 우선순위를 따른다.**
3. 목표 분량은 {{TARGET_LENGTH}}를 기준으로 하되, 장면 밀도를 위해 필요한 길이를 확보한다.
4. 두 명 이상이 장면에 함께 있으면, 대화와 반응이 상황·관계·압력의 일부를 실제로 운반해야 한다. 지문이 이미 준 사실을 대사가 복창하는 식으로 때우지 않는다.
5. 같은 방, 식사 자리, 마차, 배, 숙영지, 은신처, 경계 장소에 있는 이름 있는 인물은 장면 논리에서 사라지면 안 된다. 침묵, 반응, 퇴장, 수면, 부재 중 하나로라도 자연스럽게 처리한다.
6. `novel-calc` MCP는 **검증용**이다. 수치를 서사의 엔진처럼 쓰지 않는다.
7. 계산 결과를 인물의 대사/독백/근접 시점 서술에 그대로 복붙하지 않는다. 사람처럼 어림하고, 감정 상태에 맞게 반올림하거나 감각적 표현으로 바꾼다.
8. 무협/역사/한자어 기반 작품이면 `novel-hanja` MCP를 사용한다. LLM 추정 한자 조립 금지.
9. 한자 병기는 첫 등장 또는 재등장 간격이 충분할 때만 쓴다. 이후에는 한국어 표기로 유지한다.
10. 시대에 맞는 단위/수사/어휘를 쓴다. 비현대 배경이면 아라비아 숫자를 본문에서 피한다.
11. 각주가 필요하면 `[^N]` 형식을 쓴다.
12. naming variant 검사가 필요하면 `novel-naming` MCP를 사용한다.
13. `settings/03-characters.md`의 대표 대사는 복붙용 문장이 아니라 운용 앵커다. 어휘 선택, 위계감, 판단 방식을 읽고 실제 장면에 맞게 변주한다.
14. 회상, 상대 시간 표현, 이동/회복/수련 기간, deadline이 있는 화는 초안 후 `settings/05-continuity.md`와 대조해 시간축 self-check를 수행한다. 애매하면 `novel-calc`의 날짜/기간 계산을 사용하거나 서술을 더 보수적으로 낮춘다.

### 3.4 Review Stack

Codex lean의 리뷰는 "한 번 보고 끝"이 아니라 층별 점검이다.

#### Review Floors

- `continuity`
  - 연속성
  - 시간축, 나이, 경과일수, 이동/회복/수련 기간 정합성
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
2. time / age / duration continuity
3. opening carry-forward gate — 현재 화 첫 장면이 `직전 화 직결 앵커`, 공개/비공개 정보, 부상/결정 결과를 어기지 않는가
4. Korean naturalness
5. narrative function
6. repeated-pattern risk
7. dialogue voice drift — 주요 인물 대사가 `03-characters.md` 앵커에서 이탈하지 않았는가? `dialogue-log.md`의 최근 톤 델타와 현재 화 일관성 확인. 역할 고착 판정은 `summaries/dialogue-log.md`를 직접 읽어 최근 5회 출연의 대화 기능을 확인한다 (brief에는 1건만 포함). 4/5회 동일 기능이면 역할 고착 경고.
8. (standard+) voice convergence — 화자 태그를 제거해도 각 캐릭터를 식별할 수 있는가? 두 인물의 대사를 교체해도 어색하지 않다면 분화 실패.
9. WHY/HOW or motivation-action gap when relevant

### 3.5 Arc Boundary Audit

아크 마지막 화가 끝나면 반드시 [ARC-BOUNDARY-CHECKLIST.md](/root/novel/codex-novel-templates-lean/ARC-BOUNDARY-CHECKLIST.md)를 수행한다.

핵심 원칙:

- patch-feasible 항목은 즉시 수정
- 구조 수정이 필요한 항목은 `HOLD`로 남김
- 본문 수정 후 summary/plot 정합성을 다시 맞춤
- 다음 아크 진입 전 런웨이를 `running-context.md`에 명시

### 3.6 Post-Processing

매 화 후 최소 아래를 갱신한다.

- `summaries/running-context.md` — `Immediate Carry-Forward` 또는 `직전 화 직결 상태`를 유지한다. 다음 화 오프닝에 반드시 이어질 사실만 3~7개 bullet로 기록한다.
- `summaries/episode-log.md`
- `summaries/character-tracker.md`

조건부:

- `summaries/promise-tracker.md`
- `summaries/knowledge-map.md` — 새 정보를 배운 경우뿐 아니라 보고/경고/허락/소문/비밀 공유가 실제로 성립했거나 불발된 경우도 포함한다. 다음 화 오프닝에 영향을 주면 skip하지 않는다.
- `summaries/relationship-log.md`
- `summaries/decision-log.md`
- `plot/foreshadowing.md`
- `summaries/repetition-watchlist.md`
- `summaries/dialogue-log.md` — 대화 기능 태그는 매화 등장 시 항상 기록 (role-only 행). 톤 델타/관계톤/지향은 앵커에서 이탈한 경우만 기록 (이탈 행). 원문 복붙 금지. 3화 이상 반복된 패턴은 `03-characters.md`로 승격 검토.

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
- P1~P13을 기준으로 수행하며, Core는 항상, Optional은 관련이 있을 때만 점검한다.

---

## 4. Codex-Only Execution Model

Codex lean은 아래를 기본 전제로 하지 않는다.

- `.claude/commands/*`
- external reviewer MCP mandatory path
- editor-specific agent files

대신 아래를 전제로 한다.

- 로컬 파일 읽기
- Codex native MCP (`novel-editor`, `novel-calc`, `novel-hanja`, `novel-naming`)
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

`settings/`는 세 템플릿이 공유하는 literary/continuity layer다. 이 문서보다 더 구체적인 규칙이 있으면 `settings/`가 우선하고, 이 문서는 Codex 실행 방식만 정의한다.

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
11. 같은 공간에 둔 이름 있는 인물을 장면에서 완전히 지워두는 처리 금지

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

Codex lean의 목표는 다른 도구 체계를 이름만 바꿔 옮기는 것이 아니다.

목표는 아래 네 가지다.

1. 한 화를 안정적으로 쓴다.
2. summary와 plot을 깨뜨리지 않는다.
3. 아크 경계 감사를 누락하지 않는다.
4. tmux batch supervision과 audit supervision까지 실제로 굴러가게 한다.

이 네 가지가 돌아가면, Codex lean은 더 이상 얕은 포팅본이 아니라 독립 운영 템플릿이다.
