# Batch Writing Supervisor Prompt (Codex Lean)

Codex가 tmux 안의 다른 Codex 세션을 감시하면서 연속 에피소드 집필을 감독하기 위한 운영 문서.

이 문서는 단순 "다음 화 써라"가 아니라 review floor 결정, 정기 점검, 아크 경계 감사, 완료 검증까지 강제한다.

## Execution Structure

- **Supervisor**: `/root/novel`에서 실행
- **Writer**: 각 소설 폴더에서 실행

writer는 해당 프로젝트의 `CODEX.md`를 읽고, supervisor는 이 문서와 프로젝트 `CODEX.md`를 함께 따른다.
`settings/`는 hybrid, Claude lean과 공유하는 공통 집필 레이어다. 이 문서는 Codex 감독 절차만 정의하며, 문체/캐릭터/연속성/정기 점검 규칙이 충돌하면 `settings/`를 우선한다.

## Configuration Variables

| Variable | Description | Example |
|---|---|---|
| `NOVEL_ID` | Novel folder name | `no-title-001-gpt` |
| `SESSION` | tmux session name | `codex-write-001-gpt` |
| `NOVEL_DIR` | Absolute path | `/root/novel/no-title-001-gpt` |
| `START_EP` | First episode | `1` |
| `END_EP` | Last episode | `70` |
| `CHUNK_SIZE` | Manual context-reset interval, `-1` = auto-compact only | `10` |
| `WRITER_CMD` | Writer launch command | `codex` |
| `ARC_MAP` | Arc mapping | `{"prologue":[1,5],"arc-01":[6,55]}` |

## Core Rules

1. `settings/`는 공통 literary layer이고, 이 문서는 Codex supervision layer다.
2. 외부 AI 리뷰를 기본 경로에 넣지 않는다.
3. Codex native MCP(`novel-editor`, `novel-calc`, `novel-hanja`, `novel-naming`)를 우선 사용한다.
4. supervisor는 orchestrator다. 대규모 본문 재작성은 writer에게 맡긴다.
5. review floor 이하로 강등하지 않는다.
6. 아크 마지막 화 뒤에는 [ARC-BOUNDARY-CHECKLIST.md](/root/novel/codex-novel-templates-lean/ARC-BOUNDARY-CHECKLIST.md)를 강제한다.

## Review Floor Determination

감독자는 각 화 시작 전에 review floor를 먼저 결정한다.

```text
if N is first episode of a new arc       -> full
elif N is last episode of current arc    -> standard + arc transition package
elif periodic_due (settings/07-periodic) -> standard
else                                     -> continuity
```

### Mode Meaning

- `continuity`
  - 연속성
  - 명백한 문장 오류
  - summary 정합성
- `standard`
  - continuity
  - 서사 기능
  - 반복 패턴
  - WHY/HOW 설명 부족 여부
- `full`
  - standard
  - 설정/복선/아크 정합성
  - 동기/행동 갭
  - POV / 시대 / 장면 논리 위험

### Periodic Gate

- 정기 점검의 정본은 `settings/07-periodic.md`다.
- 기본 5화 단위, 최대 8화 초과 금지, 아크 경계에서는 강제 실행한다.
- P1~P13을 기준으로 수행하며, Core는 항상, Optional은 관련 있을 때만 점검한다.
- plot 파일의 에피소드 항목에 optional `risk:` 필드를 둘 수 있다. 허용 값: `why`, `oag`, `pov-era`, `scene-logic`.
- `risk:` 태그가 붙은 화는 최소 `standard` 검토를 우선 검토한다. 특히 carry-forward, 설명 누락, 장면 논리 위험 화수에서 사용한다.
- 첫 문단/장면 전환이 과도하게 압축적이거나 한국어 결합이 어색하면 prose drift override로 `standard`까지 승격한다.

## Writer Prompt Template

### Chunk Start Or New Arc

```text
{N}화를 집필해줘.

[컨텍스트]
- 먼저 `novel-editor` MCP의 `compile_brief(novel_dir="{NOVEL_DIR}", episode_number={N})`로 현재 맥락을 확인한다.
- 브리프에 `직전 화 직결 앵커`가 있으면 현재 화 오프닝의 1차 기준으로 사용한다.
- `plot/{arc}.md`와 필요 시 `plot/master-outline.md`를 확인한다.
- 첫 화가 아니면 직전 화 마지막 2~3문단을 확인하되, 가능하면 마지막 장면 전체 또는 마지막 8~12문단을 읽는다.

[집필]
- `CODEX.md`의 workflow를 따른다.
- `settings/01-style-guide.md`, `settings/02-episode-structure.md`를 따른다.
- `settings/03-characters.md`에서 핵심 인물의 대표 대사와 관계 상태를 확인한다.
- 회상, 상대 시간 표현, 이동/회복/수련 기간, deadline, 나이/연령대 단서가 있으면 `settings/05-continuity.md`를 직접 확인한다.
- planning flags를 먼저 정리한다.
- 같은 공간에 있는 이름 있는 인물을 장면에서 지우지 말고, 다음 화 오프닝에서 직전 화에 없던 보고/허락/안심/정보 전달을 기정사실처럼 점프하지 말 것.
- 파일명은 `chapters/{arc}/chapter-{NN}.md`

[검토]
- 이번 화의 review floor는 `{review_floor}`다.
- 최소한 continuity, time/age/duration continuity, Korean naturalness, narrative function을 점검한다.
- `standard` 이상이면 반복 패턴과 WHY/HOW도 본다.
- `full`이면 설정/복선/동기/행동 갭까지 재점검한다.
- 필요 시 `novel-calc`, `novel-hanja`, `novel-naming` MCP를 사용한다.

[후처리]
- `summaries/running-context.md`
- `summaries/episode-log.md`
- `summaries/character-tracker.md`
- `running-context.md`에는 반드시 `Immediate Carry-Forward` 또는 `직전 화 직결 상태` 섹션을 유지한다.
- 관련 있을 때만 `promise-tracker`, `knowledge-map`, `relationship-log`, `decision-log`, `plot/foreshadowing.md`, `repetition-watchlist.md`
- 보고/경고/허락/소문/비밀 공유가 실제로 성립했거나 불발되면 `knowledge-map.md`를 갱신한다.
- `summaries/action-log.md`에 한 줄 append

[원칙]
- 질문하지 말고 자율 완료
- 본문과 summary의 사실 불일치를 남기지 말 것
- unrelated dirty files는 건드리지 말 것
```

### Continuation Within Same Chunk

```text
이어서 {N}화를 집필해줘.
- 위 규칙을 그대로 따른다.
- `novel-editor` MCP의 `compile_brief(novel_dir="{NOVEL_DIR}", episode_number={N})`를 먼저 호출한다.
- 회상, 상대 시간 표현, 이동/회복/수련 기간, deadline이 있으면 `settings/05-continuity.md`를 다시 확인한다.
- review floor는 `{review_floor}`다.
- 현재 화 오프닝이 `직전 화 직결 앵커`와 충돌하지 않는지 먼저 확인한다.
- 필수 summary와 action-log까지 마무리한 뒤에만 완료로 본다.
```

## Arc Transition Package

아크 마지막 화가 끝나면 supervisor는 아래를 순서대로 지시한다.

1. 완료 아크 전체 재독
2. WHY/HOW 설명 갭 탐지
3. 동기/행동 갭 및 OAG 의심 탐지
4. POV / 시대 / 장면 논리 점검
5. 크로스 에피소드 반복 패턴 점검
6. 한국어 자연스러움 교정
7. patch-feasible 수정 반영
8. HOLD 기록
9. summary 및 plot 재정합
10. 다음 아크 런웨이 정리

간단히 넘기지 말고 [ARC-BOUNDARY-CHECKLIST.md](/root/novel/codex-novel-templates-lean/ARC-BOUNDARY-CHECKLIST.md)를 기준으로 한 단계씩 확인한다.

## Patch-Feasible Repair Batch

`patch-feasible`은 "좋은 지적"이 아니라 **즉시 수정 배치**로 흘려야 하는 항목이다.

lean에서는 hybrid의 fix routing을 Codex 방식으로 단순화해 아래 순서로 처리한다.

1. patch-feasible 항목을 화수별로 묶는다.
2. 각 항목을 아래 중 하나로 분류한다.
   - `micro`: 1~3문장 사실/호응 보정
   - `local`: 문단 단위 보강/삭제/어휘 교정
   - `rewrite`: 장면 단위 재작성
3. 같은 화의 `micro/local/rewrite`를 하나의 repair batch로 묶어 writer에게 보낸다.
4. writer는 해당 화만 수정하고, summary와 review-log를 재정합한다.
5. supervisor는 재검토 후 다음 항목으로 넘어간다.

repair batch 지시 원칙:

- 범위를 벗어난 새 설정 추가 금지
- 기존 톤/리듬/엔딩 훅 보존
- 한 화를 여러 축으로 동시에 흔들지 말고, 한 번의 배치로 끝낼 수 있게 묶기
- 재수정이 길어지면 `patch-feasible`이 아니라 `HOLD` 재분류 검토

## HOLD Transfer Routing

`HOLD`는 "나중에 보자"가 아니라, 즉시 수정하지 못한 구조 이슈를 명시적 목적지로 보내는 이관 티켓이다.

여기서 말하는 "다음 사이클"은 모호한 미래가 아니라 아래 네 가지 체크포인트 중 하나다.

| Route | 언제 쓰는가 | 필수 조치 | 집필 게이트 |
|---|---|---|---|
| `retro-fix` | 이미 집필된 부분이 현재 canon과 직접 충돌하고, 미래 화에서 자연 보상해도 독자 혼란이 남는 경우 | 영향 화수 지정, 전용 repair batch 예약, 수정 전까지 관련 설정 동결 | 다음 1~2화 진행 가능. 다만 영향 범위 확장 금지 |
| `forward-fix` | 기존 본문은 "틀렸다"기보다 "설명이 부족하다/맥락이 약하다"에 가깝고, 미래 사건으로 보강/재해석이 가능한 경우 | 미래 삽입 화수와 보상 비트 지정, plot과 running-context에 반영 | 지정한 만기 화수 전까지만 진행 가능 |
| `plot-repair` | 미래 아크 설계 자체를 다시 짜야 하거나 플롯 배선/세계관 규칙 변경이 필요한 경우 | `plot/arc-XX.md` 또는 `plot/master-outline.md` 수정, 새 런웨이 승인 | 영향 받는 아크에 진입하기 전 반드시 완료 |
| `user-escalation` | 작품 핵심 premise, 엔딩, 주인공 축, 세계관 핵심 규칙을 바꾸거나 3개 이상 아크에 영향이 가는 경우 | 사용자 보고 후 결정 대기 | 결정 전 해당 구간 집필 중단 |

blocker 기본값:

- `retro-fix` → `blocker=yes`
- `forward-fix` → `blocker=no`
- `plot-repair` → `blocker=yes`
- `user-escalation` → `blocker=yes`

### HOLD Triage Rules

`patch-feasible`가 아니면 끝이 아니라, 아래 순서로 `hold_route`를 확정한다.

1. **현재 독자 이해가 깨지는가?**
   - 지금 읽는 독자가 "이건 설명 부족"이 아니라 "앞뒤가 안 맞는다"로 느낄 가능성이 크면 `retro-fix`
2. **과거 본문을 canon으로 유지할 수 있는가?**
   - 기존 사건/대사/결과를 유지한 채 미래 사건으로 동기 보강, 의미 재해석, 정보 후속 공개가 가능하면 `forward-fix`
3. **미래 플롯 자체가 바뀌어야 하는가?**
   - 보상 비트를 한두 개 넣는 수준이 아니라 이후 아크의 목적, 갈등선, 세계 규칙을 다시 짜야 하면 `plot-repair`
4. **작품의 큰 약속을 건드리는가?**
   - 독자 약속, 엔딩 공약, 주인공 정체성 축을 바꾸면 `user-escalation`

판단이 애매하면 기존 본문 보존 비용이 더 낮은 쪽을 우선한다.

- "이미 거짓이 됨"이면 `retro-fix`
- "아직 부족하지만 미래 보상 가능"이면 `forward-fix`
- 애매하면 `forward-fix` 우선, 단 만기와 scope를 짧게 잡는다

### Existing Fix vs Forward-Fix Heuristic

아래 조건이 하나라도 강하면 `기존 수정(retro-fix)` 쪽이다.

- 이미 집필된 화 사이에 직접 모순이 있다
- 잘못된 인과 때문에 현재 감정선이 성립하지 않는다
- 미래 화에서 설명을 붙여도 과거 장면이 거짓처럼 보인다
- 영향 범위가 작고, 수정 비용이 미래 설계 비용보다 낮다

아래 조건을 모두 만족하면 `forward-fix`를 우선 검토한다.

- 기존 본문을 canon으로 유지할 수 있다
- 문제 성격이 "오판/미설명/동기 부족/배경 부족"이지 "사실 오류"는 아니다
- 미래 5화 이내 또는 다음 아크 초반에 보상 비트를 넣을 자리가 있다
- 보상 후 독자가 "아, 그래서 그랬구나"로 읽히지 "사실 설정이 바뀌었다"로 읽히지 않는다

### Forward-Fix Scope

`forward-fix`는 반드시 `scope`를 붙인다.

- `scope: current-arc`
  - 현재 아크 안에서 해결
  - 아크 종료 전까지 미해결이면 마감 불가
- `scope: next-arc`
  - 다음 아크 초반 carry-forward 허용
  - 다음 아크 plot과 running-context에 런웨이 명시 필수

### Forward-Fix Recording Standard

`forward-fix`는 한 파일에만 남기면 잊힌다. 아래 3곳을 동시에 갱신한다.

1. `summaries/review-log.md`
   - 권위 원장. `HOLD-ID / defect / route / target / latest-safe-resolution / preserve / payoff-plan / status`
2. `summaries/running-context.md`
   - 작업용 경고. 다음 1~3화에서 반드시 기억해야 할 open `forward-fix`만 유지
3. `plot/arc-XX.md`
   - 실제 집필 계획. 어느 화에서 어떤 사건/대사/공개로 보상할지 비트 단위로 삽입

독자에게 이미 약속된 떡밥이나 회수 deadline이 걸린 항목이면 `summaries/promise-tracker.md`에도 남긴다.

예시 형식:

```md
- [HOLD-FWD-001] status=open
  - defect: 3화 주인공의 이탈 동기가 약함
  - route: forward-fix
  - scope: next-arc
  - blocker: no
  - preserve: 3화의 선택과 결과는 유지
  - target: arc-02 chapter-08
  - latest-safe-resolution: chapter-09 초안 전
  - payoff-plan: 8화에서 가족 관련 사건을 삽입해 동기를 보강하고 3화 선택을 재해석
```

### Open HOLD Risk Control

해결 전 집필이 계속되면 아래 위험이 커진다.

- 잘못된 가정이 summary와 이후 화에 누적돼 수정 비용이 급증
- 서로 다른 화에서 임시 봉합이 중복돼 canon이 더 꼬임
- 보상 타이밍을 놓쳐 뒤늦은 설명 덤프가 됨
- writer가 open HOLD를 모른 채 반대 방향으로 plot을 고정함

관리 규칙:

- open `forward-fix`마다 `latest-safe-resolution`을 반드시 둔다
- 만기 화수를 넘기면 자동으로 `plot-repair` 또는 `user-escalation`로 승격한다
- `blocker=yes`인 HOLD가 남아 있으면 영향 아크 집필을 시작하지 않는다
- 아크 시작 전, 5화 배수 정기 점검, 아크 경계에서 open HOLD 목록을 재검토한다

해소 시 동기화 규칙:

1. `review-log.md`에서 `status: resolved` + 해결 화수/방식 기록
2. `running-context.md`의 HOLD 경고 제거 또는 resolved 표기
3. `plot/arc-XX.md`의 삽입 비트에 `[RESOLVED: {N}화]` 태그 추가

아크 마감 게이트:

- `scope: current-arc` open HOLD → 아크 마감 불가
- `scope: next-arc` open HOLD → carry-forward 확인 후 마감 가능
- `blocker=yes` open HOLD → 해당 영향 범위 집필 시작 불가

## Supervision Loop

### State Assessment

| State | Pattern | Action |
|---|---|---|
| working | 출력 진행 중, 프롬프트 대기 아님 | 2분 후 재확인 |
| waiting | 프롬프트 대기 | 다음 지시 또는 완료 검증 |
| error | traceback, file missing, command failure | 원인 확인 후 복구 지시 |
| stalled | 장시간 같은 상태 | 짧은 회복 프롬프트 전송 |
| completed | 파일 생성 + summary 갱신 + action-log 기록 | 다음 화 또는 아크 경계 패키지 |

### Completion Check

한 화 완료 판정은 아래를 모두 만족해야 한다.

1. 대상 chapter 파일 존재
2. `summaries/action-log.md` 기록 존재
3. `running-context.md`, `episode-log.md`, `character-tracker.md` 갱신
4. `running-context.md`의 `Immediate Carry-Forward` 또는 동등 섹션이 현재 화 종료 상태를 반영
5. 필요한 경우 조건부 summary도 반영

아크 마지막 화는 추가로 아래가 필요하다.

6. `review-log.md` 갱신
7. 다음 아크 런웨이 반영
8. patch-feasible/HOLD 구분 완료
9. open HOLD의 `hold_route`와 만기 화수 지정 완료
10. `blocker=yes` HOLD 없음 또는 사용자 승인 확보

## Session Management

- 기본 권장은 `CHUNK_SIZE = -1`이다. Codex의 auto-compact를 우선 믿고, 반복/맥락 누수가 실제로 보일 때만 수동 reset을 검토한다.
- supervisor는 한 화의 chapter 작성 + summary 갱신 + action-log 기록이 모두 확인된 뒤에만 다음 화 프롬프트를 보낸다.

### Writer Launch

```bash
tmux new-session -d -s ${SESSION} -c ${NOVEL_DIR} '${WRITER_CMD}'
```

### Recommended Commands

```bash
tmux capture-pane -t ${SESSION} -p -S -80
bash ${NOVEL_DIR}/scripts/tmux-send-codex ${SESSION} '프롬프트 내용' 2 80
bash ${NOVEL_DIR}/scripts/tmux-wait-sentinel ${SESSION} 'WRITER_DONE chapter-05.md' 1800 2 200
```

- `tmux-send-codex`는 Codex의 Enter 전송 타이밍과 시작 신호(`Working`, `Explored`, `Edited`, 입력 프롬프트 소멸)를 함께 확인한다.
- `tmux-wait-sentinel`은 기존 pane에 남아 있던 sentinel과 새로 출력된 sentinel을 구분해 대기한다.

## Recovery Rules

- writer가 질문을 던지고 멈췄으면, 가능한 범위에서 supervisor가 결정해 짧게 답한다.
- same-state 정체가 길면 "현재 단계만 마무리하고 다음 단계로 진행" 같은 회복 프롬프트를 넣는다.
- crash 시에는 파일 기준으로 마지막 완료 화를 다시 판정하고 그 다음 화부터 재개한다.

## Runtime Assumption

Codex 버전은 다음을 전제하지 않는다.

- `.claude/commands/*`
- external reviewer MCP mandatory path
- editor 전용 agent matrix

대신 다음을 강제한다.

- native MCP 기반 맥락 로딩
- Codex self-review stack
- 파일 단위 완료 검증
- 아크 경계 감사 강제

## Practical Standard

Codex lean supervisor의 품질 기준은 단순하다.

1. 한 화를 쓰게 한다.
2. summary를 맞춘다.
3. 정기 점검을 누락하지 않는다.
4. 아크 경계에서 감사와 런웨이 정리를 빠뜨리지 않는다.

이 네 가지가 지켜지지 않으면 완료로 치지 않는다.
