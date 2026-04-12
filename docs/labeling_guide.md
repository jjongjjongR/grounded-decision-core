## target object란 무엇인가
    target object는 현재 instruction이 가리키는 실제 장면 속 대상 물체다.

    예를 들어 instruction이 “책 왼쪽의 파란 컵을 집어”라면, 
    target object는 단순히 “컵”이 아니라 그 장면 안에서 '책 왼쪽에 있고 파란색인 컵' 하나여야 한다.

    즉, target object는 category 수준이 아니라 instance 수준으로 정해져야 한다.

## subgoal label 의미
    subgoal label은 지금 이 장면에서, 시스템이 어떤 짧은 판단 상태에 있는지를 나타내는 라벨이다.

    이 프로젝트에서 subgoal은 실제 모터 제어 명령이 아니라, 다음 decision 단계가 무엇이어야 하는지를 표현한다.
    즉, 바로 pick 준비를 해도 되는지, 장면을 더 확인해야 하는지, 아예 지금은 보류해야 하는지를 구분하는 역할이다.

## PREPARE_PICK
    instruction과 장면이 비교적 잘 맞고, target object가 충분히 보이며, 
    다음 단계가 “집기 준비”로 자연스럽게 이어질 수 있는 상태다.

    예:
    - target이 분명히 보인다
    - 같은 종류 물체가 있어도 instruction으로 충분히 구분된다
    - 가림이 심하지 않다

## REFINE_VIEW
    target 후보는 어느 정도 있지만,  
    가려짐, 복잡한 배경, 애매한 공간 관계 때문에 지금 바로 진행하기에는 추가 확인이 필요한 상태다.

    예:
    - 파란 컵이 두 개 있는데 책과의 관계가 애매하다
    - target이 일부 가려져 있다
    - instruction이 가리키는 관계가 image만으로 조금 헷갈린다

## ABSTAIN_DECISION
    현재 정보만으로는 target 선택이나 현재 decision을 신뢰하기 어렵기 때문에,  
    지금은 진행하지 않고 보류해야 하는 상태다.

    예:
    - target이 거의 보이지 않는다
    - instruction과 장면이 맞지 않는다
    - 지시문이 말하는 객체가 scene에 없거나 매우 불확실하다

## abstain이 필요한 경우 예시

### 예시 1
    instruction: “파란 컵을 집어”  
    scene: 컵이 두 개 있는데 둘 다 파란색이고, 하나는 절반 이상 가려져 있음  
    판단: REFINE_VIEW 또는 ABSTAIN_DECISION 가능

### 예시 2
    instruction: “책 왼쪽의 병을 잡아”  
    scene: 책은 보이지만 병이 전혀 보이지 않음  
    판단: ABSTAIN_DECISION

### 예시 3
    instruction: “접시 뒤의 빨간 컵을 집어”  
    scene: 빨간 컵이 보이긴 하지만 접시와의 관계가 애매하고 컵 일부가 가려짐  
    판단: REFINE_VIEW

### 예시 4
    instruction: “파란 컵을 집어”  
    scene: 파란 컵이 하나만 또렷하게 보이고 주변도 복잡하지 않음  
    판단: PREPARE_PICK