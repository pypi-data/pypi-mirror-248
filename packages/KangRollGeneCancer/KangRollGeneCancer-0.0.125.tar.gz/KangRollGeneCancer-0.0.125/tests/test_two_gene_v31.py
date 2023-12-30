# V 15 开始合理化了。 让H3 还是有记忆，并开始基础迭代。 
# 但这里应该多一个跟大的周期，如季节因素。 有可能季节，由于照射的阳光不养会，让人们得到不同的癌症情况。 这是基因行的因素，我们觉得是可以值得考虑的事情。 

# v 25: 做一个季节性的修复

import matplotlib.pyplot as plt
import numpy as np
import random
from sa005package.kangroll_basic_fn001_mln_com_release import fn010_translp, V3_simulate_MLN


import sys
# sys.path.insert(0, "/Users/kang/1.live_wit_GPT4/code_pypi/KangRollGeneCancerWorkspace/krgc001_env/lib/python3.8/site-packages")
sys.path.append('../')
sys.path.append('./')
sys.path.append('./tests/')


import csv

# 读取CSV文件并存储睡眠时间
sleep_hours_dict = {}
with open('./tests/boundary_data/boundary_sleep_time_per_day.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过标题行
    for row in reader:
        day, sleep_hours = int(row[0]), int(row[1])
        sleep_hours_dict[day] = sleep_hours


# 读取CSV文件并存储季节影响
seasonal_effect_dict = {}
with open('./tests/boundary_data/boundary_seasonal_effect_on_H3.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # 跳过标题行
    for row in reader:
        hour, is_summer, effect_on_H3_0, effect_on_H3_2 = int(row[0]), int(row[1]), float(row[2]), float(row[3])
        seasonal_effect_dict[hour] = (is_summer, effect_on_H3_0, effect_on_H3_2)


import numpy as np


def init_boundary_H3():
    # global Boundary_H3
    Boundary_H3 = np.array([1e-7, 0.6, 1e-3, 0]) #存储边界值    注意与H3_ini的比较。两处设定。 H3_ini = np.array([1e-10, 0.6, 5e-4, 0])
    return Boundary_H3





def apply_boundary_correction_advanced(H3_ini, delta_combined,Boundary_H3, weight=0.1):
        
    """
    根据不同的边界条件应用修正到和谐集合H3上。

    参数:
    H3_ini: 初始和谐集合H3的值
    delta_combined: 结合两基因的Delta值
    weight: 修正权重，默认为0.5

    返回:
    H3_after_correction: 修正后的和谐集合H3的值
    """

    # global Boundary_H3  # 使用全局变量 我觉得不需要。

    # ANSI 转义序列颜色代码
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'  # 重置颜色


    # 设置边界值

    # Boundary_H3 = np.array([1e-5, 1, 1e-5, 0])
    # delta_combined = np.array(delta_combined) # 确保delta_combined 是数组。这样才能与 float 类型的 weight 值，相乘。一个序列 (delta_combined) .

    # 检查边界条件并应用适当的修正
    if H3_ini[0] > 0.001 and H3_ini[2] < 1e-6:

        delta_ToSaveLife =np.array([0.1,1, 0.1, 0 ])
        # 应用边界修正
        print('--Before----!!!!-------!!!! Beyond Boundary the Life is dangreous !!!!-----!!!------Takc Care of your slelf ---and You need Help！！')
        print('H3_ini = ',H3_ini)
        print('Boundary_H3  = ',Boundary_H3 )
        print('delta_combined = ',delta_combined )
        print('weight  = ',weight )

        # 情况1: 变异超边界，修复超边界
        print(RED +"【DANGER!】情况1: 变异超边界，修复超边界。需要特别的修正。"+ RESET)
        H3_after_correction = H3_ini + weight * delta_ToSaveLife * (Boundary_H3 - H3_ini)

    elif H3_ini[0] > 0.001:
        delta_ToSaveLife =np.array([0.0001,1, 0, 0 ])
        # 情况2: 变异超边界，修复未超边界
        print(YELLOW +"情况2: 变异超边界，修复未超边界。进行部分修正。"+ RESET)
        print(YELLOW +"边界值受到-->动态冲击---> 被迫调整" + RESET)
        print('冲击前-Boundary_H3=',Boundary_H3)
        Boundary_H3[1] = (1+0.002)* Boundary_H3[1]  # 边界值动态调整
        Boundary_H3[0] = (1+0.001)* Boundary_H3[0]  # 边界值动态调整
        print('冲击后-Boundary_H3=',Boundary_H3)
        if Boundary_H3[1]>1.2  :
            Boundary_H3[1] =1.21

        H3_after_correction = H3_ini + weight * delta_ToSaveLife * (Boundary_H3 - H3_ini)

    elif H3_ini[2] < 1e-6:
        delta_ToSaveLife =np.array([0, 1, 0.1, 0 ])
        # 情况3: 变异未超边界，修复超边界
        print(BLUE +"情况3: 变异未超边界，修复超边界。进行部分修正。"+ RESET)
        H3_after_correction = H3_ini + weight * delta_ToSaveLife* (Boundary_H3 - H3_ini)

    else:
        # 情况4: 变异、修复都未超边界
        print("情况4: 变异、修复都未超边界。进行常规修正。")
        #H3_after_correction = H3_ini + weight * delta_combined * H3_ini
        # 不需要边界修正，正常修正
        H3_after_correction = H3_ini + weight * delta_combined * H3_ini
    return H3_after_correction,Boundary_H3 

# # 示例使用
# H3_ini_example = np.array([1.2, 3, 0.000001, 0.00001])
# delta_combined_example = np.array([-0.01, 0.02, -0.005, 0.0001])
# H3_after_correction = apply_boundary_correction_advanced(H3_ini_example, delta_combined_example)
# print("H3 after correction:", H3_after_correction)





def boundary_disturbance(Boundary_H3):
    """
    对Boundary_H3进行外部更大因素的扰动。
    
    参数:
    Boundary_H3: 当前的Boundary_H3值。
    
    返回:
    新的Boundary_H3值，受到外部因素的扰动。
    """

    # Boundary_H3 = np.array([1e-14, 0, 1e-4, 0]) 
    # 扰动因子范围在1%的上下浮动
    disturbance_factor = 0.003
    # 对Boundary_H3的每个元素应用扰动
    for i in range(len(Boundary_H3)):
        Boundary_H3[i] += random.uniform(-disturbance_factor, disturbance_factor) * Boundary_H3[i]
    
    # 确保Boundary_H3的值不会超出合理范围
    Boundary_H3[0] = max(min(Boundary_H3[0], 0.05), 1e-10)
    Boundary_H3[2] = max(min(Boundary_H3[2], 0.05), 1e-10)
    
    return Boundary_H3




def fn011_combined_delta(v2_TP53, v2_BRCA1, u_ini, H3_ini, lay1_iterations, lay2_iterations, Boundary_H3 ,debug_mode=False, test_random=True):
    """
    计算结合TP53和BRCA1基因的影响后的Delta值和多层网络（MLN）输出。

    参数:
    v2_TP53: TP53基因的特征谱
    v2_BRCA1: BRCA1基因的特征谱
    u_ini: 初始的双层网络值
    H3_ini: 初始和谐集合H3的值
    lay1_iterations: 第一层网络的迭代次数
    lay2_iterations: 第二层网络的迭代次数
    debug_mode: 是否开启调试模式
    test_random: 是否进行随机测试

    返回:
    combined_delta: 结合两基因的Delta值
    MLN_output_V3: 多层网络的输出
    NL_final_V4: 最终的新生负荷值
    """
    # ANSI 转义序列颜色代码
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'  # 重置颜色

    # 计算TP53的Delta值
    W_tp53 = np.zeros((4, 17))
    W_tp53[2, 16] = 1 * v2_TP53[2]  # TP53对第三行的影响
    delta_tp53 = W_tp53 @ v2_TP53

    # 计算BRCA1的Delta值
    W_brca1 = np.zeros((4, 17))
    W_brca1[0, 16] = 1 * v2_BRCA1[0]  # BRCA1对第一行的影响
    delta_brca1 = W_brca1 @ v2_BRCA1

    # 结合两个Delta值
    w_tp53 = 0.5
    w_brca1 = 0.5
    delta_combined = w_tp53 * delta_tp53 + w_brca1 * delta_brca1

    # 调整和谐集合H3并模拟多层网络动态
    weight = 0.5
    # -----------------------------伟大的额算法思想----伟大的边界修正------伟大的半盲学习------------
    # BoundaryH3=[]如果突变严重，如果无法啊修复-几乎发散进入死亡阶段。因此超越了这种模式。为避免发散设定一个边界。
    # 如果、H3_ini [0] > 1. 或者H3_ini[3]<1e-10 太小. 则
    # if 如果、H3_ini [0] > 1. 或者H3_ini[3]<1e-10 太小. 则

    #     Boundary_H3 = [0.0001, 5, 0.001, 0]
    #     H3_after_genamonic_tf = H3_ini + weight * delta_combined *( Boundary_H3 - H3_ini)

    # else 
    #     H3_after_genamonic_tf = H3_ini + weight * delta_combined * H3_ini
    
    # -----------------------------伟大的额算法思想----伟大的边界修正------伟大的半盲学习------The END------

    # 示例使用
    # H3_ini_example = np.array([0.2, 3, 0.05, 0.00001])
    # delta_combined_example = np.array([-0.01, 0.02, -0.005, 0.0001])
    H3_after_genamonic_tf,Boundary_H3  = apply_boundary_correction_advanced(H3_ini, delta_combined,Boundary_H3)

    print("--H3 after correction:", H3_after_genamonic_tf)


    MLN_output_V3 = V3_simulate_MLN(H3_after_genamonic_tf, u_ini, lay1_iterations, lay2_iterations)
    NL_final_V4 = MLN_output_V3[-1]

    # 调试信息输出
    if debug_mode:
            # 输出MLN_output_V3的尺寸
        # print(BLUE + "LOOK HERE Debug ---------------"+ RESET)
        print( "-------------->H3 H3_after_genamonic_tf :", H3_after_genamonic_tf )

        print("Combined Delta:", delta_combined)
        print("NL final V4:", NL_final_V4)
        print("H3_after_genamonic_tf:",H3_after_genamonic_tf)

    return delta_combined, MLN_output_V3, NL_final_V4,H3_after_genamonic_tf,Boundary_H3 


if __name__ == "__main__":

    # ANSI 转义序列颜色代码
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'  # 重置颜色
    # 四组不同的损伤对
    damage_pairs = [(0.01, 0.0) ,(0.07, 0.11), (0.21, 0.23) ,(0.33, 0.12),(0.27, 0.37)]
    colors = ['blue','brown', 'green', 'red', 'black']

    # 准备图形
    fig, axs = plt.subplots(5, 1, figsize=(10, 8))

    # 遍历每组损伤对，进行多层网络分析
    for index, (v1_brca1_damage, v1_tp53_damage) in enumerate(damage_pairs):
        Boundary_H3 = init_boundary_H3()

        print(BLUE + "init-Boundary-----:" +RESET)
        print('Boundary=',Boundary_H3)

        total_MLN_output = []
        u_ini = 0.01
        cycles = 365* 8 #365 * 1 # 5年周期
        H3_ini = np.array([1e-10, 0.6, 5e-4, 0])


        v2_TP53 = np.array([0, 0, -1, 0] + [0] * 12 + [v1_tp53_damage])
        v2_BRCA1 = np.array([1, 0, 0, 0] + [0] * 12 + [v1_brca1_damage])


        day =0
        H3_storage=[]
        H3_storage.extend(H3_ini)
        H3_storage.extend(H3_ini)
        for cycle in range(1,cycles):


            # 根据CSV文件中的数据设置突变周期
            sleep_hours = sleep_hours_dict[cycle]
            repair_duration = sleep_hours*10

            mutation_duration = 240 - repair_duration

            # 使用固定的随机数种子产生的随机数
            # mutation_duration = random.randint(12, 19)
            # repair_duration = 24 - mutation_duration

            # 突变周期的分析...
            delta_combined, MLN_output_V3, NL_final_V4,H3_after_genamonic_tf,Boundary_H3 = fn011_combined_delta(v2_TP53, v2_BRCA1, u_ini, H3_ini, mutation_duration, repair_duration,Boundary_H3 , debug_mode=True, test_random=True)
            total_MLN_output.extend(MLN_output_V3)
            u_ini  = MLN_output_V3[-1]
        
            # 根据CSV文件中的数据调整H3_after_genamonic_tf
            print('BEFORE-根据CSV文件中的数据调整H3_BEFORE_genamonic_tf- H3_after_genamonic_tf = ', H3_after_genamonic_tf)
            is_summer, effect_on_H3_0, effect_on_H3_2 = seasonal_effect_dict[cycle]

            print('effect_on_H3_0 = ',effect_on_H3_0)
            print('effect_on_H3_2 = ',effect_on_H3_2)
            print(' H3_ini        = ', H3_ini )
            # Boundary_H3 = np.array([0.001, 1, 0.01, 0])


            # 示例使用
            # Boundary_H3 = init_boundary_H3()
            # print("Initial Boundary_H3:", Boundary_H3)
            print(BLUE + 'Disturbed Boundary_H3-- （Week INFLENECE，in future, if need） ---' +RESET)
            Boundary_H3_disturbed = boundary_disturbance(Boundary_H3)
            print("Disturbed Boundary_H3:", Boundary_H3_disturbed)
            H3_after_genamonic_tf[0] = H3_after_genamonic_tf[0] + effect_on_H3_0 *1.5* (Boundary_H3_disturbed[0] - H3_after_genamonic_tf[0] )
            H3_after_genamonic_tf[2] = H3_after_genamonic_tf[2] + effect_on_H3_2 *0.5* (Boundary_H3_disturbed[2] - H3_after_genamonic_tf[2])
            

            # H3_after_genamonic_tf[0] = H3_after_genamonic_tf[0] - effect_on_H3_0 *H3_after_genamonic_tf[0]*0.9   #(Boundary_H3[0] - H3_after_genamonic_tf[0] + effect_on_H3_0)
            # H3_after_genamonic_tf[2] = H3_after_genamonic_tf[2] + effect_on_H3_2 *H3_after_genamonic_tf[0]*1  #(Boundary_H3[2] - H3_after_genamonic_tf[2] + effect_on_H3_2 )
            
            print('-After 根据CSV文件中的数据调整H3_after_genamonic_tf- H3_after_genamonic_tf = ', H3_after_genamonic_tf)

            # -----------根据CSV文件中的数据调整H3_after_genamonic_tf END ----------

            H3_ini = H3_after_genamonic_tf
            print ('-----------H3_init --------------=' ,H3_ini)





            # day = day+1
            # if day == 7 :
            #     H3_storage.extend(H3_ini)
            #     H3_influnece = H3_storage[-2]
            #     day = 0
            #     3_after_genamonic_tf[0] = H3_after_genamonic_tf[0] - effect_on_H3_0 *H3_influnece[0]*0.9   #(Boundary_H3[0] - H3_after_genamonic_tf[0] + effect_on_H3_0)
            #     H3_after_genamonic_tf[2] = H3_after_genamonic_tf[2] + effect_on_H3_2 *H3_influnece[0]*1  #(Boundary_H3[2] - H3_after_genamonic_tf[2] + effect_on_H3_2 )
            #     print(BLUE + 'Week INFLENECE ---' +RESET)
            #     print('-day == 7----Week Invluece IMPACT !!! After 根据CSV文件中的数据调整H3_after_genamonic_tf- H3_after_genamonic_tf = ', H3_after_genamonic_tf)
            


        # 绘制每组损伤对的结果
        axs[index].plot(total_MLN_output, color=colors[index])
        axs[index].set_xlabel('Hours')  # (length : Cycles * (lay1_inte + lay2 -inte)) = 40 * 200 = 8000
        axs[index].set_ylabel('Neoplastic Load Value')
        axs[index].legend([f'BRCA1 Damage: {v1_brca1_damage}, TP53 Damage: {v1_tp53_damage}'])
        axs[index].grid(True)
        axs[index].set_ylim([-0.1, 1.22])

    # 设置总标题并调整布局
    plt.suptitle('Impact of TP53 and BRCA1 Gene Alterations on Tumor Dynamics - A Multi-Layer Network Analysis')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show(block=False)
    plt.pause(10)
    plt.close()
