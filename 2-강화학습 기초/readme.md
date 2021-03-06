# 2장 강화학습 기초 1
: MDP와 벨만 방정식
* 강화학습이 어떤 방정식을 풀어내는 방법이라면 그 방정식이 무엇인지 아는 것이 중요할 것이다...! 그 방정식은 바로 **벨만 방정식**이다.
* 순차적 행동 결정 문제는 **MDP로 정의 가능**...(1장에서 말했던 것처럼)/순차적 행동 결정 문제의 간단 예시 **그리드월드**를 통해 MDP 알아보기..!
* MDP를 통해 정의된 문제에서 에이전트가 학습하기 위해 **가치함수** 개념 도입...! 근데 가치함수가 벨만 방정식과 연결이 된다..!
* * *

## MDP
: MDP의 구성요소 => 상태, 행동, 보상함수, 상태 변환 확률, 할인율
* MDP의 이해를 돕기 위해 그리드월드(Grid World) 예제 사용
* 그리드 월드: 격자로 이뤄진 환경에서 문제를 푸는 각종 예제
* * *

### 상태
**에이전트가 관찰 가능한 상태의 집합: S**
* (상태라는 말이 모호할 수 있는데) "자신의 상황에 대한 관찰" == 상태
* 그리드 월드에서 상태의 개수는 유한
* 그리드 월드에서 상태는 격자 상의 각 위치(좌표)
* 그리드 월드에 상태가 5개 있을 경우, 수식으로 표현하면 
* ![image](https://user-images.githubusercontent.com/48302257/178220002-fd951711-0b89-4215-abe5-62a8952590a5.png)
* 에이전트는 시간에 따라 상태 집합 안에 있는 상태를 탐험한다. 이 때 시간을 t, 시간 t일 때의 상태를 St라고 표현한다.
* 예를 들어, 시간이 t일 때 상태가 (1, 3)이라면 St=(1, 3)
* 어떤 t에서의 상태 St는 정해진 것이 아니다. 때에 따라 t=1 일 때, St=(1, 3)일 수도 있고 St=(4, 2)일 수도 있다. 
![image](https://user-images.githubusercontent.com/48302257/178625124-40709fdc-0892-40c3-b99b-640a35dace91.png)


**"상태 = 확률 변수(Random Variable)"**

**St = s => "시간 t에서의 상태 St가 어떤 상태s다."**
* * *

### 행동
**에이전트가 상태 St에서 할 수 있는 가능한 행동의 집합 : A**
* 보통 에이전트가 할 수 있는 행동은 모든 상태에서 같다. At = a
* "시간 t에 에이전트가 특정한 행동 a를 했다."
* t라는 시간에 에이전트가 어떤 행동을 할 지는 정해져 있지 않으므로 At처럼 대문자로 표현한다.
* 그리드 월드에서 에이전트가 할 수 있는 행동은 A = {up, down, left, right}
* 만약 시간 t에서 상태가 (1, 3)이고 At=right 이라면 다음 시간의 상태는 (2, 3)이 된다.
* **만약 예상치 못한 요소가 있다면 에이전트가 특정 행동을 했을 때 어디로 이동할지 결정하는 것이 '상태 변환 확률'이다.**
* * *

### 보상함수
**에이전트가 학습할 수 있는 유일한 정보: R**
* 시간 t에서 상태가 St = s 이고, 행동이 At = a 일 때 에이전트가 받는 보상은 아래와 같은 수식으로 표현한다.
![image](https://user-images.githubusercontent.com/48302257/178626664-4d4ec745-2ee2-4161-8fa7-b1561bebe5b5.png)
* **기댓값**: 일종의 평균이며 어떤 정확한 값이 아니라 **나오게 될 숫자에 대한 예상**
* **보상 또한 기댓값**이어서 **상태 s에서 행동 a를 했을 경우**에 받을 것이라 예상되는 숫자이다.
* **Why 기댓값??**
* => **환경에 따라서** 같은 상태에서 같은 행동을 취하더라도 **다른 보상**을 줄 수도 있으므로 **보상함수는 기댓값으로 표현**한다.

또한 보상함수에서 중요한 것은 시점!!

* 에이전트가 어떤 상태에서 행동한 시간: **t**
* 보상을 받는 시간: **t+1**
* 이유: 보상을 에이전트가 t시점에서 이미 알고 있는 것이 아니고, 행동을 한 후에 환경이 알려주는 것이기 때문이다. 에이전트는 환경으로부터 **하나의 시간 단위가 지난 다음에 보상을 받으며,** 이 단위를 **타임스텝**이라고 한다.

![image](https://user-images.githubusercontent.com/48302257/178627845-1822d133-7adc-4993-9787-756b226ee078.png)

* * *

### 상태 변환 확률
* 에이전트가 행동을 취한다고 해서 모두 상태가 행동에 따라 그대로 변하는 것은 아님.
* 에이전트가 상태 s에서 어떤 행동 a를 했을 때, 도달하는 다음 타임스텝의 상태를 s'라고 한다면 s'는 상태 s에서 a를 했을 때 도달할 수 있는 다음 상태를 의미한다.
* 하지만 에이전트는 s`에 도달하지 못 할 수도 있고, 앞으로 가는 행동 a를 취할 때, 바람이 불 수도 있고 넘어질 수도 있다. 이처럼 상태의 변화에는 확률적인 요인이 들어간다.

![image](https://user-images.githubusercontent.com/48302257/178633342-80b2d951-8c7f-42ea-9d6a-cd1543a16992.png)

(P는 확률을 의미, 상태가 St=s이고 그 상태에서의 행동이 At=a일 때(조건문 |로 표현), 다음 시점 t+1에서 상태 s`에 도달할 확률)

* 이 값 역시 에이전트가 알지 못 하는 값으로서 '환경'의 일부
* 상태변환확률은 환경의 모델이라고도 한다.
* * *

### 할인율
* 에이전트는 항상 현재에 판단을 내리기 때문에 현재에 가까운 보상일수록 더 큰 가치를 가지게 정의해야한다.
* 같은 보상이면 **나중에 받을수록 가치가 줄어든다**는 것을 수학적으로 표현하기 위해 **할인율** 도입
* **할인**: 미래의 가치를 현재의 가치로 환산하는 것
* **할인율**: 시간에 따라 할인하는 비율
* 할인율은 γ로 표기하며, 0과 1 사이의 값이다.
* 시간 t로부터 k 시간이 지난 후에 보상 Rt+k 을 받는다고 하면, 현재로부터 시간이 k만큼 지났기 때문에 미래에 받을 **보상Rt+k은 γk-1만큼 할인된다.**

![image](https://user-images.githubusercontent.com/48302257/178633562-f9430e88-fab0-4220-8886-ae9e9eb1cdf6.png)
* * *

### 정책
* 정책은 **모든 상태에서 에이전트가 할 행동**을 말한다.
* 상태가 입력으로 들어오면 행동을 출력으로 내보내는 일종의 함수라고 생각해도 좋음
* 정책은 **π**로 표기한다.

![image](https://user-images.githubusercontent.com/48302257/178633703-de5cc445-a2bd-431e-8054-37a8f8dce562.png)

(시간 t에 에이전트가 상태 s에 있을 때 가능한 모든 행동 중에 a를 할 확률)
* 정책은 각 상태마다 어떤 행동을 할지 알려주며, 에이전트는 학습해 나가며 수많은 정책 중에서 최적 정책을 학습한다.
* 강화학습 문제를 통해 알고 싶은 것은 그냥 정책이 아니라 **최적정책**이다.
* 최적정책은 하나의 상태s에서 하나의 행동a만을 선택
* * *

=> 이처럼 **MDP**를 통해 **순차적 행동 결정 문제**를 정의했다. 

1) 에이전트가 현재 상태에서 앞으로 받을 보상들을 고려해서 행동을 결정한다. 

2) 그러면 환경은 에이전트에게 실제 보상과 다음 상태를 알려준다.

3) 이 과정을 반복하면서 에이전트는 어떤 상태에서 앞으로 받을 것이라 예상했던 보상에 대해 틀렸다는 것을 알게 된다.

4) 그러한 과정에서 에이전트는 실제로 받은 보상을 토대로 가치함수와 정책을 바꿔나간다. 

5) 학습과정을 충분히 반복한다면 가장 많은 보상을 받게 하는 정책을 학습할 수 있다.

* 앞으로 받을 것이라 예상했던 보상 = **가치함수(Value Function)**
* * *

## 가치함수
우리가 지금까지 한 일: 문제를 MDP로 정의

=> 에이전트는 MDP를 통해 최적 정책을 찾으면 된다.

**하지만 에이전트는 어떻게 최적 정책을 찾을 수 있을까?**

### 가치함수
에이전트 입장에서 어떤 행동을 하는 것이 좋은지를 어떻게 알 수 있을까??

=> 현재 상태에서 앞으로 받을 보상을 고려해서 선택해야 좋은 선택!

하지만 아직 받지 않은 보상들을 어떻게 고려할 수 있을까?

=> 에이전트는 **가치함수**를 통해 행동을 선택할 수 있다.

현재 시간 t부터 에이전트가 행동을 하면서 받을 보상을 모두 더해보자.

![image](https://user-images.githubusercontent.com/48302257/178639184-847f0d5a-2f19-4107-8718-1ee12c77bf87.png)

하지만 이 수식에는 3가지 문제가 있다.

![image](https://user-images.githubusercontent.com/48302257/178639284-e3b57a52-a1c3-4bef-b0f7-75f8617f09f6.png)

1. 현재에 받은 보상 100과 미래에 받는 보상 100을 똑같이 취급한다.

2. 보상 100을 1번 받을 때와 보상 20을 5번 받을 때를 구분하지 못 한다.

3. 시간이 무한대라면 0.1을 받아도, 1을 받아도 합이 무한대다.

**단순한 보상의 합으로는 판단을 내리기 어려우므로, 좀 더 정확한 판단을 위해 할인율(감가율)을 고려한다.** (할인율은 미래의 보상을 현재의 보상으로 변환하기 위해 미래에 받을 보상에 곱해주는 0과 1 사이의 값을 의미함.)
![image](https://user-images.githubusercontent.com/48302257/178639810-e4aeeaa5-f18b-49de-bbea-417015ced105.png)

이 값을 반환값(Return) Gt 이라고 한다. 
![image](https://user-images.githubusercontent.com/48302257/178644679-180891ee-fef0-47f7-9911-4de82c6695bf.png)
에이전트는 에피소드가 끝난 후에야 반환값을 알 수 있다.

하지만 에피소드가 끝날 때까지 기다려야 할까?

때로는 정확한 값을 얻기 위해 끝까지 기다리는 것보다 정확하지 않더라도 현재의 정보를 토대로 행동하는 것이 나을 때가 있다.

=> 가치함수 = 어떠한 상태에 가면 받을 것이라고 예상되는 값

![image](https://user-images.githubusercontent.com/48302257/178646660-4719c756-f13f-404d-bcc8-0e4e912f1ed6.png)

여기까지는 가치함수를 정의할 때 정책을 고려하지 않음

하지만 **정책을 고려하지 않으면 안 된다..!!**
* 상태에서 상태로 넘어갈 때 에이전트는 무조건 행동을 해야하고 각 상태에서 행동을 하는 것이 에이전트의 정책이기 때문
* 정책에 따라서 계산하는 가치함수는 당연히 달라질 수 밖에 없음
* **MDP에서의 가치함수는 항상 정책을 고려**

**벨만 기대 방정식(Bellman Expectation Equation)**
![image](https://user-images.githubusercontent.com/48302257/178647145-cad73b27-3d5b-4fd0-a141-401a2779c01a.png)

* 현재 상태의 가치함수와 다음 상태의 가치함수 사이의 관계를 말해주는 방정식
* 강화학습은 벨만 방정식을 어떻게 풀어나가느냐의 스토리
* * *

### 큐함수
가치함수는 말 그대로 "함수" => 입력/출력이 무엇인지 알아야 한다.

"상태"(입력) => "가치함수" => "받을 보상의 합"(출력) 

* 지금까지 설명한 가치함수는 **상태 가치함수**
* 에이전트는 가치함수를 통해 다음에 어떤 상태로 가야할 지 판단할 수 있다.
* 어떤 상태로 가면 좋을지 판단한 후에 그 상태로 가기 위한 행동을 따져볼 것이다.

**하지만....**

* **어떤 상태에서 각 행동에 대해 따로 가치함수를 만들어서 그 정보를 얻어올 수 있다면 에이전트는 굳이 다음 상태의 가치함수를 따져보지 않아도 어떤 행동을 해야할지 선택할 수 있다.**
* 이처럼 어떤 상태에서 어떤 행동이 얼마나 좋은지 알려주는 함수를 **행동 가치함수**라고 한다. 

-> **큐함수(Q Function)!**

큐함수는 상태, 행동이라는 두 가지 변수를 가지며 qπ(s, a)라고 나타낸다.

1. 각 행동을 했을 때 앞으로 받을 보상인 큐함수 qπ(s, a)를 π(a|s)에 곱한다.
2. 모든 행동에 대해 큐함수와 정책을 곱한 값을 더하면 가치함수가 된다.

** 큐함수는 강화학습에서 중요한 역할을 한다.**
* **강화학습에서 에이전트가 행동을 선택하는 기준**으로 가치함수보다는 보통 **큐함수를 사용**한다.
* * *
정리)
에이전트가 어떤 정책이 더 좋을 정책인지 판단하는 기준 => 가치함수

가치함수: 현재 상태로부터 정책을 따라갔을 때 받을 것이라 예상되는 보상의 합

보통 가치함수보다는 에이전트가 선택할 각 행동의 가치를 직접적으로 나타내는 큐함수 사용
* * *

## 벨만 방정식
### 벨만 기대 방정식
![image](https://user-images.githubusercontent.com/48302257/178653165-706accb7-1a95-4a39-a31c-dbb61ee0a01b.png)

위 함수는 현재 가치함수 값을 갱신한다.

하지만 갱신하려면 기댓값을 계산해야 하는데 어떻게 계산할까?

* 기댓값에는 어떤 행동을 할 확률(정책 π(a|s))과 그 행동을 했을 때 어떤 상태로 가게 되는 확률(상태 변환 확률)이 포함되어 있다.
* 따라서 정책과 상태 변환 확률을 포함해서 계산하면 된다.

![image](https://user-images.githubusercontent.com/48302257/178655099-893a2146-8c4b-429b-97f7-347023a76000.png)

상태 변환 확률이 모든 s와 a에 대해 1이라고 가정하자. 그리고 다음 예제를 한 번 생각해보자.
* 행동은 "상, 하, 좌, 우" 4가지
* 에이전트의 초기 정책은 무작위로 각 행동의 선택 확률은 25%
* 현재 에이전트 상태에 저장된 가치함수는 0
  * 왼쪽 상태의 가치함수 1, 밑쪽 상태의 가치함수 0.5
  * 위쪽 상태의 가치함수 0, 오른쪽 상태의 가치함수 0
* 감가율 0.9
* 오른쪽으로 행동을 취할 경우 노란색 별로 표현된 1의 보상을 받음

![image](https://user-images.githubusercontent.com/48302257/178653642-20ec9b59-b722-4ef6-bd69-829eccf8ed8e.png)

* 행동  = 상 : 0.25 x (0 + 0.9 x 0) = 0 
* 행동  = 하 : 0.25 x (0 + 0.9 x 0.5) = 0.1125 
* 행동  = 좌 : 0.25 x (0 + 0.9 x 1) = 0.225 
* 행동  = 우 : 0.25 x (1 + 0.9 x 0) = 0.25 
* 기댓값 = 0 + 0.1125 + 0.225 + 0.25 = 0.5875
* * *

### 벨만 최적 방정식
벨만 기대 방정식을 통해 계속 계산을 진행하다 보면 언젠가 식의 왼쪽 항과 오른쪽 항이 동일해지는 순간이 온다.

=>** vπ(s) 값이 수렴** => 현재 정책 π에 대한 참 가치함수를 구한 것

**하지만 참 가치함수와 최적 가치 함수는 다르다.**
* **참 가치함수**는 **"어떤 정책"을 따라서 움직였을 경우에 받게 되는 보상에 대한 참값**
* 가치함수의 정의가 "현재로부터 미래까지 받을 보상의 총합" 인데 이 값이 얼마가 될지에 대한 값
* 하지만 **최적의 가치함수**는 **수많은 정책 중에서 가장 높은 보상을 주는 가치함수**다. 

강화학습은 MDP로 정의 되는 문제에서 최적 정책을 찾는다.

더 좋은 정책은 무엇일까? 어떤 정책이 더 좋은 정책일까?

=> 가치함수(받을 보상들의 합)를 통해 판단할 수 있다.

모든 정책에 대해 가장 큰 가치함수를 주는 정책이 최적 정책

=> 최적 정책을 따라갔을 때 받을 보상의 합이 최적 가치함수

![image](https://user-images.githubusercontent.com/48302257/178656057-2e97a46b-0af4-485c-9d98-3f27e90409b8.png)

최적 정책은 각 상태 s에서의 최적의 큐함수 중에서 가장 큰 큐함수를 가진 행동을 하는 것

=> 선택 상황에서 판단 기준은 큐함수이며, 최적 정책은 언제나 이 큐함수 중에서 가장 높은 행동을 하나 하는 것

**벨만 최적 방정식(Bellman Optimality Equation)**

![image](https://user-images.githubusercontent.com/48302257/178656660-5c7ad9ea-208d-4c17-a3a8-f5c107c5c5ab.png)
* * *
정리)
현재 상태의 가치함수와 다음 상태 가치함수의 관계식 = 벨만 방정식

**벨만 기대 방정식** = 특정 정책을 따라갔을 때 가치함수 사이의 관계식

**벨만 최적 방정식*8 = 최적의 가치함수를 받게하는 정책(최적정책), 그 때 가치함수 사이의 관계식 
* * *
