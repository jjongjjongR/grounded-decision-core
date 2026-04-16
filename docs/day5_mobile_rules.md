# Day5 Mobile Manipulation Rules

## 목표
Day5의 목표는 mobile manipulation 전체를 구현하는 것이 아니라,
모바일 환경에서 target grounding / subgoal 판단이 왜 더 어려워지는지
scene 설계로 반영하는 것이다.

---

## fixed-base와 mobile setting 차이

fixed-base manipulation에서는 보통
- 작업 공간이 고정되어 있고
- target이 이미 작업 범위 안에 있으며
- 시야가 비교적 안정적이다.

반면 mobile manipulation에서는
- target이 처음부터 보이지 않을 수 있고
- 이동하면서 시야가 계속 바뀌고
- target이 보여도 팔이 닿지 않을 수 있으며
- navigation과 manipulation 판단이 서로 영향을 준다.

---

## Day5에서 추가하는 mobile-like difficulty

### 1. target not visible yet
현재 시야에는 target이 없지만, instruction상 target은 다른 위치에 있을 수 있다.

### 2. partial visibility from current view
현재 시점에서는 target이 일부만 보여 판단이 애매하다.

### 3. visible but not reachable
target은 보이지만 현재 base pose에서는 팔이 닿기 어렵다.

### 4. multiple similar targets across locations
서로 다른 위치에 비슷한 target들이 있어 ambiguity가 커진다.

### 5. navigation required before manipulation
조작 전에 먼저 위치 이동이나 시야 확보가 필요하다.

---

## Day5 라벨 철학

### PREPARE_PICK
현재 시야와 위치 기준으로 target이 명확하고 진행 가능

### REFINE_VIEW
target 후보는 있지만 현재 view / 위치 / ambiguity 때문에 한 번 더 확인 필요

### ABSTAIN_DECISION
현재 정보로는 진행하면 위험하거나 instruction과 현재 scene이 맞지 않음

---

## 핵심 원칙
Day5에서는 새로운 controller나 planner를 만들지 않는다.
기존 Day3/Day4 baseline을 그대로 사용하면서,
scene가 mobile setting일 때 왜 흔들리는지 확인한다.