# Batch Audit Supervisor Prompt (Codex Lean)

Codex가 tmux 안의 다른 Codex 세션을 감시하면서, 기존 원고에 대한 전범위 감사 또는 구간 감사를 감독하기 위한 운영 문서.

이 문서는 "새 화 집필"이 아니라 "이미 존재하는 본문 점검"에 초점을 둔다.

## Purpose

- 기존 본문을 N화 단위 또는 전체 범위로 감사
- patch-feasible 수정은 즉시 반영
- 구조 수정이 필요한 항목은 HOLD로 남김
- 보고서와 summary 재정합까지 마무리

## Configuration Variables

| Variable | Description | Example |
|---|---|---|
| `NOVEL_ID` | Novel folder name | `no-title-001-gpt` |
| `SESSION` | tmux session name | `codex-audit-001-gpt` |
| `NOVEL_DIR` | Absolute path | `/root/novel/no-title-001-gpt` |
| `START_EP` | Start episode | `1` |
| `END_EP` | End episode | `55` |
| `BATCH_SIZE` | `-1` for full audit, else per-batch size | `10` |
| `AUDITOR_CMD` | Auditor launch command | `scripts/run-codex-auditor` |

## Audit Stack

감사자는 범위 내 본문을 읽고 아래 순서로 점검한다.

1. continuity / fact mismatch
2. opening carry-forward mismatch
3. WHY/HOW explanation gap
4. motivation-action gap / OAG suspicion
5. POV / era mismatch
6. scene logic
7. repetition
8. Korean naturalness

이 순서는 batch 단위 감사에도 유지한다.

## Supervisor Responsibilities

1. tmux 세션 생성 또는 재사용
2. 감사 범위와 배치 계획 결정
3. 감사 프롬프트 전송
4. 파일 기반 완료 검증
5. 다음 배치 또는 종료 처리

## Prompt Template

### Full Audit

```text
{START_EP}~{END_EP}화를 감사해줘.

[감사 범위]
- 기존 본문을 다시 쓰는 게 아니라 감사한다.
- patch-feasible 항목만 즉시 수정한다.
- 구조 수정이 필요한 항목은 HOLD로 남긴다.

[점검 순서]
1. continuity / fact mismatch
2. opening carry-forward mismatch
3. WHY/HOW explanation gap
4. motivation-action gap / OAG suspicion
5. POV / era mismatch
6. scene logic
7. repetition
8. Korean naturalness

[필수 산출물]
- `summaries/review-log.md`
- 필요 시 `summaries/repetition-watchlist.md`
- 필요한 summary 재정합
- `summaries/action-log.md` append

[원칙]
- 외부 AI 사용 금지
- unrelated dirty files 건드리지 말 것
- 마지막에 수정 화수와 HOLD만 간단히 보고
```

### Batch Audit

```text
{BATCH_START}~{BATCH_END}화를 감사해줘.
- 위 full audit 규칙을 그대로 따른다.
- 이번 배치에서 나온 carry-forward 문제는 다음 배치와 충돌하지 않게 `review-log.md`에 명시한다.
```

## Completion Check

배치 완료 판정은 아래를 모두 만족할 때만 한다.

1. tmux 세션이 프롬프트 대기 상태
2. `summaries/review-log.md` 갱신
3. 수정이 있었다면 대상 chapter 파일 또는 summary 파일의 timestamp 변화
4. `summaries/action-log.md` 기록 존재

## Batch Transition

`BATCH_SIZE > 0`일 때:

1. 현재 배치 결과 검증
2. `review-log.md` 마지막 범위 확인
3. 다음 배치 프롬프트 전송
4. 마지막 배치 후 전체 HOLD와 반복 감시 패턴이 남아 있는지 확인

## Recommended tmux Commands

```bash
tmux capture-pane -t ${SESSION} -p -S -80
tmux send-keys -t ${SESSION} -l '감사 프롬프트'
tmux send-keys -t ${SESSION} Enter
```

감사자 실행 예시:

```bash
tmux new-session -d -s ${SESSION} -c ${NOVEL_DIR} 'scripts/run-codex-auditor'
```

## Notes

- 이 문서는 Codex-only 감사 운영 문서다.
- Claude 전용 checker 명령을 호출하지 않는다.
- 대신 동일한 검사 축을 사람이 읽는 수준의 Codex 절차로 강제한다.
