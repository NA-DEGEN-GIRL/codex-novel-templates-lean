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

```bash
bash scripts/tmux-send-codex write-001 "continue" 2 60
```

### `scripts/tmux-wait-sentinel`

tmux pane을 폴링해서 `WRITER_DONE ...` 또는 `FIX_DONE ...` 같은 sentinel 문자열을 기다린다. 시작 시 pane에 이미 남아 있던 sentinel과 새로 나온 sentinel을 구분한다.

```bash
bash scripts/tmux-wait-sentinel write-001 "WRITER_DONE chapter-05.md" 1800 2 200
bash scripts/tmux-wait-sentinel write-001 "FIX_DONE chapter-05" 600 1 120
```

## Notes

- 이 스크립트들은 MCP 연결 없이 로컬 import 방식으로 동작한다.
- lean의 기본 경로는 native MCP이고, `compile-brief` / `novel-calc` / `novel-hanja`는 compatibility fallback이다.
- `mcp` 파이썬 패키지가 설치되어 있어야 서버 모듈 import가 된다.
- 경로는 현재 워크스페이스(`/root/novel/...`) 기준으로 고정되어 있다.
- `run-codex-writer` / `run-codex-supervisor` / `run-codex-auditor`는 승인 프롬프트를 최대한 없애기 위해 `--dangerously-bypass-approvals-and-sandbox`를 사용한다.
- `tmux-send-codex`는 Codex의 Enter 타이밍 quirks를 흡수하고, 멀티라인 프롬프트도 첫 줄 기준으로 마지막 입력 프롬프트 줄만 확인한다.
- `tmux-wait-sentinel`은 기존 pane에 남은 sentinel을 새 완료 신호로 오인하지 않도록 기본적으로 무시한다.
- 이 옵션은 외부 샌드박스나 사용자가 환경을 통제하고 있을 때만 쓰는 것이 맞다.
