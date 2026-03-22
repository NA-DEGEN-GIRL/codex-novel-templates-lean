# Batch Writing Supervisor Prompt (Codex Lean)

Codex가 tmux 안의 다른 Codex 세션을 감시하면서 연속 에피소드 집필을 감독하기 위한 운영 문서.

Claude lean의 감독 수준을 Codex 방식으로 끌어오기 위해, 이 문서는 단순 "다음 화 써라"가 아니라 review floor 결정, 정기 점검, 아크 경계 감사, 완료 검증까지 강제한다.

## Execution Structure

- **Supervisor**: `/root/novel`에서 실행
- **Writer**: 각 소설 폴더에서 실행

writer는 해당 프로젝트의 `CODEX.md`를 읽고, supervisor는 이 문서와 프로젝트 `CODEX.md`를 함께 따른다.

## Configuration Variables

| Variable | Description | Example |
|---|---|---|
| `NOVEL_ID` | Novel folder name | `no-title-001-gpt` |
| `SESSION` | tmux session name | `codex-write-001-gpt` |
| `NOVEL_DIR` | Absolute path | `/root/novel/no-title-001-gpt` |
| `START_EP` | First episode | `1` |
| `END_EP` | Last episode | `70` |
| `CHUNK_SIZE` | Context reset interval, `-1` = no forced reset | `10` |
| `WRITER_CMD` | Writer launch command | `scripts/run-codex-writer` |
| `ARC_MAP` | Arc mapping | `{"prologue":[1,5],"arc-01":[6,55]}` |

## Core Rules

1. 외부 AI 리뷰를 기본 경로에 넣지 않는다.
2. `scripts/compile-brief`, `scripts/novel-calc`, `scripts/novel-hanja`를 우선 사용한다.
3. supervisor는 orchestrator다. 대규모 본문 재작성은 writer에게 맡긴다.
4. review floor 이하로 강등하지 않는다.
5. 아크 마지막 화 뒤에는 [ARC-BOUNDARY-CHECKLIST.md](/root/novel/codex-novel-templates-lean/ARC-BOUNDARY-CHECKLIST.md)를 강제한다.

## Review Floor Determination

감독자는 각 화 시작 전에 review floor를 먼저 결정한다.

```text
if N is first episode of a new arc   -> full
elif N is last episode of current arc -> standard + arc transition package
elif N % 5 == 0                      -> standard
else                                 -> continuity
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

## Writer Prompt Template

### Chunk Start Or New Arc

```text
{N}화를 집필해줘.

[컨텍스트]
- 먼저 `scripts/compile-brief {NOVEL_DIR} {N}`로 현재 맥락을 확인한다.
- `plot/{arc}.md`와 필요 시 `plot/master-outline.md`를 확인한다.
- 첫 화가 아니면 직전 화 마지막 2~3문단을 확인한다.

[집필]
- `CODEX.md`의 workflow를 따른다.
- `settings/01-style-guide.md`, `settings/02-episode-structure.md`를 따른다.
- planning flags를 먼저 정리한다.
- 파일명은 `chapters/{arc}/chapter-{NN}.md`

[검토]
- 이번 화의 review floor는 `{review_floor}`다.
- 최소한 continuity, Korean naturalness, narrative function을 점검한다.
- `standard` 이상이면 반복 패턴과 WHY/HOW도 본다.
- `full`이면 설정/복선/동기/행동 갭까지 재점검한다.
- 필요 시 `scripts/novel-calc`, `scripts/novel-hanja`를 사용한다.

[후처리]
- `summaries/running-context.md`
- `summaries/episode-log.md`
- `summaries/character-tracker.md`
- 관련 있을 때만 `promise-tracker`, `knowledge-map`, `relationship-log`, `decision-log`, `plot/foreshadowing.md`, `repetition-watchlist.md`
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
- `scripts/compile-brief {NOVEL_DIR} {N}`를 먼저 실행한다.
- review floor는 `{review_floor}`다.
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
4. 필요한 경우 조건부 summary도 반영

아크 마지막 화는 추가로 아래가 필요하다.

5. `review-log.md` 갱신
6. 다음 아크 런웨이 반영
7. patch-feasible/HOLD 구분 완료

## Session Management

### Writer Launch

```bash
tmux new-session -d -s ${SESSION} -c ${NOVEL_DIR} 'scripts/run-codex-writer'
```

### Recommended Commands

```bash
tmux capture-pane -t ${SESSION} -p -S -80
tmux send-keys -t ${SESSION} -l '프롬프트 내용'
tmux send-keys -t ${SESSION} Enter
```

## Recovery Rules

- writer가 질문을 던지고 멈췄으면, 가능한 범위에서 supervisor가 결정해 짧게 답한다.
- same-state 정체가 길면 "현재 단계만 마무리하고 다음 단계로 진행" 같은 회복 프롬프트를 넣는다.
- crash 시에는 파일 기준으로 마지막 완료 화를 다시 판정하고 그 다음 화부터 재개한다.

## Important Difference From Claude Version

Codex 버전은 다음을 전제하지 않는다.

- `.claude/commands/*`
- external reviewer MCP mandatory path
- Claude 전용 agent matrix

대신 다음을 강제한다.

- 로컬 스크립트 기반 맥락 로딩
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
