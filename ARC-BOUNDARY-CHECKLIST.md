# Arc Boundary Checklist (Codex Lean)

> 아크 마지막 화 완료 직후 수행하는 Codex 전용 아크 경계 감사 절차.
> 목적은 "다음 아크로 넘기기 전에 결함을 국소 수정하고, 구조 결함은 HOLD로 분리"하는 것이다.

## 0. Scope Lock

- 방금 완료한 아크의 본문만 대상이다.
- unrelated dirty files는 건드리지 않는다.
- 외부 AI는 기본 경로에서 사용하지 않는다.

## 1. Re-read The Completed Arc

완료 아크 전체를 다시 읽으며 아래를 표시한다.

- WHY/HOW 설명 갭
- 동기/행동 갭
- OAG(알고도 안 하는 행동) 의심
- POV 지식 위반
- 시대/세계관 어휘 위반
- 장면 내부 물리 논리 문제
- 크로스 에피소드 반복 패턴
- 한국어 자연스러움 문제

## 2. Classify Findings

각 이슈를 아래 중 하나로 분류한다.

- `patch-feasible`
  - 1~2화의 국소 수정으로 해결 가능
- `HOLD`
  - 구조 수정 필요
  - 후속 화 다수에 영향
  - 플롯 재배선 필요

`HOLD`는 바로 지우지 말고 `summaries/review-log.md`에 남긴다.

## 3. Patch In This Order

수정은 아래 순서로 직렬 수행한다.

1. continuity / fact mismatch
2. WHY/HOW explanation gap
3. motivation-action gap / OAG
4. POV / era mismatch
5. scene logic
6. repetition
7. Korean naturalness

같은 화를 동시에 여러 축으로 수정하지 않는다. 앞 수정이 뒤 판단을 바꾸기 쉽다.

## 4. Reconcile State Files

본문 수정 후 아래를 다시 맞춘다.

- `summaries/running-context.md`
- `summaries/episode-log.md`
- `summaries/character-tracker.md`

조건부:

- `summaries/promise-tracker.md`
- `summaries/knowledge-map.md`
- `summaries/relationship-log.md`
- `plot/foreshadowing.md`
- `summaries/repetition-watchlist.md`

## 5. Carry-Forward Triage

아크 종료 시 unresolved thread를 아래로 나눈다.

- 다음 아크 초반에 바로 이어질 것
- 중장기 carry-forward
- 사실상 종료된 것
- 설명 보강 필요하지만 아직 회수 시점이 아닌 것

이 분류를 `running-context.md`와 `promise-tracker.md`에 반영한다.

## 6. Next Arc Readiness

다음 아크의 `plot/arc-XX.md`를 확인하고 최소 아래가 보이는지 점검한다.

- 다음 화의 출발점
- 주인공의 현재 목표
- 현재 위험
- carry-forward될 핵심 복선
- 최근 아크에서 생긴 신체/관계/정보 상태

부족하면 plot 문서를 최소 보강한다.

## 7. Logging

반드시 아래를 남긴다.

- `summaries/review-log.md`
  - 이번 아크 감사 결과
  - patch-feasible 처리 내역
  - HOLD 목록
- `summaries/action-log.md`
  - 아크 경계 감사 수행 로그 한 줄

## 8. Completion Standard

아래를 모두 만족해야 아크 경계 감사 완료로 본다.

1. patch-feasible 항목이 반영됨
2. HOLD가 기록됨
3. summary 파일 재정합 완료
4. 다음 아크 런웨이가 `running-context.md`에 명시됨
5. action-log와 review-log가 갱신됨
