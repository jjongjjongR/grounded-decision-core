## 프로젝트 한 줄 정의:
    정적인 이미지와 언어 지시를 기반으로 target object를 고르고 short-horizon decision subgoal을 선택한 뒤, 그 선택의 신뢰도가 낮으면 abstain하는 검증형 프로젝트

## 왜 이 프로젝트를 하는지: 
    모바일 매니퓰레이션 전체를 처음부터 end-to-end로 구현하려고 하면 문제 범위가 너무 커지고, 
    가장 먼저 이해하고 검증해야 하는 핵심이 흐려질 수 있다.

    그래서 이 프로젝트는 실제 로봇 제어보다 앞단에 있는 판단 구조에 집중한다.  
    구체적으로는, 언어 지시와 장면 이미지를 보고
    1. 지금 어떤 물체를 목표로 삼아야 하는지
    2. 지금 당장 어떤 짧은 단계의 판단 상태에 있는지
    3. 이 판단이 얼마나 믿을 만한지
    4. 확신이 낮을 때는 무리하게 진행하지 않고 보류할 수 있는지
    를 먼저 다룬다.

    즉, 이 프로젝트의 목적은 “잘 움직이는 로봇”을 바로 만드는 것이 아니라,  
    잘못된 target 선택과 잘못된 초기 판단을 줄일 수 있는 grounded decision 구조를 먼저 만드는 것이다.

## 포함 / 제외 범위
    - 포함
        - single RGB image
        - single natural language instruction
        - tabletop scene
        - discrete subgoal label prediction
        - consistency scoring
        - abstain
    - 제외
        - video / observation history
        - object detector end-to-end 학습
        - segmentation mask 예측
        - low-level control
        - trajectory planning
        - controller tuning
        - re-grounding / replanning / memory

## 최종 목표
    1. 이미지와 지시문을 보고 target object를 고를 수 있는가
    2. 그 상황에서 다음 short-horizon decision subgoal을 고를 수 있는가
    3. 선택이 instruction / scene과 얼마나 맞는지 consistency score로 표현할 수 있는가
    4. 확신이 낮을 때 abstain 해서 잘못된 결정을 줄일 수 있는가

## 평가하고 싶은 질문
    1. instruction을 보고 올바른 target object를 고를 수 있는가
    2. target은 맞더라도 현재 장면 상태에 맞는 subgoal을 고를 수 있는가
    3. ambiguity가 큰 상황에서 consistency score가 실제 불확실성을 반영하는가
    4. abstain을 넣었을 때 잘못된 진행을 실제로 줄일 수 있는가
    5. abstain을 너무 많이 해서 아무것도 못 하는 구조가 되지는 않는가
    6. clear scene과 ambiguous scene에서 성능 차이가 어떻게 나는가