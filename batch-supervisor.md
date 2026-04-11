# Batch Writing Supervisor Prompt (Codex Lean)

Codex가 tmux 안의 다른 Codex 세션을 감시하면서 연속 에피소드 집필을 감독하기 위한 운영 문서.

이 문서는 단순 "다음 화 써라"가 아니라 review floor 결정, 정기 점검, 아크 경계 감사, 완료 검증까지 강제한다.

## Execution Structure

- **Supervisor**: `/root/novel`에서 실행. writer/review tmux 세션 orchestration, sentinel 대기, gate 판정, `/root/novel/config.json` 갱신만 맡는다.
- **Writer**: 각 소설 폴더의 tmux 세션에서 실행. chapter draft와 rewrite batch만 맡는다.
- **Review**: 각 소설 폴더의 별도 tmux 세션에서 실행. review floor 기반 감사, summary/review-log/action-log 정합성, arc-boundary package를 맡는다.

writer와 review는 각각 해당 프로젝트의 `CODEX.md`를 읽고, supervisor는 이 문서와 프로젝트 `CODEX.md`를 함께 따른다.
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
| `REVIEW_CMD` | Review launch command | `scripts/run-codex-review` |
| `ARC_MAP` | Arc mapping | `{"prologue":[1,5],"arc-01":[6,55]}` |
| `RUN_NONCE` | Per-prompt unique sentinel token minted by supervisor | `20260407-ep05-a1c9` |

review 세션 이름은 기본적으로 `${SESSION}-review`를 사용한다.

## Supervisor Start Prompt

Supervisor 세션을 띄운 직후에는 아래 형태로 시작하는 편이 안전하다.

```text
/root/novel/no-title-XXX 프로젝트를 /root/novel/no-title-XXX/batch-supervisor.md 기준으로 운영해줘.
writer 세션은 codex-write-XXX, review 세션은 codex-write-XXX-review이고, 이번 범위는 {START_EP}~{END_EP}화다.
supervisor가 writer/review 분리를 유지하면서 gate, summary 정합성 확인, /root/novel/config.json 업데이트까지 마무리해라.

중요:
- writer 세션에 `Working`, `Reading`, `Explored`, `Edited`, `Ran` 같은 진행 표시가 보이면 정상 진행으로 간주하고 추가 지시를 넣지 마라.
- review 세션이 후처리를 맡는다. writer에게 summary/review-log/action-log를 닫게 하지 마라.
- 매 화 또는 repair batch를 보낼 때마다 고유한 `RUN_NONCE`를 새로 정하고, writer에는 `WRITER_DONE ... :: run={RUN_NONCE}`, review에는 `REVIEW_DONE chapter-{NN} :: run={RUN_NONCE}` exact sentinel을 그 실행에만 사용해라.
- exact sentinel 또는 명시적 timeout 전에는 회복 프롬프트를 보내지 마라.
- 장문 프롬프트는 pane에 직접 paste하지 말고 `tmp/run-prompts/*.txt`에 저장한 뒤, tmux에는 `그 파일을 읽고 그대로 수행해` 같은 짧은 pointer prompt만 보내는 것을 기본값으로 삼아라.
- `tmux-send-codex`는 pointer prompt 제출 뒤 입력창에 프롬프트가 남아 있으면 3초 간격으로 최대 4회까지 `Enter`를 더 보내 확인한다. `NO_START_SIGNAL`이면 그때 pane을 직접 다시 본다.
```

## Core Rules

1. `settings/`는 공통 literary layer이고, 이 문서는 Codex supervision layer다.
2. 외부 AI 리뷰를 기본 경로에 넣지 않는다.
3. Codex native MCP(`novel-editor`, `novel-calc`, `novel-hanja`, `novel-naming`)를 우선 사용한다.
4. supervisor는 orchestrator다. 대규모 본문 재작성은 writer에게 맡긴다.
5. writer는 chapter draft + rewrite만 맡고, review 세션은 review/summaries/review-log/action-log를 맡는다.
6. review floor는 writer가 아니라 review 세션이 소비한다.
7. review floor 이하로 강등하지 않는다.
8. 아크 마지막 화 뒤에는 [ARC-BOUNDARY-CHECKLIST.md](/root/novel/codex-novel-templates-lean/ARC-BOUNDARY-CHECKLIST.md)를 강제한다.
9. supervisor는 `verify-review-done.py` 통과 후 `/root/novel/config.json`을 직접 갱신한다. writer와 review는 `config.json`을 건드리지 않는다.

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

### Open HOLD Preflight

각 화 집필 프롬프트를 보내기 전에 아래를 먼저 실행한다.

```bash
python3 ${NOVEL_DIR}/scripts/check-open-holds.py --novel-dir ${NOVEL_DIR} --current-episode ${N} --fail-on-blocker
```

- `blocker=yes`인 open HOLD가 잡히면 현재 화 집필을 멈추고 `retro-fix`, `plot-repair`, `user-escalation` 중 맞는 경로로 먼저 보낸다.
- overdue open HOLD가 있으면 같은 화에서 자연 해소 가능한지 먼저 판단하고, 불가능하면 `forward-fix` 유지가 아니라 `plot-repair` 또는 `user-escalation` 재분류를 검토한다.

`review_floor`는 writer prompt에 직접 넣지 않는다. writer는 초안과 chapter-level sanity check까지만 맡고, `continuity / standard / full` 판정과 summary 정합성은 review 세션이 맡는다.

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
- 본문은 마크다운 제목 `# {N}화 - {제목}`으로 시작하고, 파일 끝 `EPISODE_META.title`과 같은 제목을 사용한다.
- `settings/01-style-guide.md`, `settings/02-episode-structure.md`를 따른다.
- `settings/03-characters.md`에서 핵심 인물의 대표 대사, 관계 상태, 관계별 말투 규칙을 확인한다.
- `CODEX.md`의 `§8.1 호칭/어투 매트릭스`가 있으면, 이번 화에서 실제로 만나는 관계축(부모/연장자/동년배/아랫사람/적대자)을 먼저 확인한다.
- 회상, 상대 시간 표현, 이동/회복/수련 기간, deadline, 나이/연령대 단서가 있으면 `settings/05-continuity.md`를 직접 확인한다.
- planning flags를 먼저 정리한다.
- 같은 공간에 있는 이름 있는 인물을 장면에서 지우지 말고, 다음 화 오프닝에서 직전 화에 없던 보고/허락/안심/정보 전달을 기정사실처럼 점프하지 말 것.
- 본문과 대사에서 `1화에서`, `3화에서`, `프롤로그에서`, `에필로그에서`, `1부에서` 같은 메타 참조를 쓰지 않는다.
- 과거 사건은 화수/부/프롤로그 같은 메타 단위가 아니라 날짜, 장소, 사건명, 인물 기억으로만 지칭한다.
- 파일명은 `chapters/{arc}/chapter-{NN}.md`

[자기 점검]
- 이번 화의 기능이 실제로 수행되었는가?
- 현재 화 오프닝이 `직전 화 직결 앵커`와 충돌하지 않는가?
- 같은 공간의 이름 있는 인물을 빠뜨리지 않았는가?
- 화자-청자 위계가 대사 표면에 남아 있는가? 부모/연장자/사부/상급자 앞 register를 기본 반말로 평탄화하지 않았는가?
- 명백한 한국어 결합 오류나 meta 참조가 남지 않았는가?
- `EPISODE_META.title`이 본문 제목과 일치하는가?
- 필요 시 `novel-calc`, `novel-hanja`, `novel-naming` MCP를 사용한다.

[후처리 금지]
- `summaries/*` 수정 금지
- `review-log.md`, `action-log.md` 수정 금지
- `config.json` 수정 금지
- review floor 감사, 정기 점검, 아크 경계 감사 직접 수행 금지
- git commit 금지

[완료 신호]
- 이번 실행의 `RUN_NONCE`는 `{RUN_NONCE}`다.
- 가능하면 `tmp/sentinels/chapter-{NN}.done`에 같은 문자열을 먼저 기록한다.
- chapter와 `EPISODE_META` 저장이 끝난 뒤 마지막 줄에만 정확히 `WRITER_DONE chapter-{NN}.md :: run={RUN_NONCE}`를 1회 출력한다.
- 위 문자열을 계획, 메모, 자기점검, 중간 보고, 오류 설명에 다시 쓰지 말 것.

[원칙]
- 질문하지 말고 자율 완료
- summary나 review-log를 대신 닫으려 하지 말 것
- unrelated dirty files는 건드리지 말 것
```

### Continuation Within Same Chunk

```text
이어서 {N}화를 집필해줘.
- 위 규칙을 그대로 따른다.
- `novel-editor` MCP의 `compile_brief(novel_dir="{NOVEL_DIR}", episode_number={N})`를 먼저 호출한다.
- 회상, 상대 시간 표현, 이동/회복/수련 기간, deadline이 있으면 `settings/05-continuity.md`를 다시 확인한다.
- 본문 첫 줄 제목 `# {N}화 - {제목}`과 `EPISODE_META.title`을 일치시킨다.
- 현재 화 오프닝이 `직전 화 직결 앵커`와 충돌하지 않는지 먼저 확인한다.
- 본문과 대사에서 `1화에서`, `3화에서`, `프롤로그에서`, `에필로그에서`, `1부에서` 같은 메타 참조를 쓰지 않는다.
- 과거 사건은 화수/부/프롤로그 같은 메타 단위가 아니라 날짜, 장소, 사건명, 인물 기억으로만 지칭한다.
- 완료 신호는 마지막 줄의 exact sentinel `WRITER_DONE chapter-{NN}.md :: run={RUN_NONCE}` 1회만 허용한다.
- summaries/action-log/review-log는 review 세션이 맡는다.
```

## Review Session Prompt Template

### Episode Post-Write

```text
{N}화의 post-write review를 수행해줘.

[읽기]
- `chapters/{arc}/chapter-{NN}.md`
- `novel-editor` MCP의 `compile_brief(novel_dir="{NOVEL_DIR}", episode_number={N})`
- `plot/{arc}.md`
- `settings/01-style-guide.md`, `settings/03-characters.md`, 필요 시 `settings/05-continuity.md`, `settings/07-periodic.md`
- `summaries/running-context.md`, `summaries/episode-log.md`, `summaries/character-tracker.md`, `summaries/review-log.md`

[검토]
- 이번 화의 review floor는 `{review_floor}`다.
- `continuity`: 연속성, 명백한 문장 오류, summary 정합성
- 화자-청자 호칭, 존대/반말, 위계 register가 장면 관계와 충돌하면 continuity 급 결함으로 본다.
- `standard`: continuity + 서사 기능 + 반복 패턴 + WHY/HOW 설명 부족 여부
- `full`: standard + 설정/복선/아크 정합성 + 동기/행동 갭 + POV/시대/장면 논리 위험
- prose drift가 보이면 문학적 의도라고 넘기지 말고 한국어 자연성 기준으로 잡는다.

[수정 원칙]
- `micro`, `local` patch-feasible은 review 세션이 직접 수정 가능하다.
- `rewrite`급 문제는 review 세션에서 크게 다시 쓰지 말고 supervisor가 writer repair batch로 되돌리게 한다.
- open HOLD는 `review-log.md`의 권위 형식으로 기록한다.

[후처리]
- 필수: `summaries/running-context.md`, `summaries/episode-log.md`, `summaries/character-tracker.md`, `summaries/review-log.md`, `summaries/action-log.md`
- `running-context.md`에는 반드시 `Immediate Carry-Forward` 또는 `직전 화 직결 상태`를 유지한다.
- 관련 있을 때만 `desire-state.md`, `signature-moves.md`, `knowledge-map.md`, `relationship-log.md`, `decision-log.md`, `promise-tracker.md`, `repetition-watchlist.md`, `plot/foreshadowing.md`
- review 결과와 수정 여부를 `summaries/action-log.md`에 한 줄 append한다.

[완료 신호]
- rewrite급 문제 없이 post-write가 닫히면 마지막 줄에 정확히 `REVIEW_DONE chapter-{NN} :: run={RUN_NONCE}`를 1회 출력한다.
- writer repair batch가 필요하면 마지막 줄에 정확히 `REWRITE_NEEDED chapter-{NN}.md :: run={RUN_NONCE}`를 1회 출력한다.
- 위 문자열은 계획/메모/중간 보고에 재사용하지 말 것.
```

### Recheck After Writer Repair

```text
writer repair batch가 반영된 `chapters/{arc}/chapter-{NN}.md`를 재검토해줘.
- 대상 화와 직접 관련된 summary/review-log/action-log만 다시 맞춘다.
- 새 결함을 넓게 추가 탐색하지 말고, 직전 repair batch의 해결 여부를 우선 확인한다.
- 해결되면 마지막 줄에 정확히 `RECHECK_DONE chapter-{NN} :: run={RUN_NONCE}`를 1회 출력한다.
```

## Review And Repair Cycle

1. supervisor가 writer 세션에 현재 화 프롬프트를 보낸다.
2. `WRITER_DONE chapter-{NN}.md :: run={RUN_NONCE}`를 기다린 뒤 `python3 ${NOVEL_DIR}/scripts/verify-writer-done.py --novel-dir ${NOVEL_DIR} --episode ${N}`를 실행한다.
3. writer gate가 통과하면 같은 `RUN_NONCE`로 review 세션에 post-write prompt를 보낸다.
4. review 세션이 `REVIEW_DONE chapter-{NN} :: run={RUN_NONCE}`를 출력하면 `python3 ${NOVEL_DIR}/scripts/verify-review-done.py --novel-dir ${NOVEL_DIR} --episode ${N}`를 실행한다.
5. review 세션이 `REWRITE_NEEDED chapter-{NN}.md :: run={RUN_NONCE}`를 출력하면 supervisor가 새 repair nonce를 발급해 writer에 bounded repair batch를 보낸다.
6. repair batch 뒤에는 writer gate를 다시 통과시키고, review 세션에 recheck prompt를 보내 `RECHECK_DONE chapter-{NN} :: run={RUN_NONCE}`를 기다린다.
7. 최종 완료는 `verify-review-done.py` 통과 후에만 인정한다.

## Arc Transition Package

아크 마지막 화의 `REVIEW_DONE` 이후, supervisor는 review 세션에 아래를 순서대로 지시한다.

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

lean에서도 patch-feasible 분류는 review 세션이 하고, 실제 rewrite batch가 필요할 때만 writer 세션으로 되돌린다.

1. review 세션이 patch-feasible 항목을 화수별로 묶는다.
2. review 세션이 각 항목을 아래 중 하나로 분류한다.
   - `micro`: 1~3문장 사실/호응 보정
   - `local`: 문단 단위 보강/삭제/어휘 교정
   - `rewrite`: 장면 단위 재작성
3. `micro`, `local`은 review 세션이 직접 처리하고 summary/review-log를 재정합한다.
4. `rewrite`는 같은 화의 항목을 하나의 repair batch로 묶어 writer에게 보낸다.
5. writer는 해당 화 본문만 수정한다.
6. review 세션이 recheck 후 summary와 review-log를 재정합한다.
7. supervisor는 재검토 후 다음 항목으로 넘어간다.

repair batch 지시 원칙:

- 범위를 벗어난 새 설정 추가 금지
- 기존 톤/리듬/엔딩 훅 보존
- 한 화를 여러 축으로 동시에 흔들지 말고, 한 번의 배치로 끝낼 수 있게 묶기
- 재수정이 길어지면 `patch-feasible`이 아니라 `HOLD` 재분류 검토

`resolution_threshold`:

- `resolved`
  - 사실 오류와 장면 결함이 사라졌고 다음 화 carry-forward를 다시 열 수 있을 때
- `accepted_with_residuals`
  - 핵심 결함은 닫혔고 문장 밀도/리듬 같은 경미한 잔여만 남을 때
- `escalate_hold`
  - 같은 결함이 한 번의 repair batch 뒤에도 반복되거나, 2개 이상 장면 재작성이 필요해지거나, plot 변경이 필요해질 때

lean에서는 한 화당 repair batch를 1회까지만 권장한다. 그 뒤에도 `resolved`가 아니면 fix ping-pong보다 `HOLD` 라우팅을 우선한다.

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
| working | `Working`/`Reading`/`Explored`/`Edited`/`Ran` 등 진행 표시가 보이거나 출력이 계속 늘어나는 상태 | 정상 진행으로 간주. `tmux-wait-sentinel` 대기를 유지하고 추가 지시 금지 |
| waiting | 프롬프트 대기 | 다음 지시 또는 완료 검증 |
| error | traceback, file missing, command failure | 원인 확인 후 복구 지시 |
| stalled | 진행 표시도 없고 출력 증가도 없으며, sentinel도 없고, 프롬프트 대기 상태도 아닌 정체가 timeout을 넘김 | 짧은 회복 프롬프트 전송 |
| completed | writer 또는 review exact sentinel 확인 | 대응 gate 실행 후 다음 단계 판단 |

### Completion Check

한 화는 `writer gate`와 `review gate`를 모두 통과해야 완료다.

1. writer gate
   - 대상 chapter 파일 존재
   - `### EPISODE_META` 존재
   - `python3 ${NOVEL_DIR}/scripts/verify-writer-done.py --novel-dir ${NOVEL_DIR} --episode ${N}` 통과
2. review gate
   - `summaries/running-context.md`, `summaries/episode-log.md`, `summaries/character-tracker.md`, `summaries/review-log.md`, `summaries/action-log.md` 갱신
   - `running-context.md`의 `Immediate Carry-Forward` 또는 동등 섹션이 현재 화 종료 상태를 반영
   - 필요한 경우 조건부 summary도 반영
   - `python3 ${NOVEL_DIR}/scripts/verify-review-done.py --novel-dir ${NOVEL_DIR} --episode ${N}` 통과

아크 마지막 화의 review gate는 추가로 아래가 필요하다.

1. 다음 아크 런웨이 반영
2. patch-feasible/HOLD 구분 완료
3. open HOLD의 `hold_route`와 만기 화수 지정 완료
4. `blocker=yes` HOLD 없음 또는 사용자 승인 확보
5. voice profile freshness 확인 또는 다음 아크 첫 화 전 갱신 예약

## Root config.json Update

`lean`도 상위 카탈로그 `/root/novel/config.json`을 운영 대상으로 본다. episode 집필이 완료되면 supervisor가 직접 갱신한다.

### Initialization Requirement

- 프로젝트 초기화 시 `config.json`에 해당 소설 entry가 이미 있어야 한다.
- `config.json.parts` 배열 순서는 `ARC_MAP` 순서와 맞춰 둔다.
- part의 표시명은 자유지만, 순서가 어긋나면 화별 등록이 흔들린다.

### Episode Registration Rule

완료 검증 후 supervisor는 아래 순서로 `/root/novel/config.json`을 갱신한다.

1. 현재 화 번호 `N`이 속한 arc key를 `ARC_MAP`에서 찾는다.
2. chapter 파일의 `EPISODE_META`에서 `title`을 읽는다. 없으면 기본값은 `"{N}화"`다.
3. `config.json.novels[]`에서 `id == NOVEL_ID`인 entry를 찾는다.
4. `ARC_MAP` 순서와 같은 인덱스의 `parts[]`를 target part로 본다.
   - target part가 없으면 생성한다.
   - 표시명 기본값:
     - `prologue` → `프롤로그`
     - `arc-01` → `1부`
     - `arc-02` → `2부`
     - `interlude-01` → `인터루드 1`
     - `epilogue` → `에필로그`
5. target part의 `episodes` 배열에 아래 객체를 upsert 한다.

```json
{ "number": N, "title": "제목", "file": "no-title-XXX/chapters/{arc}/chapter-{NN}.md" }
```

6. 같은 `number`가 이미 있으면 덮어쓴다.
7. `episodes` 배열은 화수 오름차순으로 유지한다.
8. `totalEpisodes`는 등록된 전체 episode 수와 맞춘다.

### Timing Rule

- `config.json` 갱신은 `REVIEW_DONE` 또는 `RECHECK_DONE` 이후 `verify-review-done.py`가 통과한 뒤에만 수행한다.
- `config.json` 반영이 끝나기 전에는 다음 화 writer 프롬프트를 보내지 않는다.

## Session Management

- 기본 권장은 `CHUNK_SIZE = -1`이다. Codex의 auto-compact를 우선 믿고, 반복/맥락 누수가 실제로 보일 때만 수동 reset을 검토한다.
- supervisor는 한 화의 `writer gate + review gate + config.json 반영`이 모두 확인된 뒤에만 다음 화 프롬프트를 보낸다.

## Sentinel Discipline

- supervisor는 매 화 또는 repair batch를 보내기 직전에 고유한 `RUN_NONCE`를 만든다.
- 권장 형식은 `YYYYMMDD-epNN-xxxx` 또는 `YYYYMMDD-fixNN-xxxx`다.
- writer에게는 exact sentinel 문자열을 `[완료 신호]` 블록에서만 알려 준다.
- review 세션에도 exact sentinel 문자열을 `[완료 신호]` 블록에서만 알려 준다.
- writer는 이 문자열을 마지막 줄에 단 한 번만 출력해야 하며, 계획/메모/자기점검/중간 보고에 다시 쓰면 안 된다.
- review 세션도 `REVIEW_DONE`, `REWRITE_NEEDED`, `RECHECK_DONE` 문자열을 마지막 줄에 단 한 번만 출력해야 하며, 계획/메모/중간 보고에 다시 쓰면 안 된다.
- 가능하면 같은 문자열을 `tmp/sentinels/chapter-{NN}.done`에도 기록하게 해 file fallback을 남긴다.
- supervisor는 bare `WRITER_DONE`만 보고 완료로 판단하지 말고, 반드시 `RUN_NONCE`가 포함된 exact sentinel line을 기다린다.
- supervisor는 bare `REVIEW_DONE`나 bare `RECHECK_DONE`만 보고 완료로 판단하지 말고, 반드시 `RUN_NONCE`가 포함된 exact sentinel line을 기다린다.
- 재전송이나 repair batch 재시도 시에는 새 `RUN_NONCE`를 다시 발급하고, 이전 nonce는 폐기한다.

### Session Launch

```bash
tmux new-session -d -s ${SESSION} -c ${NOVEL_DIR} '${WRITER_CMD}'
tmux new-session -d -s ${SESSION}-review -c ${NOVEL_DIR} '${REVIEW_CMD}'
```

### Recommended Commands

```bash
tmux capture-pane -t ${SESSION} -p -S -80
tmux capture-pane -t ${SESSION}-review -p -S -80
mkdir -p ${NOVEL_DIR}/tmp/run-prompts
cat > ${NOVEL_DIR}/tmp/run-prompts/ep05-writer.txt <<'EOF'
장문 writer prompt
EOF
bash ${NOVEL_DIR}/scripts/tmux-send-codex ${SESSION} "\`${NOVEL_DIR}/tmp/run-prompts/ep05-writer.txt\`를 읽고 그대로 수행해. sentinel은 파일에 적힌 exact 문자열만 마지막 줄에 출력해." 2 80
bash ${NOVEL_DIR}/scripts/tmux-wait-sentinel ${SESSION} "WRITER_DONE chapter-05.md :: run=${RUN_NONCE}" 1800 2 200 0 ${NOVEL_DIR}/tmp/sentinels/chapter-05.done
cat > ${NOVEL_DIR}/tmp/run-prompts/ep05-review.txt <<'EOF'
장문 review prompt
EOF
bash ${NOVEL_DIR}/scripts/tmux-send-codex ${SESSION}-review "\`${NOVEL_DIR}/tmp/run-prompts/ep05-review.txt\`를 읽고 그대로 수행해. sentinel은 파일에 적힌 exact 문자열만 마지막 줄에 출력해." 2 80
bash ${NOVEL_DIR}/scripts/tmux-wait-sentinel ${SESSION}-review "REVIEW_DONE chapter-05 :: run=${RUN_NONCE}" 1800 2 200
```

- `tmux-send-codex`는 짧은 pointer prompt를 보내고, Codex의 시작 신호(`Working`, `Explored`, `Edited`, 입력 프롬프트 소멸)를 함께 확인한다.
- `tmux-wait-sentinel`은 bare `WRITER_DONE`이 아니라 `RUN_NONCE`가 붙은 exact sentinel line을 기다린다.
- `tmux-send-codex`, `tmux-wait-sentinel`, `compile_brief`, `check-open-holds.py`는 `tmp/run-metadata/events.jsonl`에 런타임 이벤트를 남긴다.
- writer sentinel이 잡혀도 supervisor는 `python3 ${NOVEL_DIR}/scripts/verify-writer-done.py --novel-dir ${NOVEL_DIR} --episode ${N}`로 초안 gate를 다시 확인한다.
- review sentinel이 잡혀도 supervisor는 `python3 ${NOVEL_DIR}/scripts/verify-review-done.py --novel-dir ${NOVEL_DIR} --episode ${N}`로 review gate를 다시 확인한다. gate 실패 시 다음 화로 진행하지 않는다.
- 장문 프롬프트는 기본적으로 `tmp/run-prompts/*.txt`에 저장하고, tmux에는 파일 경로를 읽게 하는 짧은 pointer prompt만 보낸다.
- `tmux-send-codex`는 prompt가 입력창에 남아 있으면 3초 간격으로 최대 4회까지 `Enter`를 더 보낸다. 그래도 `NO_START_SIGNAL`이면 pointer prompt 잔류 여부와 pane 출력 증가를 직접 재확인한다.
- 시작 신호가 없더라도 마지막 입력 프롬프트 줄이 아직 남아 있으면 "멈춤"보다 "아직 제출 대기"로 우선 해석한다. 프롬프트가 실제로 사라졌거나 새 출력이 시작된 뒤에만 다음 상태 판정을 진행한다.
- `WORKING_CONFIRMED`, `WORKING_CONFIRMED_AFTER_EXTRA_ENTERS`, `RESPONSE_CONFIRMED`, `PROMPT_DISAPPEARED` 중 하나가 잡힌 뒤에는 writer가 문서를 읽거나 계획을 세우는 구간도 정상 진행으로 본다. 이 단계에서는 새 프롬프트를 덧붙이지 말고 `tmux-wait-sentinel` 또는 명시적 장기 timeout까지 기다린다.
- `tmux-wait-sentinel`은 기존 pane에 남아 있던 sentinel과 새로 출력된 sentinel을 구분해 대기한다.

## Recovery Rules

- writer가 질문을 던지고 멈췄으면, 가능한 범위에서 supervisor가 결정해 짧게 답한다.
- review 세션이 rewrite 필요를 명시하면, supervisor는 review 세션에서 본문을 크게 다시 쓰게 하지 말고 writer repair batch로 되돌린다.
- `working` 판정 중에는 same-state처럼 보여도 회복 프롬프트를 넣지 않는다. 문서 읽기, 파일 탐색, 계획 정리는 정상 작업으로 간주한다.
- 회복 프롬프트는 `working`이 아닌 상태에서 `tmux-wait-sentinel` timeout 또는 명백한 입력 대기/오류가 확인됐을 때만 보낸다.
- same-state 정체가 길더라도 먼저 pane 재캡처로 출력 증가 여부와 마지막 20~80줄 변화를 확인한 뒤, 정말 무변화일 때만 "현재 단계만 마무리하고 다음 단계로 진행" 같은 회복 프롬프트를 넣는다.
- crash 시에는 파일 기준으로 마지막 완료 화를 다시 판정하고 그 다음 화부터 재개한다.

## Voice Profile Freshness Handoff

아크 경계나 반복 drift가 의심될 때는 `settings/01-style-guide.md` §0.3 대표 문단이 현재 실제 서술 목소리와 계속 맞는지 확인한다.

권장 절차:

1. 최근 아크 범위에 대해 아래를 실행한다.

```bash
python3 ${NOVEL_DIR}/scripts/suggest-voice-profile-refresh.py --novel-dir ${NOVEL_DIR} --from-episode ${ARC_START} --to-episode ${ARC_END} --top 5
```

2. 후보 문단 중 현재 화자/리듬/시점 운용을 가장 잘 대표하는 것을 골라 §0.3을 갱신한다.
3. 적절한 문단을 바로 확정하기 어렵다면 `summaries/review-log.md`에 open HOLD로 남기고, 다음 아크 첫 화 전까지 처리한다.

이 handoff는 "문체를 새로 발명"하는 절차가 아니라, 실제로 굴러간 voice를 style guide에 다시 동기화하는 절차다.

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
2. review 세션이 summary와 review-log를 맞춘다.
3. 정기 점검을 누락하지 않는다.
4. 아크 경계에서 감사와 런웨이 정리를 빠뜨리지 않는다.
5. `verify-review-done.py`를 통과하기 전에는 완료로 치지 않는다.

이 다섯 가지가 지켜지지 않으면 완료로 치지 않는다.
