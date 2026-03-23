# Codex Role Map

이 문서는 런타임 필수 문서가 아니다. Codex 프로젝트에서 역할을 어떻게 단순화해 볼 수 있는지 설명하는 참고 메모다.

| Legacy Role Name | Codex Role | 비고 |
|---|---|---|
| writer | writer | 본문 작성, 부분 재작성 |
| unified-reviewer | continuity-reviewer + narrative-reviewer + korean-reviewer | 필요 시 1개 또는 3개로 분할 |
| story-consultant | concept-reviewer | 초기 기획 검증 |
| why-checker | plot-checker | 설명 갭, 인과, 질문 누락 |
| oag-checker | plot-checker | 동기/행동 갭은 같은 축으로 묶는다 |
| pov-era-checker | plot-checker + korean-reviewer | 시점 지식/시대 어휘 위반 점검 |
| scene-logic-checker | continuity-reviewer | 장면 내부 물리 논리 점검 |
| repetition-checker | narrative-reviewer | 반복 패턴 탐지 |
| plot-surgeon | plot-repairer | 플롯 파일 수정과 rewrite brief 생성 |
| korean-naturalness | korean-reviewer | 교정 전용 |
| full-audit | full-auditor | 장편 전체 감사 |

## 왜 이렇게 줄이나

Codex의 강점은 프로젝트 파일을 직접 읽고 수정하며 필요할 때 역할을 가볍게 나누는 데 있다. 세밀한 agent 정의를 많이 둘수록 유지 비용만 커진다.

그래서 실무상 최소 Codex 역할 세트는 아래다.

1. writer
2. continuity-reviewer
3. narrative-reviewer
4. korean-reviewer
5. plot-checker
6. plot-repairer (필요 시)
7. full-auditor (범위 감사 시)

집필만 할 때는 1~5면 충분하고, 범위 감사까지 갈 때만 6~7이 추가된다.
