# Codex Utility Scripts

Codex에서 기존 lean의 핵심 도구 일부를 셸 명령처럼 쓰기 위한 로컬 래퍼.

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
scripts/novel-hanja hanja_verify text='"천외귀환(天外歸還)"' novel_id='"no-title-001"'
```

## Notes

- 이 스크립트들은 MCP 연결 없이 로컬 import 방식으로 동작한다.
- `mcp` 파이썬 패키지가 설치되어 있어야 서버 모듈 import가 된다.
- 경로는 현재 워크스페이스(`/root/novel/...`) 기준으로 고정되어 있다.
