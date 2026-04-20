# Day7 Project Summary

## 프로젝트 한 줄 정의

정적인 이미지와 언어 지시, candidate objects를 기반으로 target object를 고르고, short-horizon subgoal을 선택한 뒤, 확신이 낮으면 abstain하는 grounded decision toy-project.

---

## 왜 이 프로젝트를 했는가

VLA 기반 mobile manipulation을 처음부터 end-to-end로 구현하는 것은 범위가 너무 크다.

그래서 이 프로젝트는 실제 control이나 trajectory planning이 아니라, action 이전 단계의 판단 문제에 집중했다.

구체적으로는 다음 질문을 다뤘다.

1. instruction이 가리키는 target object를 고를 수 있는가?
2. target이 정해졌을 때 다음 short-horizon subgoal을 고를 수 있는가?
3. 선택의 신뢰도를 consistency score로 표현할 수 있는가?
4. 확신이 낮을 때 abstain할 수 있는가?
5. mobile-like scene에서 기존 baseline은 어디서 무너지는가?

---

## Day별 진행 요약

### Day1
프로젝트 문제 정의를 했다.

### Day2
입력/출력 스키마를 정했다.

### Day3
candidate object annotation과 target grounding baseline을 만들었다.

### Day4
baseline prediction을 reasoning 관점으로 해석하는 check script를 만들었다.

### Day5
mobile-like scene을 추가하고 기존 baseline의 한계를 확인했다.

### Day6
Day5 결과를 failure taxonomy로 분석했다.

### Day7
전체 프로젝트를 연구 방향으로 정리했다.

---

## 현재 프로젝트의 범위

### 포함
- single RGB image 기반 설정
- single instruction
- candidate object 기반 target selection
- short-horizon subgoal prediction
- consistency scoring
- abstention
- mobile-like difficulty scene
- failure analysis

### 제외
- real robot control
- low-level trajectory planning
- segmentation
- object detector 학습
- video history
- memory
- replanning
- Isaac Sim 연동

---

## 핵심 결론

이 프로젝트는 로봇을 움직인 프로젝트가 아니라, 로봇이 움직이기 전에 무엇을 해야 하는지 판단하는 grounded decision layer를 작게 검증한 프로젝트다.

특히 Day5~Day6를 통해 mobile-like scene에서는 단순 keyword baseline이 reference object, visibility, distance, reachability를 처리하지 못한다는 것을 확인했다.