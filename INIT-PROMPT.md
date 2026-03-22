# Codex Init Prompt

> `/root/novel/`에서 Codex를 열고 아래 프롬프트를 붙여넣는다.
> 목표는 "새 소설 프로젝트 생성 + 초기 검증"까지다. 에피소드 집필은 하지 않는다.

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
   - `codex-novel-templates-lean/`의 `settings/`, `plot/`, `summaries/`, `chapters/`, `reference/`, `compile_brief.py`, `CODEX.md`를 복사
   - 작품용 `CLAUDE.md` 대신 `CODEX.md`를 채운다
   - `plot/master-outline.md`, `plot/arc-01.md`, `plot/foreshadowing.md`를 실제 내용으로 채운다
   - `summaries/` 초기 파일을 점검한다

4. 사전 검증
   - 동기 갭 점검
   - WHY/HOW 설명 갭 점검
   - 설정/플롯/캐릭터 상호 모순 점검

5. 보고
   - 생성한 파일 목록
   - 남은 리스크
   - 바로 집필 가능한지 여부

## 검토 기준

- 캐릭터 목표와 플롯 요구가 충돌하지 않는가
- 핵심 약속 3개가 아크에 실제로 반영되는가
- 세계관 규칙이 장르 쾌감과 충돌하지 않는가
- 1아크까지 읽었을 때 다음 화를 누를 이유가 충분한가
```
