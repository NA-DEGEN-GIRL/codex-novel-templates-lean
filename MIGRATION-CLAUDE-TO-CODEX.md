# Claude Project -> Codex Project Migration Prompt

> 기존 Claude 기반 소설 프로젝트를 Codex 운영 방식으로 옮길 때 쓰는 프롬프트.
> 목표는 "집필 가능한 Codex 버전"을 만드는 것이지, Claude 내부 명령 체계를 억지로 복제하는 것이 아니다.

## 사용법

```bash
cd /root/novel
```

아래 프롬프트를 Codex에 붙여넣는다.

## Prompt

```text
codex-novel-templates-lean/ 를 기준으로 [프로젝트명]/ 을 Codex 운영형 프로젝트로 마이그레이션해줘.

## 절대 금지

- `chapters/` 본문은 수정하지 마라.
- 기존 설정, 캐릭터, 세계관 의미를 바꾸지 마라.
- 이미 있는 `summaries/` 내용을 삭제하지 마라.
- Claude 전용 파일을 Codex에서 쓸 수 있다고 가정하지 마라.

## 목표

- Claude 중심 운영 문서를 Codex 중심 운영 문서로 치환
- 핵심 소설 데이터 구조(`settings/`, `plot/`, `summaries/`, `chapters/`) 유지
- Codex에서 다음 화 집필이 가능한 최소 상태 확보
- 필요한 경우에만 얇은 자동화 제안

## 단계

### 1. 인벤토리

먼저 수정 없이 아래를 정리해라.

- 현재 폴더 구조
- `.claude/agents` / `.claude/commands` 목록
- 작품 고유 규칙
- Codex로 옮겨야 할 핵심 운영 규칙
- Codex에서 버릴 수 있는 Claude 전용 요소

### 2. 매핑 계획

아래 매핑표를 만든다.

- `CLAUDE.md` -> `CODEX.md`
- `.claude/agents/writer.md` -> Codex writer workflow
- `.claude/agents/unified-reviewer.md` -> Codex review checklist
- `why-check`, `oag-check` -> plot-check workflow
- `batch-supervisor.md` -> Codex 운영 메모 또는 수동 배치 절차

위험 요소와 롤백 기준도 적는다.

### 3. Codex 문서 생성

프로젝트 안에 아래를 만든다.

- `CODEX.md`
- `MIGRATION-NOTES-CODEX.md`

필요하면 아래도 만든다.

- `PROMPTS/next-episode.md`
- `PROMPTS/partial-rewrite.md`
- `PROMPTS/arc-review.md`

### 4. 운영 규칙 이식

기존 `CLAUDE.md`에서 아래를 보존해 `CODEX.md`에 옮긴다.

- Project overview
- core promises
- thematic statement
- prohibitions
- file priority
- writing workflow
- summary update rule

의미는 보존하고, Codex 기준으로 표현만 바꿔라.

### 5. Claude 전용 요소 분리

`.claude/` 폴더는 바로 삭제하지 말고 다음 중 하나로 처리한다.

- 계속 보관: reference-only
- 또는 `archive/claude-runtime/`로 이동

중요한 점은 Codex가 이 폴더에 의존하지 않는 상태를 만드는 것이다.

### 6. 검증

아래를 확인한다.

- `chapters/` diff 없음
- `CODEX.md`만 읽어도 다음 화 작업 순서를 이해할 수 있음
- `summaries/`와 `plot/`가 여전히 참조 가능함
- Codex 기준 집필 절차가 과도하게 Claude 명령어에 묶여 있지 않음

### 7. 결과 보고

아래 형식으로 요약한다.

1. 유지한 것
2. 치환한 것
3. 보류한 것
4. 지금 바로 집필 가능한지
5. 다음 자동화 우선순위 3개

## 중요 판단 기준

- Codex에서 실제로 돌릴 수 있는가
- 새 사람이 봐도 운영 방식이 이해되는가
- Claude 기능 부재가 치명적이지 않은가
- 자동화 없이도 한 화를 쓸 수 있는가
```

## 권장 해석

이 프롬프트는 "모든 Claude agent를 Codex skill/MCP로 먼저 다시 만들자"는 방향을 피한다. 먼저 운영 문서와 프로젝트 구조를 Codex 친화적으로 바꾼 뒤, 반복 비용이 큰 부분만 자동화하는 순서가 맞다.
