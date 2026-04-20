# Day7 Research Direction

## 관심 문제

나는 mobile manipulation을 위한 VLA에서, low-level control 자체보다 action 이전 단계의 grounding, subgoal reasoning, uncertainty-aware abstention에 관심이 있다.

---

## 현재 toy-project에서 확인한 것

작은 toy-project를 통해 다음을 확인했다.

1. target grounding은 단순 object detection보다 어렵다.
2. instruction 안에는 target object와 reference object가 함께 등장할 수 있다.
3. visibility가 낮은 target은 단순 baseline에서 쉽게 밀린다.
4. mobile-like scene에서는 거리, 깊이, reachability가 중요해진다.
5. 잘못된 판단을 높은 confidence로 진행하는 것은 위험하다.
6. 따라서 action 이전에 grounded decision의 신뢰성을 점검하는 layer가 필요하다.

---

## VLA와의 연결

VLA는 image와 language instruction을 받아 action을 출력한다.

하지만 action을 바로 출력하기 전에 다음 질문이 중요하다.

1. target이 정확히 grounding되었는가?
2. 현재 scene에서 action으로 넘어가도 되는가?
3. 더 확인해야 하는가?
4. 확신이 낮으면 abstain할 수 있는가?

따라서 이 toy-project는 full VLA 구현이 아니라, VLA의 action 이전 단계에 필요한 decision verification layer를 작게 만든 것이다.

---

## mobile manipulation과의 연결

mobile manipulation에서는 fixed-base manipulation보다 다음 문제가 더 중요하다.

1. target이 처음부터 보이지 않을 수 있다.
2. 시야가 이동에 따라 바뀐다.
3. target이 보여도 reachable하지 않을 수 있다.
4. reference object와 target object를 구분해야 한다.
5. 거리와 깊이 정보가 target grounding에 영향을 준다.

---

## 다음 연구 질문

1. target object와 reference object를 더 안정적으로 구분할 수 있는가?
2. visibility / distance / reachability를 consistency score에 반영할 수 있는가?
3. mobile-like scene에서 abstention policy를 더 잘 설계할 수 있는가?
4. VLA의 action output 이전에 grounded decision verification layer를 둘 수 있는가?
5. memory나 re-grounding이 들어가면 mobile manipulation에서 안정성이 좋아지는가?

---

## 컨택용 한 문장

저는 mobile manipulation을 위한 VLA에서, low-level control보다 action 이전 단계의 target grounding, subgoal reasoning, uncertainty-aware abstention이 신뢰성에 어떤 영향을 주는지에 관심이 있습니다.