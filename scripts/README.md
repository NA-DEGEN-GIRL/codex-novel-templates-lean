# Codex Lean Runtime Scripts

Codex lean의 기본 경로는 **native MCP 직접 호출**이다.

- `compile_brief`
- `novel-calc`
- `novel-hanja`
- `novel-naming`

하지만 lean은 MCP fallback wrapper와 tmux/session helper를 함께 둔다.
즉 `scripts/`는 둘 다 포함한다.

1. MCP 미등록, 일시 장애, 로컬 디버깅용 compatibility wrapper
2. Codex tmux writer/supervisor 운영용 helper

## Available

### `scripts/compile-brief`

`compile_brief.py`를 직접 실행한다.

```bash
scripts/compile-brief /root/novel/no-title-001-gpt 7
scripts/compile-brief /root/novel/no-title-001-gpt 7 "윤서하,리라"
```

### `scripts/novel-calc`

`mcp-novel-calc`의 함수들을 CLI처럼 호출한다.

```bash
scripts/novel-calc calculate expression='"1250 * 1.35"'
scripts/novel-calc date_calc date_str='"2026-03-22"' operation='"add"' days=3
scripts/novel-calc char_count file_path='"/root/novel/no-title-001-gpt/chapters/arc-01/chapter-01.md"'
```

JSON 방식도 가능하다.

```bash
scripts/novel-calc date_calc --json '{"date_str":"2026-03-22","operation":"add","days":3}'
```

### `scripts/novel-hanja`

`mcp-novel-hanja`의 함수들을 CLI처럼 호출한다.

```bash
scripts/novel-hanja hanja_lookup text='"天外歸還"'
scripts/novel-hanja hanja_search reading='"검"' meaning_hint='"칼"'
scripts/novel-hanja hanja_verify text='"천외귀환(天外歸還)"' novel_id='"no-title-001-gpt"'
```

### `scripts/run-codex-writer`

현재 프로젝트 디렉터리에서 Codex를 전체 승인/샌드박스 우회 모드로 실행한다.

```bash
scripts/run-codex-writer
```

### `scripts/run-codex-supervisor`

`/root/novel`에서 supervisor Codex를 전체 승인/샌드박스 우회 모드로 실행한다.

```bash
/root/novel/codex-novel-templates-lean/scripts/run-codex-supervisor
```

### `scripts/run-codex-auditor`

현재 프로젝트 디렉터리에서 감사 전용 Codex 세션을 실행한다.

```bash
scripts/run-codex-auditor
```

### `scripts/tmux-send-codex`

Codex tmux 세션에 프롬프트를 보내고, `2초` 안에 `Working`뿐 아니라 `Explored`/`Edited`/`Ran`/`Reading` 같은 진행 표시, 새 응답 블록, 또는 입력 프롬프트 소멸을 시작 신호로 본다. 셋 다 안 보이면 `Enter`를 한 번만 다시 보내고 재확인한다.

긴 멀티라인 프롬프트는 paste 후 첫 `Enter`, 심지어 1회 재시도 뒤에도 실제 제출이 안 될 수 있다. 이때 `NO_START_SIGNAL`만 보고 곧바로 stalled로 판정하지 말고, pane을 다시 캡처해서 마지막 입력 프롬프트 줄이 **현재 pane 바닥에 실제로 남아 있는지** 확인한 뒤 `Enter`를 1~2회 추가로 보내 재확인하는 편이 안전하다.

```bash
bash scripts/tmux-send-codex write-001 "continue" 2 60
```

### `scripts/tmux-wait-sentinel`

tmux pane을 폴링해서 `WRITER_DONE ... :: run=...` 또는 `FIX_DONE ... :: run=...` 같은 exact sentinel 문자열을 기다린다. 시작 시 pane에 이미 남아 있던 sentinel과 새로 나온 sentinel을 구분한다.

권장 방식은 supervisor가 매 실행마다 고유한 `RUN_NONCE`를 만들어 exact line을 기다리는 것이다. bare `WRITER_DONE`만 기다리면 오탐 여지가 커진다.

```bash
bash scripts/tmux-wait-sentinel write-001 "WRITER_DONE chapter-05.md :: run=20260407-ep05-a1c9" 1800 2 200
bash scripts/tmux-wait-sentinel write-001 "FIX_DONE chapter-05 :: run=20260407-fix05-b13e" 600 1 120
bash scripts/tmux-wait-sentinel write-001 "WRITER_DONE chapter-05.md :: run=20260407-ep05-a1c9" 1800 2 200 0 tmp/sentinels/chapter-05.done
```

### `scripts/event-log.py`

helper와 `compile_brief`가 남기는 런타임 이벤트를 `tmp/run-metadata/events.jsonl`에 append한다.

### `scripts/check-open-holds.py`

`summaries/review-log.md`의 open HOLD를 읽어 blocker / overdue 상태를 판정한다.

```bash
python3 scripts/check-open-holds.py --novel-dir /root/novel/no-title-001-gpt --current-episode 12 --fail-on-blocker
```

### `scripts/verify-writer-done.py`

writer sentinel 이후 chapter/summary/action-log/carry-forward가 실제로 닫혔는지 파일 기준으로 검증한다.

```bash
python3 scripts/verify-writer-done.py --novel-dir /root/novel/no-title-001-gpt --episode 12
```

### `scripts/summarize-runtime-metrics.py`

`events.jsonl`을 요약해서 runtime 안정화 지표를 본다.

```bash
python3 scripts/summarize-runtime-metrics.py --novel-dir /root/novel/no-title-001-gpt --format markdown
```

### `scripts/suggest-voice-profile-refresh.py`

최근 화에서 §0.3 대표 문단 후보를 추출한다. 아크 경계 voice freshness 점검이나 `01-style-guide.md` §0.3 갱신 후보를 고를 때 쓴다.

```bash
python3 scripts/suggest-voice-profile-refresh.py --novel-dir /root/novel/no-title-001-gpt --from-episode 1 --to-episode 20 --top 5
```

### `scripts/validate-settings.py`

`running-context`, `desire-state`, `signature-moves`, `03-characters`, `01-style-guide`의 최소 계약을 검사한다.

```bash
python3 scripts/validate-settings.py --novel-dir /root/novel/no-title-001-gpt
```

## Notes

- 이 스크립트들은 MCP 연결 없이 로컬 import 방식으로 동작한다.
- lean의 기본 경로는 native MCP이고, `compile-brief` / `novel-calc` / `novel-hanja`는 compatibility fallback이다.
- `mcp` 파이썬 패키지가 설치되어 있어야 서버 모듈 import가 된다.
- 경로는 현재 워크스페이스(`/root/novel/...`) 기준으로 고정되어 있다.
- `run-codex-writer` / `run-codex-supervisor` / `run-codex-auditor`는 승인 프롬프트를 최대한 없애기 위해 `--dangerously-bypass-approvals-and-sandbox`를 사용한다.
- `tmux-send-codex`는 Codex의 Enter 타이밍 quirks를 흡수하고, 멀티라인 프롬프트도 첫 줄 기준으로 마지막 입력 프롬프트 줄이 **현재 pane 바닥에 남아 있는지**만 확인한다. 오래된 prompt echo만 남아 있으면 추가 Enter를 보내지 않는다.
- 다만 매우 긴 paste에서는 helper의 1회 재시도만으로 부족할 수 있으므로, supervisor는 마지막 입력 프롬프트 줄 잔류 여부를 보고 수동 `Enter` 추가 전송 가능성을 항상 열어 둔다.
- `tmux-wait-sentinel`은 기존 pane에 남은 sentinel을 새 완료 신호로 오인하지 않도록 기본적으로 무시한다.
- `tmux-send-codex`, `tmux-wait-sentinel`, `compile_brief`, `check-open-holds.py`는 `tmp/run-metadata/events.jsonl`에 이벤트를 남긴다.
- `verify-writer-done.py`도 gate pass/fail을 `events.jsonl`에 남긴다.
- `tmux-wait-sentinel`은 optional sentinel file fallback도 지원한다.
- 추천 sentinel 형식은 `WRITER_DONE chapter-{NN}.md :: run={RUN_NONCE}`처럼 nonce가 붙은 exact 한 줄이다.
- 이 옵션은 외부 샌드박스나 사용자가 환경을 통제하고 있을 때만 쓰는 것이 맞다.
