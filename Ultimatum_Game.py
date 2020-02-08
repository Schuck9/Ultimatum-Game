"""
A simple implementation of Ultimatum_Game
@date: 2020.2.8
@author: Tingyu Mo
"""

import numpy as np
import pandas as pd

class Ultimatum_Game():
    def __init__(self,population):
        self.N = population

    def Make_Player(self,N):
        '''
        generate random strategy vector(p,q) from uniform distribution,
        
        inwhich p is the proposer's offer 

        and q is the responder's minmum demand.
        '''
        p_vector = np.random.rand(N)
        q_vector = np.random.rand(N)
        
        return p_vector, q_vector

    def Play(self,p_vector,q_vector):
        '''
        Each generation, every agent plays the UG with every other agent, 
        
        once in the proposer role and once in the responder role.
        '''
        pay_off_array = np.zeros((N,N)) #shape = (N,N-1)
        for P1 in range(self.N):
            for P2 in range(P1,self.N):
                if P1 != P2:
                    # proposer = P1 , responder = P2
                    offer = p_vector[P1]
                    demand = q_vector[P2]
                    if offer > demand:
                        # acception
                        pay_off_array[P1][P2] += 1 - offer 
                        pay_off_array[P2][P1] += offer

                    # proposer = P2 , responder = P1
                    offer = p_vector[P2]
                    demand = q_vector[P1]
                    if offer > demand:
                        # acception
                        pay_off_array[P2][P1] += 1 - offer 
                        pay_off_array[P1][P2] += offer   
                else:
                    continue
                    
        return pay_off_array

    def Pay_off_calculate(self,pay_off,w):
        '''
        calculate average pay off of an individuals 
        
        and correspond effective pay off.
        '''
        avg_payoff = np.mean(pay_off,axis=1)# axis = 1,across row
        effective_payoff = np.exp(w*avg_payoff) # exp[w*πi]

        return effective_payoff

    def Moran_process(self,p_vector,q_vector,effective_payoff,u):
        '''
        Then one agent is picked proportional to exp[wπ] to reproduce, 

        where w is the intensity of selection; 

        and one agent is picked at random to die.
        '''
        individual_index = np.arange(self.N)
        effective_payoff = effective_payoff*1.0/np.sum(effective_payoff)
        birth,death = np.random.choice(individual_index,size = 2,p = effective_payoff)
        if np.random.rand(1) <= u:
            # Mutation occurs
            p_vector[death],q_vector[death] = np.random.rand(2)
            # print("Mutation occurs!\n")
        else :
            # Reproduce occurs
            p_vector[death],q_vector[death] = p_vector[birth],q_vector[birth]

        return p_vector,q_vector
    
    def Save(self,pq_array):
        df = pd.DataFrame(data = pq_array)
        df.to_csv('./results.csv',index = None)
        # df = pd.read_csv('./results.csv')
        # print(df)





if __name__ == '__main__':

    N = 100
    w = 1e-1
    u = pow(10,-1.25) #u = 10^(-1.25)
    Epochs = pow(10,2) #演化轮次
    #生成环境env
    UG = Ultimatum_Game(N)
    #创建N个博弈方
    p_vector, q_vector = UG.Make_Player(N)
    for Epoch in range(Epochs):
    #各博弈方进行最后通牒博弈并计算各自的得益
        pay_off_array = UG.Play(p_vector,q_vector)
        #计算各博弈方的平均得益和有效得益
        effective_payoff = UG.Pay_off_calculate(pay_off_array,w)
        #演化过程
        p_vector,q_vector = UG.Moran_process(p_vector,q_vector,effective_payoff,u)
        if Epoch % 50 == 0:
            print("Epoch[{}]".format(Epoch+1))
            print("p_vector:\n{}\nq_vector:\n{}".format(p_vector,q_vector))
    #保留一位有效数字
    p_vector = np.around(p_vector,1)
    q_vector = np.around(q_vector,1)
    print("p_vector:\n{}\nq_vector:\n{}".format(p_vector,q_vector))
    pq_array = np.vstack((p_vector,q_vector))
    UG.Save(pq_array)
    print("done!")