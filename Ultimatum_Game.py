"""
A simple implementation of Ultimatum Game
@date: 2020.2.13
@author: Tingyu Mo
"""

import numpy as np
import pandas as pd
import os
import time

class Ultimatum_Game():
    def __init__(self,N,w,u,divided_part = 12+1,check_point = None):
        self.N = N
        self.w = w
        self.u = u
        # self.meta_element = np.around(np.arange(0,1,1/12),2) #1/12 equally divided
        self.meta_element=np.arange(divided_part)
        self.Frequency_matrix = np.zeros((divided_part,divided_part))
        
        if check_point == None:
            self.dir_str = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
            os.mkdir("./result/{}".format(self.dir_str))
        else:
            self.dir_str = check_point
        

    def Make_Player(self,N):
        '''
        generate random strategy vector(p,q) from uniform distribution,
        
        inwhich p is the proposer's offer 

        and q is the responder's minmum demand.
        '''
        # p_vector = np.random.rand(N)
        # q_vector = np.random.rand(N)
        meta_element = self.meta_element
        p_vector = np.random.choice(meta_element,size = N)
        q_vector = np.random.choice(meta_element,size = N)

        return p_vector, q_vector

    def Play(self,p_vector,q_vector):
        '''
        Each generation, every agent plays the UG with every other agent, 
        
        once in the proposer role and once in the responder role.
        '''
        pay_off_array = np.zeros((N,N)) #shape = (N,N-1)
        for P1 in range(self.N):
            for P2 in range(P1+1,self.N):
                if P1 != P2:
                    # proposer = P1 , responder = P2
                    offer = p_vector[P1]
                    demand = q_vector[P2]
                    if offer >= demand:
                        # acception
                        # 1-offer has be modifed as 12 - offer at 2020/2/9/15:17  
                        pay_off_array[P1][P2] += 12 - offer 
                        pay_off_array[P2][P1] += offer

                    # proposer = P2 , responder = P1
                    offer = p_vector[P2]
                    demand = q_vector[P1]
                    if offer >= demand:
                        # acception
                        pay_off_array[P2][P1] += 12 - offer 
                        pay_off_array[P1][P2] += offer   
                else:
                    continue
        #Probability is NaN at 2020/2/9/0:18, modifed "/12"            
        return pay_off_array/12

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
        birth,death = np.random.choice(a = individual_index,size = 2,p = effective_payoff)
        if np.random.rand(1) <= u:
            # Mutation occurs
            # p_vector[death],q_vector[death] = np.random.rand(2)
            p_vector[death] = np.random.choice(self.meta_element,size = 1)
            q_vector[death] = np.random.choice(self.meta_element,size = 1)
            # print("Mutation occurs!\n")
        else :
            # Reproduce occurs
            p_vector[death],q_vector[death] = p_vector[birth],q_vector[birth]

        return p_vector,q_vector
    
    def Frequency_calculate(self,p_vector,q_vector,Epochs):
        '''
        Frequency of each strategy pair (p,q) over the whole evolution
        '''
        for i in range(self.N):
                # self.Frequency_matrix[p][q] = ( 1.0*self.Frequency_matrix[p][q]*(Epochs-1)+1) / (Epochs)
                self.Frequency_matrix[p_vector[i]][q_vector[i]] +=1 

        return None
                


    
    def Save(self,pq_array,Epoch):
        '''
        save frequency matrix and strategy array
        '''
        subdir = "./result/{}/w{}_ep{}_u{}".format(self.dir_str,self.w,Epoch,self.u)
        os.mkdir(subdir)
        df = pd.DataFrame(data = pq_array)
        df.to_csv('./result/{}/w{}_ep{}_u{}/strategy_w{}_ep{}_u{}.csv'.format(self.dir_str,self.w,Epoch,self.u,self.w,Epoch,self.u),index = None)
        freq = pd.DataFrame(data = self.Frequency_matrix*1.0/(100*Epoch))
        freq.to_csv('./result/{}/w{}_ep{}_u{}/frequency_w{}_ep{}_u{}.csv'.format(self.dir_str,self.w,Epoch,self.u,self.w,Epoch,self.u),index = None)
        # df = pd.read_csv('./results.csv')
        # print(df)

    def train(self,p_vector,q_vector):
        '''
        evolution starts!
        '''
        for Epoch in range(1,Epochs):
            #各博弈方进行最后通牒博弈并计算各自的得益
                pay_off_array = self.Play(p_vector,q_vector)
                #计算各博弈方的平均得益和有效得益
                effective_payoff = self.Pay_off_calculate(pay_off_array,self.w)
                #演化过程
                p_vector,q_vector = self.Moran_process(p_vector,q_vector,effective_payoff,self.u)
                #计算频率
                self.Frequency_calculate(p_vector,q_vector,Epoch)
                if Epoch % 50000== 0:
                    print("Epoch[{}]".format(Epoch))
                    print("p_vector:\n{}\nq_vector:\n{}".format(p_vector,q_vector))
                    print("Frequency:\n{}\n".format(self.Frequency_matrix*1.0/(100*Epoch)))
                # if Epoch % 100000 == 0:
                    #保留一位有效数字
                    p_vector = np.around(p_vector,1)
                    q_vector = np.around(q_vector,1)
                    print("p_vector:\n{}\nq_vector:\n{}".format(p_vector,q_vector))
                    pq_array = np.vstack((p_vector,q_vector))
                    self.Save(pq_array,Epoch)

    def retrain(self,filepath):
        '''
        continue evolution from specific check point
        '''
        lists = os.listdir(filepath)         
        lists.sort(key=lambda fn: os.path.getmtime(filepath + "/" + fn)) 
        result_dir = os.path.join(filepath, lists[-1])      
        result_list = os.listdir(result_dir)
    
        parse_str = result_list[0][:-4].split("_")
        if parse_str[0] == 'strategy':
            strategy_path = os.path.join(result_dir,result_list[0])
            frequency_path = os.path.join(result_dir,result_list[1])
        else:
            strategy_path = os.path.join(result_dir,result_list[1])
            frequency_path = os.path.join(result_dir,result_list[0])
        w = float(parse_str[1][1:])
        Epoch = int(parse_str[2][2:])
        u = float(parse_str[3][1:])
        self.w = w
        self.u = u

        strategy = pd.read_csv(strategy_path)
        frequency = pd.read_csv(frequency_path)
        pd_array = strategy.values
        self.Frequency_matrix = (frequency.values)*(100*Epoch)
        p_vector,q_vector = pd_array[0],pd_array[1]
        
        return p_vector, q_vector,w,Epoch+1,u

    


    





if __name__ == '__main__':

    N = 100
    w = np.around(pow(10,-0.5),4)
    u = np.around(pow(10,-1.25),4) #u = 10^(-1.25)
    Epochs = pow(10,8) #演化轮次
    check_point = "./result/2020-02-11-10-46-10"
    # check_point = None
    #生成环境env
    if check_point!= None:
        UG = Ultimatum_Game(N,w,u,check_point = check_point)
        p_vector, q_vector,w,Start,u = UG.retrain(check_point)
    else:
        UG = Ultimatum_Game(N,w,u)
        Start = 1
        #创建N个博弈方
        p_vector, q_vector = UG.Make_Player(N)
        
    for Epoch in range(Start,Epochs):
    #各博弈方进行最后通牒博弈并计算各自的得益
        pay_off_array = UG.Play(p_vector,q_vector)
        #计算各博弈方的平均得益和有效得益
        effective_payoff = UG.Pay_off_calculate(pay_off_array,w)
        #演化过程
        p_vector,q_vector = UG.Moran_process(p_vector,q_vector,effective_payoff,u)
        #计算频率
        UG.Frequency_calculate(p_vector,q_vector,Epoch)
        if Epoch % 100000== 0:
            print("Epoch[{}]".format(Epoch))
            print("p_vector:\n{}\nq_vector:\n{}".format(p_vector,q_vector))
            print("Frequency:\n{}\n".format(UG.Frequency_matrix*1.0/(100*Epoch)))
        # if Epoch % 100000 == 0:
            #保留一位有效数字
            p_vector = np.around(p_vector,1)
            q_vector = np.around(q_vector,1)
            print("p_vector:\n{}\nq_vector:\n{}".format(p_vector,q_vector))
            pq_array = np.vstack((p_vector,q_vector))
            UG.Save(pq_array,Epoch)
    print("done!")