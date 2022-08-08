import numpy as np
import random
from environment import Env
from collections import defaultdict
import serial



ser = serial.Serial('COM8', 9600)

def Decode(A): #아두이노에서 보내는 값을 파이썬으로 읽어오는 함수
    A = A.decode()
    A = str(A)
    Ard1=int(A[0:1])
    Ard2=int(A[1:2])
    Ard3=int(A[2:5])
    Ard4=int(A[5:6])
    Ard5=int(A[6:7])
    Ard6=int(A[7:8])
    return Ard1,Ard2,Ard3,Ard4,Ard5,Ard6


def Ardread():# return list [Ard1,Ard2]
        if ser.readable():
            LINE = ser.readline()
            code=Decode(LINE) 
            #print(code)
            return code
        else : 
            print("읽기 실패 from _Ardread_")


class QLearningAgent:
    def __init__(self, actions):
        self.actions = actions
        self.step_size = 0.6
        self.discount_factor = 0.9
        self.epsilon = 0.9
        
        
        self.q_table = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])

    # <s, a, r, s'> 샘플로부터 큐함수 업데이트
    def learn(self, state, action, reward, next_state):
        state, next_state = str(state), str(next_state)
        q_1 = self.q_table[state][action]
        # 벨만 최적 방정식을 사용한 큐함수의 업데이트
        q_2 = reward + self.discount_factor * max(self.q_table[next_state])
        
        self.q_table[state][action] += self.step_size * (q_2 - q_1)

    # 큐함수에 의거하여 입실론 탐욕 정책에 따라서 행동을 반환
    def get_action(self, state):
        state = str(state)
        if np.random.rand() < self.epsilon and min(self.q_table[state]) > -70 :
            # 무작위 행동 반환
            action = np.random.choice(self.actions)
            #self.epsilon -= 0.005 # 학습을 진행함에 따라 엡실론의 값을 감소 - > 최적 큐함수를 찾았다 하더라도 엡실론의 확률로 계속 탐험하는 한계 해결 - 정답은 아님
        else:
            # 큐함수에 따른 행동 반환
            state = str(state)
            q_list = self.q_table[state]
            action = arg_max(q_list)
            
        return action
    
    def check_direction(self, state): #가치함수 값이 가장 큰 액션 값(방향)을 구함
        state = str(state)
        q_list = self.q_table[state]
        checkdirect = np.argwhere(q_list == np.amax(q_list))
        return checkdirect
    
    def check_hunnit(self, state): #가치함수 값이 가장 큰 액션 값(방향)을 구함
        state = str(state)
        checkend = max(self.q_table[state])
        return checkend
    


# 큐함수의 값에 따라 최적의 행동을 반환
def arg_max(q_list):
    max_idx_list = np.argwhere(q_list == np.amax(q_list))
    max_idx_list = max_idx_list.flatten().tolist()
    return random.choice(max_idx_list)

def arg_min(q_list):
    min_idx_list = np.argwhere(q_list == np.amin(q_list))
    min_idx_list = min_idx_list.flatten().tolist()
    return random.choice(min_idx_list)


if __name__ == "__main__":

    
    env = Env()
    agent = QLearningAgent(actions=list(range(env.n_actions)))
    i=0
    redsign = 1
    packet = Ardread()
    #print(packet)
    emer = packet[0]
    way = packet[1]
    speed = packet[2]
    carnum = packet[3]
    xposition = packet[4]
    yposition = packet[5]
    print("수신받은 패킷 정보")
    print("----------------")
    if emer==1:
        print("응급여부 : no")
    elif emer==2 :
        print("응급여부 : yes")
    print("방향 : ", way)
    print("속도 : ", speed)
    print("차량 대수 : ", carnum)
    print("x좌표(위도) : ", xposition)
    print("y좌표(경도) : ", yposition)
    #if redsign == 1:
    checkreset = env.reset()
        
        
        
        #print("receive the packet")
    #while(i<100):
    for episode in range(1000):
        state = env.reset()
        
        while True: 
    
            if i==100 :# state의 큐테이블 최대값이 100이 되는 시점에서 시작점으로 돌아가서 큐테이블 중 최대값의 방향을 기준으로 신호제어
                state = [1,1] # 시작지점으로 돌아가기
                ckdirect = agent.check_direction(state)
                print(ckdirect)
                

                if state == [1,1]:
                    if ckdirect == [0]:
                        #print("change the signal to up")
                        if redsign == 1 and emer == 2:
                            ser.write(b'U')
                        else:
                            ser.write(b'H')
                        
                    elif ckdirect == [1]:
                        #print("change the signal to down")
                        if redsign == 1 and emer == 2:
                            ser.write(b'D')
                         
                        else:
                            ser.write(b'H')
                            ser.write(b'L')
                    
                    elif ckdirect == [2]:
                        #print("change the signal to left")
                        if redsign == 1 and emer == 2:
                            ser.write(b'L')
                        else:
                            ser.write(b'H')
                            
                            ser.write(b'L')
                        
                    elif ckdirect == [3]:
                        #print("change the signal to right")
                        if redsign == 1 and emer == 2:
                            ser.write(b'R')
                        else:
                            ser.write(b'H')
                            ser.write(b'L')
                    
                    else:
                        print("fail")

       
                i = 101
                
            
            elif(i==101):
                break
            
            else :
                # 게임 환경과 상태를 초기화
                env.render()
                # 현재 상태에 대한 행동 선택
                action = agent.get_action(state)
                # 행동을 취한 후 다음 상태, 보상 에피소드의 종료여부를 받아옴
                next_state, reward, done = env.step(action)
                # <s,a,r,s'>로 큐함수를 업데이트
                agent.learn(state, action, reward, next_state)

                state = next_state
            
                # 모든 큐함수를 화면에 표시
                env.print_value_all(agent.q_table)
                check_action = action

                i = agent.check_hunnit(state)# 현재 state의 큐테이블 리스트에서 최대값을 갱신
            
                if done:
                    break        
                
