"""
Ultimatum Game in complex network Visualization 
@date: 2020.5.9
@author: Tingyu Mo
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
# from img_concat import image_compose



def avg_pq_viz(data_path):
    '''
    Figure 2 like
    '''
    data = pd.read_excel(data_path)
    u = 0.001
    w = 0.1
    info = 'RG_Share_0.1~1'
    save_path = "./{}_u_{}_w_{}.jpg".format(info,u,w)
    x_label = [0.1,0.3,0.7,1]
    x_axis = np.log10(x_label)
    p_axis = list(data['p'])
    q_axis = list(data['q'])

    plt.figure()
    # plt.rcParams['font.family'] = ['sans-serif']
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.title(" {} u={} w={}".format(info,u,w))
    plt.xlabel("Selection strength(w)")#x轴p上的名字
    plt.ylabel("Mean")#y轴上的名字
    plt.xticks(x_axis,x_label,fontsize=16)
    plt.plot(x_axis, p_axis,marker='^',linestyle='-',color='skyblue', label='Offer (p)')
    plt.plot(x_axis, q_axis, marker='s',linestyle='-',color='red', label='Demand (q)')
    # plt.plot(x_axis, thresholds, color='blue', label='threshold')
    plt.legend(loc = 'upper right') # 显示图例
    plt.savefig(save_path)
    print("Figure has been saved to: ",save_path)
    plt.show()

def transition_viz(data_path):
    data = pd.read_excel(data_path)
    u_ = [0.001,0.01,0.1]
    # w = [0.01,0.1,1,10]

    info = 'RG_Transition'

    x_label = ["0.5/1","0.5","1"]
    x_axis = [1,2,3]
    # x_axis = np.log10(x_label)

    pt_axis = list(data['pt'])
    qt_axis = list(data['qt'])
    p_0_5_axis = list(data['p_0.5'])
    q_0_5_axis = list(data['q_0.5'])
    p_1_axis = list(data['p_1'])
    q_1_axis = list(data['q_1'])
    y_p_list = []
    y_q_list = []
    # y_p_list_sub = []
    # y_q_list_sub = []
    for i in range(0,len(pt_axis)):
    	# print(i)
    	y_p_list_sub = []
    	y_p_list_sub.append(pt_axis[i])
    	y_p_list_sub.append(p_0_5_axis[i])
    	y_p_list_sub.append(p_1_axis[i])
    	y_q_list_sub = []
    	y_q_list_sub.append(qt_axis[i])
    	y_q_list_sub.append(q_0_5_axis[i])
    	y_q_list_sub.append(q_1_axis[i])
    	# if (i+1) % 4 == 0 :
    	y_p_list.append(y_p_list_sub)
    	y_q_list.append(y_q_list_sub)
    		# y_p_list_sub.clear()
    		# y_q_list_sub.clear()
    plt.figure()
    i = 0	
    for _,u in enumerate(u_):
	    plt.clf()
	    save_path = "./{}_u_{}_offer.jpg".format(info,u)
	    # plt.rcParams['font.family'] = ['sans-serif']
	    # plt.rcParams['font.sans-serif'] = ['SimHei']
	    # plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
	    plt.title(" Offer(p) {} u={} ".format(info,u))
	    plt.xlabel("Transition Mode")#x轴p上的名字
	    plt.ylabel("Mean")#y轴上的名字
	    plt.xticks(x_axis,x_label,fontsize=16)
	    # plt.plot(x_axis, p_axis,marker='^',linestyle='-',color='skyblue', label='Offer (p)')
	    # plt.plot(x_axis, q_axis, marker='s',linestyle='-',color='red', label='Demand (q)')
	    # plt.plot(x_axis, y_list[0] ,marker='>',linestyle='-',color='purple', label='w = 0.001')
	    plt.plot(x_axis, y_p_list[i] ,marker='^',linestyle='-',color='skyblue', label='WS = 0.01')
	    plt.plot(x_axis, y_p_list[i+1], marker='s',linestyle='-',color='green', label='WS = 0.1')
	    plt.plot(x_axis, y_p_list[i+2], marker='*',linestyle='-',color='red', label='WS = 1')
	    plt.plot(x_axis, y_p_list[i+3], marker='+',linestyle='-',color='black', label='WS = 10')	    # plt.plot(x_axis, thresholds, color='blue', label='threshold')
	    plt.legend(loc = 'upper right') # 显示图例
	    plt.savefig(save_path)
	    print("Figure has been saved to: ",save_path)
	    plt.clf()
	    # plt.show()

	    
	    save_path = "./{}_u_{}_demond.jpg".format(info,u)
	    # plt.rcParams['font.family'] = ['sans-serif']
	    # plt.rcParams['font.sans-serif'] = ['SimHei']
	    # plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
	    plt.title(" Demand(q) {} u={}".format(info,u))
	    plt.xlabel("Transition Mode")#x轴p上的名字
	    plt.ylabel("Mean")#y轴上的名字
	    plt.xticks(x_axis,x_label,fontsize=16)
	    # plt.plot(x_axis, p_axis,marker='^',linestyle='-',color='skyblue', label='Offer (p)')
	    # plt.plot(x_axis, q_axis, marker='s',linestyle='-',color='red', label='Demand (q)')
        # plt.plot(x_axis, y_list[0] ,marker='>',linestyle='-',color='purple', label='w = 0.001')
	    plt.plot(x_axis, y_q_list[i] ,marker='^',linestyle='-',color='skyblue', label='WS = 0.01')
	    plt.plot(x_axis, y_q_list[i+1], marker='s',linestyle='-',color='green', label='WS = 0.1')
	    plt.plot(x_axis, y_q_list[i+2], marker='*',linestyle='-',color='red', label='WS = 1')
	    plt.plot(x_axis, y_q_list[i+3], marker='+',linestyle='-',color='black', label='WS = 10')	
	    #plt.plot(x_axis, y_q_list[i+2], marker='*',linestyle='-',color='red', label='Share = 0.5')
        # plt.plot(x_axis, y_list[4], marker='x',linestyle='-',color='black', label='w = 10')
	    # plt.plot(x_axis, thresholds, color='blue', label='threshold')
	    plt.legend(loc = 'upper right') # 显示图例
	    plt.savefig(save_path)
	    print("Figure has been saved to: ",save_path)
	    # plt.show()
	    i = i+4


if __name__ == '__main__':

    # RecordName ='2020-03-03-09-14-20'   
    # time_option = "all"
    # pq_distribution_viz(RecordName,time_option)
    # avg_pq_viz()
    data_path ='./transition_excel.xlsx'
    avg_pq_viz(data_path)
    # image_compose("./result/Fig/")