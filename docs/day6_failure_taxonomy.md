# Day6 Failure Taxonomy

## 목표

Day6의 목표는 Day5 mobile-like scene에서 baseline이 왜 틀렸는지 유형별로 분석하는 것이다.

단순히 "틀렸다"가 아니라, 어떤 종류의 실패인지 분류한다.

---

## Failure Type 1. TARGET_MISMATCH

### 정의
예측한 target object가 ground truth target object와 다른 경우.

### 의미
모델이 instruction이 가리키는 실제 target을 잘못 골랐다는 뜻이다.

---

## Failure Type 2. SUBGOAL_MISMATCH

### 정의
예측한 subgoal label이 ground truth subgoal label과 다른 경우.

### 의미
target 선택 이후 다음 decision 상태를 잘못 판단했다는 뜻이다.

---

## Failure Type 3. MISSED_ABSTAIN

### 정의
정답은 abstain해야 하는 상황인데, 모델은 진행해도 된다고 판단한 경우.

### 의미
로봇 시스템에서는 위험한 실패다. 확신이 낮은 상황에서 행동을 강행할 수 있기 때문이다.

---

## Failure Type 4. WRONG_ABSTAIN

### 정의
정답은 진행 가능한 상황인데, 모델이 불필요하게 abstain한 경우.

### 의미
안전하지만 너무 보수적인 시스템이 될 수 있다.

---

## Failure Type 5. OVERCONFIDENT_WRONG_DECISION

### 정의
target을 틀리게 골랐는데도 consistency score가 높고 abstain하지 않은 경우.

### 의미
신뢰성 측면에서 가장 위험한 실패다. 틀린 결정을 높은 확신으로 진행하기 때문이다.

---

## Failure Type 6. VISIBILITY_BIAS

### 정의
정답 target은 partial 또는 hard visibility인데, 모델이 clear한 주변 물체를 선택한 경우.

### 의미
모바일 환경에서는 target이 멀거나 가려질 수 있다. 단순 baseline은 잘 보이는 물체를 과하게 선호할 수 있다.

---

## Failure Type 7. REFERENCE_OBJECT_CONFUSION

### 정의
"책장 옆의 병", "문 옆의 컵", "테이블 뒤의 숟가락"처럼 기준 물체와 target 물체가 함께 등장할 때, 기준 물체를 target으로 착각하는 실패.

### 의미
언어 지시의 구조를 이해하지 못한 실패다.

---

## Failure Type 8. DISTANCE_OR_DEPTH_MISUNDERSTANDING

### 정의
"복도 끝", "멀리 있는", "뒤쪽" 같은 위치/깊이 단서를 제대로 해석하지 못한 실패.

### 의미
mobile manipulation에서는 거리와 깊이 정보가 중요하다.

---

## Failure Type 9. REACHABILITY_BLINDNESS

### 정의
target이 보이더라도 현재 위치에서 실제로 조작 가능한지 판단하지 못하는 실패.

### 의미
mobile manipulation에서는 target visibility와 arm/base feasibility가 다르다.

---

## Day6 결론

Day6에서 중요한 것은 baseline 성능을 높이는 것이 아니라,
baseline이 왜 실패하는지 언어화하는 것이다.

이번 분석을 통해 mobile-like scene에서 다음 문제가 중요하다는 것을 확인했다.

1. target object와 reference object 구분
2. visibility에 따른 불확실성
3. distance/depth 이해
4. reachability 판단
5. overconfidence와 abstention