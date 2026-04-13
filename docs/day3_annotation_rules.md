# Day 3 Annotation Rules

## 목표
3일차의 목표는 장면 이미지 안의 객체들을 candidate object로 정리하고,
instruction이 가리키는 정답 target object를 instance-level로 고정하는 것이다.

## 핵심 개념

    ### candidate object
    candidate object는 장면 안에 존재하는 객체 후보 하나를 의미한다.

    각 candidate object는 아래 정보를 가진다.

    - obj_id: 객체 고유 이름
    - category: 객체 종류
    - color: 객체 색상
    - bbox: 이미지 안 위치
    - visibility: 잘 보이는지 여부
    - notes: 보조 관계 설명

    ### grounding label
    grounding label은 instruction이 실제로 가리키는 정답 객체이다.

    예:
    instruction: "책 왼쪽의 파란 컵을 집어"
    grounding label: cup_blue_left_01

## obj_id 규칙
obj_id는 사람이 봐도 어느 객체인지 알 수 있게 짓는다.

형식 예시:
- cup_blue_left_01
- bottle_back_01
- spoon_on_plate_01

규칙:
1. category를 먼저 쓴다
2. 주요 속성(color, position)을 붙인다
3. 마지막에 번호를 붙인다

## bbox 규칙
bbox는 [x_min, y_min, x_max, y_max] 형식을 사용한다.

주의:
- 완벽한 detection 품질은 필요 없다
- 대략 객체를 감싸면 된다
- 지금은 grounding 실습이 목적이다

## visibility 규칙
visibility는 아래 셋 중 하나만 사용한다.

- clear: 잘 보임
- partial: 일부 가려짐
- hard: 많이 가려져서 판단이 어려움

## notes 규칙
notes는 공간 관계나 사람이 이해하기 좋은 설명을 짧게 적는다.

예:
- left_of_book
- behind_plate
- on_plate
- center

## ground truth 규칙
각 scene마다 아래 정답을 정한다.

    - gt_target_obj_id
    - gt_target_bbox
    - gt_subgoal_label
    - gt_should_abstain

## subgoal 라벨 규칙

    ### PREPARE_PICK
    target이 충분히 명확하고 다음 단계가 집기 준비로 이어질 수 있는 상태

    ### REFINE_VIEW
    target 후보는 있지만 장면 ambiguity, 가림, 관계 애매함 때문에 한 번 더 확인이 필요한 상태

    ### ABSTAIN_DECISION
    현재 정보만으로 target 선택이나 decision을 신뢰하기 어려워 보류해야 하는 상태

## abstain 판단 예시

    ### 예시 1
    instruction: "파란 컵을 집어"
    scene: 파란 컵이 2개 있고 둘 다 비슷하게 보임
    가능 판단: REFINE_VIEW 또는 ABSTAIN_DECISION

    ### 예시 2
    instruction: "책 왼쪽의 노란 컵을 집어"
    scene: 노란 컵이 없음
    판단: ABSTAIN_DECISION

    ### 예시 3
    instruction: "접시 위의 숟가락을 선택해"
    scene: 숟가락이 접시 위에 또렷하게 보임
    판단: PREPARE_PICK