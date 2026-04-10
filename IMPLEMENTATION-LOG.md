# Codex Lean Template Implementation Log

이 문서는 `claude-codex-novel-templates-hybrid`에 먼저 적용한 안정화/품질 보강 패치 중, `codex-novel-templates-lean`에 실제로 이식한 항목만 추려 기록한다.

## 목표

- Codex 단독 운영에서도 runtime 상태를 관찰할 수 있게 만들기
- `compile_brief`가 실제 집필 직전에 필요한 cue를 먼저 보여주게 만들기
- open HOLD를 writer가 모른 채 덮어쓰는 상황을 줄이기
- drift를 테스트와 validator로 빨리 잡을 수 있게 만들기

## 적용 범위

## Commit Inventory

| Commit | 제목 | 핵심 범위 |
|--------|------|-----------|
| `351b78e` | `Add lean runtime observability helpers` | `tmux-send-codex`, `tmux-wait-sentinel`, `event-log.py`, `check-open-holds.py`, `summarize-runtime-metrics.py`, `suggest-voice-profile-refresh.py`, `.gitignore`, `scripts/README.md` |
| `f7c661b` | `Add lean live cues and HOLD handoff support` | `compile_brief` live cues/runtime snapshot, `CODEX.md`, `batch-supervisor.md`, `03-characters.md`, `review-log.md`, `running-context.md`, `desire-state.md`, `signature-moves.md` |

### 1. Runtime Observability

- `scripts/event-log.py`
  - helper와 `compile_brief`가 `tmp/run-metadata/events.jsonl`에 이벤트를 남긴다.
- `scripts/tmux-send-codex`
  - `WORKING_CONFIRMED`, `RESPONSE_CONFIRMED`, `PROMPT_DISAPPEARED`, `NO_START_SIGNAL` 등 결과를 이벤트로 기록한다.
- `scripts/tmux-wait-sentinel`
  - start/result 이벤트를 기록한다.
  - optional sentinel file fallback(`tmp/sentinels/chapter-{NN}.done`)을 지원한다.
- `scripts/summarize-runtime-metrics.py`
  - read error, hold check, tmux helper 결과, brief size를 요약한다.

### 2. HOLD Operations

- `scripts/check-open-holds.py`
  - `summaries/review-log.md`의 open HOLD를 읽어 overdue / blocker를 기계적으로 판정한다.
- `batch-supervisor.md`
  - 각 화 집필 전 `check-open-holds.py` preflight를 추가했다.
  - blocker HOLD가 있으면 집필보다 fix routing을 먼저 타도록 명시했다.
- `summaries/review-log.md`
  - canonical HOLD block 예시를 추가했다.
- `summaries/running-context.md`
  - `## HOLD 경고` 섹션을 추가했다.

### 3. Drafting Surface / Live Fields

- `compile_brief.py`
  - `## Live Drafting Cues`를 추가했다.
  - 이번 화 기능, 직전 화 마지막 장면 압축, carry-forward, 엔딩 훅, 보이스 우선순위, 어휘 치환, 대사 경고, 반복 패턴, decision-log, open HOLD, desire-state, signature-moves를 집필 전 cue로 노출한다.
  - `tmp/briefs/chapter-{NN}.md` snapshot 저장과 `compile_brief_complete` 이벤트 기록을 추가했다.
  - `settings/01-style-guide.md` parser를 정리해 `### 시점`, `### 우선 원칙`이 중복/잡음 없이 나오게 했다.
- `summaries/desire-state.md`
  - `Current Desire / Current Anxiety / This Episode Touchpoints` 템플릿 추가
- `summaries/signature-moves.md`
  - `Opening / Pressure / Landing / Overused Moves` 템플릿 추가
- `settings/03-characters.md`
  - `말 길이 경향`, `회피 반응`, `대화 대비축` 필드 추가
- `CODEX.md`
  - `running-context` HOLD 경고와 `desire-state`, `signature-moves` 갱신 규칙을 post-processing에 반영했다.

### 4. Validation / Tests

- `scripts/validate-settings.py`
  - `01-style-guide.md`, `03-characters.md`, `running-context.md`, `desire-state.md`, `signature-moves.md` 최소 계약을 검사한다.
- `scripts/verify-writer-done.py`
  - writer sentinel 뒤 chapter / action-log / episode-log / carry-forward가 실제로 닫혔는지 파일 기준으로 검증한다.
- `tests/test_compile_brief.py`
  - fixture 기반 snapshot, live cues, HOLD/live fields, style parser, snapshot/event, validator 검증
- `tests/test_runtime_helpers.py`
  - `tmux-send-codex`, `tmux-wait-sentinel`, `check-open-holds.py`, `verify-writer-done.py`, `summarize-runtime-metrics.py`, `suggest-voice-profile-refresh.py` 검증
  - sandbox에서 tmux socket이 막히면 helper smoke test는 skip
- `tests/golden/brief-ep2.md`
  - 새 `compile_brief` 출력 기준 snapshot

### 5. Supervisor Handoff Tightening

- `batch-supervisor.md`
  - `resolution_threshold`를 명시해 repair batch가 한 화에서 무한 반복되지 않게 했다.
  - sentinel 확인 뒤 `verify-writer-done.py` gate를 통과해야 다음 화로 넘어가게 했다.
  - 아크 경계에 `Voice Profile Freshness Handoff`를 추가해 `suggest-voice-profile-refresh.py` 결과를 §0.3 갱신 또는 HOLD로 연결했다.
- `CODEX.md`
  - batch 경로의 writer completion gate와 arc-boundary voice refresh 규칙을 반영했다.
- `skills/codex-batch-supervisor/SKILL.md`
  - supervisor skill의 완료 검증과 arc 경계 규칙에도 같은 gate/handoff를 반영했다.

## Verification

실행한 검증:

```bash
python3 -m py_compile compile_brief.py scripts/event-log.py scripts/check-open-holds.py scripts/summarize-runtime-metrics.py scripts/suggest-voice-profile-refresh.py scripts/validate-settings.py scripts/verify-writer-done.py tests/test_compile_brief.py tests/test_runtime_helpers.py
pytest -q tests/test_compile_brief.py tests/test_runtime_helpers.py
python3 scripts/validate-settings.py --novel-dir /root/novel/codex-novel-templates-lean
```

확인 결과:

- `pytest`: `12 passed, 2 skipped`
- `validate-settings.py`: `VALID settings/running-context contract OK`
- `verify-writer-done.py`: `GATE_OK episode=01 chapter=chapters/arc-01/chapter-01.md`
- escalated tmux smoke:
  - `tmux-send-codex` → `WORKING_CONFIRMED`
  - `tmux-wait-sentinel` → `SENTINEL_FOUND mode=file_fallback`
  - 두 helper 모두 `events.jsonl` 기록 확인

## Notes

- `lean`에는 기존에 nonce/sentinel discipline과 tmux state 해석 개선이 이미 일부 들어가 있었고, 이번 패치는 그 위에 observability/live cues/test를 얹는 형태로 진행했다.
- `Creative Selector`, 문서 증설, reference works 기반 문체 복제 같은 항목은 이번 라운드에서도 넣지 않았다.
