# Codex Init Prompt

> `/root/novel/`에서 Codex를 열고 아래 프롬프트를 붙여넣는다.
> 목표는 "새 소설 프로젝트 생성 + 초기 검증 + Codex 운영 레이어 정렬"까지다. 에피소드 집필은 하지 않는다.

## Prompt

```text
codex-novel-templates-lean/ 를 참고해서 새 소설 프로젝트를 만들어줘.

## 조건

- 장르: [장르]
- 톤: [톤앤무드]
- 분량: [에피소드 목표 분량]
- 총 화수: [목표 화수]
- 특이사항: [있으면 적기]

## 작업 원칙

- 에피소드 본문은 쓰지 마라. 프로젝트 셋업만 한다.
- 템플릿의 `settings/`, `plot/`, `summaries/` 구조를 유지하라.
- `CODEX.md`를 기준 운영 문서로 삼아라.
- Claude 전용 `.claude/commands`를 흉내내지 말고, Codex 기준 역할 분리로 설계하라.
- 외부 AI 리뷰를 기본 경로에 넣지 마라.
- `compile_brief`가 `CODEX.md` 기준으로 작동하는 구조를 유지하라.
- Codex에서 등록된 MCP(`novel-editor`, `novel-calc`, `novel-hanja`, `novel-naming`)를 사용할 수 있다고 가정하라.
- `scripts/`에는 MCP fallback wrapper와 tmux helper(`tmux-send-codex`, `tmux-wait-sentinel`)를 함께 유지하라.
- 아크 경계 감사와 정기 점검이 문서 레벨에서 빠지지 않게 구성하라.

## 진행 순서

1. 컨셉 3개 제안
   - 제목
   - 한줄 소개
   - 주인공
   - 핵심 갈등
   - 예상 아크
   - 차별점

2. 선택한 컨셉 확장
   - 주요 캐릭터 3~5명
   - 핵심 약속 3개
   - 아크 구성
   - 세계관 핵심 규칙

3. 프로젝트 생성
   - 새 폴더 생성
   - `codex-novel-templates-lean/`의 `settings/`, `plot/`, `summaries/`, `chapters/`, `reference/`, `scripts/`, `skills/`, `compile_brief.py`, `CODEX.md`, `batch-supervisor.md`, `batch-supervisor-audit.md`, `ARC-BOUNDARY-CHECKLIST.md`를 복사
   - 작품용 `CLAUDE.md` 대신 `CODEX.md`를 채운다
   - `plot/master-outline.md`, `plot/arc-01.md`, `plot/foreshadowing.md`를 실제 내용으로 채운다
   - `plot`의 고위험 화수에는 optional `risk:` 필드(`why`, `oag`, `pov-era`, `scene-logic`)를 넣을 수 있게 구조를 유지한다
   - `summaries/` 초기 파일에서 placeholder와 작품 전용 규칙 누락을 점검한다 (`running-context`, `character-tracker`, `knowledge-map`, `dialogue-log` 포함)
   - `summaries/running-context.md`에 `Immediate Carry-Forward` 섹션이 있는지 확인한다
   - `scripts/run-codex-writer`, `scripts/run-codex-supervisor`, `scripts/run-codex-auditor`, `scripts/tmux-send-codex`, `scripts/tmux-wait-sentinel`가 usable 한지 확인한다
   - `README.md`와 `CODEX.md`에 native MCP 우선 / scripts fallback 구조가 반영되게 한다

4. 사전 검증
   - writer runtime preflight: `01-style-guide.md` → `03-characters.md` → `02-episode-structure.md` 순으로 실제 Codex writer 기준 GO/REVISE 판정
   - 동기 갭 점검
   - WHY/HOW 설명 갭 점검
   - 설정/플롯/캐릭터 상호 모순 점검
   - `settings/07-periodic.md`와 `ARC-BOUNDARY-CHECKLIST.md`가 현재 아크 설계와 충돌하지 않는지 점검
   - `compile_brief.py`와 `novel-editor` MCP의 `compile_brief` 경로가 `CODEX.md`와 초기 summary를 읽는 데 무리가 없는지 점검

5. 보고
   - 생성한 파일 목록
   - 남은 리스크
   - 바로 집필 가능한지 여부
   - 첫 집필 전 추천 실행 순서
   - 첫 아크 종료 후 반드시 돌릴 감사 절차

## 검토 기준

- 캐릭터 목표와 플롯 요구가 충돌하지 않는가
- 핵심 약속 3개가 아크에 실제로 반영되는가
- 세계관 규칙이 장르 쾌감과 충돌하지 않는가
- 1아크까지 읽었을 때 다음 화를 누를 이유가 충분한가
- `CODEX.md`만 읽어도 writer / supervisor / auditor가 어떤 순서로 움직여야 하는지 분명한가
- 정기 점검과 아크 경계 감사가 운영 문서에 빠짐없이 연결되어 있는가
```
