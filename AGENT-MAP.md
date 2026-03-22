# Claude -> Codex Agent Map

Codex에서는 Claude의 `.claude/agents/*.md`를 그대로 실행하지 않는다. 대신 역할을 아래처럼 압축해서 운용한다.

| Claude Lean Role | Codex Role | 비고 |
|---|---|---|
| writer | writer | 본문 작성, 부분 재작성 |
| unified-reviewer | continuity-reviewer + narrative-reviewer + korean-reviewer | 필요 시 1개 또는 3개로 분할 |
| story-consultant | concept-reviewer | 초기 기획 검증 |
| why-checker | plot-checker | 설명 갭, 인과, 질문 누락 |
| oag-checker | plot-checker | 동기/행동 갭은 같은 축으로 묶는다 |
| plot-surgeon | plot-repairer | 플롯 파일 수정과 rewrite brief 생성 |
| korean-naturalness | korean-reviewer | 교정 전용 |
| full-audit | full-auditor | 장편 전체 감사 |

## 왜 이렇게 줄이나

Codex의 강점은 "프로젝트 파일을 직접 읽고 수정하며 필요할 때 서브에이전트를 띄우는 것"이다. Claude처럼 프로젝트 안에 세밀한 agent 정의를 많이 둘수록 이식 비용만 커진다.

그래서 1차 Codex 버전은 아래 5역할이면 충분하다.

1. writer
2. continuity-reviewer
3. narrative-reviewer
4. korean-reviewer
5. plot-checker

이 정도면 실제 집필 테스트를 시작할 수 있다.
