# Batch Writing Supervisor Prompt (Codex Lean)

Codex가 tmux 안의 다른 Codex 세션을 감시하면서 연속 에피소드 집필을 감독하기 위한 운영 프롬프트.

이 문서는 Claude용 `batch-supervisor.md`를 그대로 복제하지 않는다. Codex lean의 원칙에 맞춰 다음에 집중한다.

- 외부 AI 비의존
- 로컬 파일/스크립트 중심
- tmux 세션 감시
- 아크 전환/정기 점검의 누락 방지

## Purpose

감독자(supervisor) Codex는 `/root/novel/`에서 실행되고, 작성자(writer) Codex는 개별 소설 폴더에서 실행된다.

- supervisor
  - 배치 진행 관리
  - tmux 세션 상태 확인
  - 다음 화 프롬프트 전송
  - 아크 전환 패키지 누락 방지
- writer
  - 실제 집필
  - 요약 갱신
  - 자체 리뷰 수행

## Configuration Variables

아래 변수는 실제 프로젝트에 맞게 바꿔 넣는다.

| Variable | Description | Example |
|---|---|---|
| `NOVEL_ID` | Novel folder name | `no-title-001-gpt` |
| `SESSION` | tmux session name | `codex-write-001` |
| `NOVEL_DIR` | Absolute path | `/root/novel/no-title-001-gpt` |
| `START_EP` | First episode | `1` |
| `END_EP` | Last episode | `70` |
| `CHUNK_SIZE` | Optional context reset interval. `-1` means never force reset | `10` |
| `WRITER_CMD` | Writer launch command | `codex` |
| `ARC_MAP` | Arc mapping | `{"arc-01":[1,10],"arc-02":[11,20]}` |

## Core Rules

1. 외부 AI 리뷰를 요구하지 않는다.
2. `compile_brief`, `novel-calc`, `novel-hanja`는 로컬 스크립트로만 사용한다.
3. 감독자는 본문을 직접 쓰지 않는다. writer에게 지시하고 결과를 검증한다.
4. 아크 전환 시 plot-check와 summary 정리를 반드시 수행한다.
5. 설정/플롯 수정이 본문에 영향을 주면, 필요한 최소 범위만 부분 재작성한다.

## Writer Prompt Template

감독자는 각 화 시작 시 아래 형식으로 writer에게 지시한다.

```text
{N}화를 집필해줘.

[컨텍스트]
- 먼저 `scripts/compile-brief {NOVEL_DIR} {N}`로 맥락을 확인한다.
- 현재 아크의 `plot/{arc}.md`를 확인한다.
- 직전 화 마지막 2~3문단을 확인한다.

[집필]
- `CODEX.md`의 표준 워크플로를 따른다.
- `settings/01-style-guide.md`, `settings/02-episode-structure.md`를 따른다.
- 파일명은 `chapters/{arc}/chapter-{NN}.md`

[검토]
- 연속성
- 한국어 자연스러움
- 서사 기능
- 필요하면 `scripts/novel-calc`와 `scripts/novel-hanja`를 사용한다.

[후처리]
- `summaries/running-context.md`
- `summaries/episode-log.md`
- `summaries/character-tracker.md`
- 필요 시 다른 summary/plot 파일
- `summaries/action-log.md`에 한 줄 append

[원칙]
- 질문하지 말고 자율 완료
- 본문과 summary 사이의 사실 불일치를 남기지 말 것
```

## Review Floor

감독자는 각 화의 최소 점검 강도를 결정한다.

```text
if first episode of arc -> full
elif last episode of arc -> standard + arc transition package
elif N % 5 == 0 -> standard
else -> continuity
```

### Mode Meaning

- `continuity`
  - 연속성, 명백한 문장 오류, summary 정합성
- `standard`
  - continuity + 서사 기능 + 반복 패턴 점검
- `full`
  - standard + 설정/아크/복선 정합성 재확인

## Arc Transition Package

아크 마지막 화가 끝나면 감독자는 아래를 순서대로 지시한다.

1. 완료 아크 재검토
   - WHY/HOW 설명 갭
   - 동기/행동 갭
   - 반복 패턴
2. 필요한 최소 수정
   - patch-feasible만 우선 수정
   - 구조 수정이 필요하면 HOLD로 남기고 다음 플롯 조정 사이클로 넘김
3. 새 아크 플롯 점검
   - `plot/{next_arc}.md` 존재 확인
   - 없으면 생성
   - 새 아크의 목표, 갈등, 다음 2~3화 런웨이 확인
4. 아크 요약 정리
   - carry-forward thread
   - 종료된 약속/복선
   - 캐릭터 상태 기준선 갱신

## Supervision Loop

감독자는 주기적으로 tmux 화면을 확인하고 상태를 판정한다.

### State Types

| State | Pattern | Action |
|---|---|---|
| working | 출력 진행 중, 프롬프트 대기 아님 | 2분 후 재확인 |
| waiting | 프롬프트 대기 | 다음 지시 또는 완료 검증 |
| error | traceback, file missing, command failure | 원인 확인 후 복구 지시 |
| stalled | 같은 상태가 오래 지속 | 짧은 확인 프롬프트 전송 |
| completed | 파일 생성 + summary 갱신 + action-log 기록 | 다음 화 진행 |

### Completion Check

완료 판정은 최소 아래를 확인한다.

1. 해당 chapter 파일 존재
2. `summaries/action-log.md`에 작업 흔적 존재
3. 필수 summary 3종이 갱신됨

## Recommended Commands

감독자가 자주 쓰는 명령 예시:

```bash
tmux capture-pane -t ${SESSION} -p -S -60
tmux send-keys -t ${SESSION} -l '프롬프트 내용'
tmux send-keys -t ${SESSION} Enter
```

맥락 확인 예시:

```bash
/root/novel/codex-novel-templates-lean/scripts/compile-brief ${NOVEL_DIR} ${N}
```

## Important Difference From Claude Version

Codex 버전의 supervisor는 다음을 하지 않는다.

- `.claude/commands/*` 호출 전제
- 외부 AI 리뷰 자동 호출
- Claude 전용 MCP 권한 흐름 전제

대신 아래를 한다.

- 로컬 스크립트 실행
- 파일 수정 결과 검증
- 필요한 경우 Codex 서브에이전트 역할 분리

## Practical Use

이 문서는 "완전 자동 에이전트"라기보다 "감독용 표준 운영 절차"에 가깝다. 실제로는 supervisor Codex가 이 문서를 기준으로 writer 세션을 감시하면서, 화 단위 진행과 아크 전환 누락을 막는 데 사용한다.
