import matplotlib.pyplot as plt
import numpy as np
import random
from sa005package.kangroll_basic_fn001_mln_com_release import fn010_translp,V3_simulate_MLN

# 定义TP53和BRCA1的基因功能特征谱
        # GFFS:
        # - TP 53   : [0 0 -1 0 ]  -tau2

        # v2_test = np.array([0, 0, -1, 0] + [0]*12 + [v1_test])  # BRAC1 的基因功能特征谱
        
        # -  BRAC1: [1 0 0 0 ]    - tau1
        # v2_test = np.array([1, 0, 0, 0] + [0]*12 + [v1_test])  # BRAC1 的基因功能特征谱 



# fn011_combined_delta



# 定义函数
# def fn010_translp(v1, v2, u_ini, H3_ini, lay1_iterations, lay2_iterations, debug_mode=False, test_random=True):

def fn011_combined_delta(v2_TP53,v2_BRCA1,u_ini, H3_ini, lay1_iterations, lay2_iterations, debug_mode=False, test_random=True):
    
    # v2_TP53 = np.array([0, 0, -1, 0] + [0]*12 + [v1_tp53_damage])  # TP53示例参数
    # v2_BRCA1 = np.array([1, 0, 0,0] + [0]*12 + [v1_brca1_damage])  # BRCA1示例参数

    v2 = v2_TP53 
    # 初始化17维的权重矩阵 W
    W_v3 = np.zeros((4, 17))
    # W_v3[0, 16] = -1 * v2[0]  # 第1位控制W的第1行
    # W_v3[2, 16] = -1 * v2[1]  # 第2位控制W的第3行

    W_v3[0, 16] =  1*  v2[0] 
    W_v3[1, 16] =  1*  v2[1] 
    W_v3[2, 16] =  1*  v2[2] 
    W_v3[3, 16] =  1*  v2[3] 

    # 计算调整因子 Delta

    delta_tp53 = W_v3 @ v2

    v2 = v2_BRCA1
    # 初始化17维的权重矩阵 W
    W_v3 = np.zeros((4, 17))
    # W_v3[0, 16] = -1 * v2[0]  # 第1位控制W的第1行
    # W_v3[2, 16] = -1 * v2[1]  # 第2位控制W的第3行

    W_v3[0, 16] =  1*  v2[0] 
    W_v3[1, 16] =  1*  v2[1] 
    W_v3[2, 16] =  1*  v2[2] 
    W_v3[3, 16] =  1*  v2[3] 

    # 计算调整因子 Delta

    delta_brca1 = W_v3 @ v2


    # 权重因子
    w_tp53 = 0.5
    w_brca1 = 0.5

    # 加权平均Delta
    delta_combined = w_tp53 * delta_tp53 + w_brca1 * delta_brca1

    # # print('delta_v3 =',delta_v3)
    # w =2;
    # # 调整和谐集合 H3
    # H3_after_genamonic_tf = H3_ini + w*delta_v3 * H3_ini

    if debug_mode:

        print("Debug Information:")
        print("delta_tp53:", delta_tp53)
        print("delta_brca1:", delta_brca1)
        print("delta_combined :", delta_combined )
        # print("Delta:", delta_v3)
        # print("H3:", H3_after_genamonic_tf)

    # # 模拟多层网络动态
    # MLN_output_V3 = V3_simulate_MLN(H3_after_genamonic_tf, u_ini,lay1_iterations, lay2_iterations)

    # # 计算新生负荷
    # NL_final_V4 = MLN_output_V3[-1]

    # if debug_mode:
    #     print("v2_TP53 :", v2_TP53 )
    #     print("v2_BRCA1:", v2_BRCA1)
    #     print("combined_delta=",combined_delta)

    # print('delta_v3 =',delta_v3)
    weight =2;
    # 调整和谐集合 H3
    H3_after_genamonic_tf = H3_ini + weight*delta_combined * H3_ini

    print('H3_after_genamonic_tf ',H3_after_genamonic_tf )
    # 模拟多层网络动态
    MLN_output_V3 = V3_simulate_MLN(H3_after_genamonic_tf, u_ini,lay1_iterations, lay2_iterations)

    # 计算新生负荷
    NL_final_V4 = MLN_output_V3[-1]

    if debug_mode:
        # print("V3:", MLN_output_V3)
        print("NL final V4:", NL_final_V4)

    return delta_combined,MLN_output_V3, NL_final_V4





# 四组不同的损伤对
damage_pairs = [(0.1, 0.2),(0.2, 0.3), (0.4, 0.4), (0.5, 0.3)]
colors = ['blue', 'green', 'red', 'black']  # 颜色列表

# 准备图形
fig, axs = plt.subplots(4, 1, figsize=(10, 8))



for index, (v1_brca1_damage,v1_tp53_damage) in enumerate(damage_pairs):
    total_MLN_output = []
    # 初始化参数
    u_ini = 0.01  # 初始的双层网络值
    cycles = 40  # 总循环次数
    # random.seed(42 + cycle * 100 + i)
    H3_ini_test = np.array([0.001, 1, 0.010, 0])    #修复的时间是2倍， 修复规模是10倍。
    total_MLN_output = [] 

    print ('v1_brca1_damage',v1_brca1_damage)
    print ('v1_tp53_damage=',v1_tp53_damage)


    # v2_TP53 = np.array([0, 0, -1, 0] + [0]*12 + [0.2])  # TP53示例参数
    # v2_BRCA1 = np.array([1, 0, 0,0] + [0]*12 + [0.3])  # BRCA1示例参数

    v2_TP53 = np.array([0, 0, -1, 0] + [0]*12 + [v1_tp53_damage])  # TP53示例参数
    v2_BRCA1 = np.array([1, 0, 0,0] + [0]*12 + [v1_brca1_damage])  # BRCA1示例参数

    for cycle in range(cycles):

        delta_combined,MLN_output_V3, NL_final_V4 = fn011_combined_delta(v2_TP53,v2_BRCA1,u_ini, H3_ini_test, lay1_iterations=100, lay2_iterations=100, debug_mode=True, test_random=True)

        total_MLN_output.extend(MLN_output_V3)

        print('in main:combined_delta =',delta_combined )
        # print("--------V3:", MLN_output_V3)
        print("NL final V4:", NL_final_V4)
        u_ini = MLN_output_V3[-1]


#     # v1_test_barc1_inverse = (1 - v1_brca1_damage)
#     # print("v1_test_barc1_inverse",v1_test_barc1_inverse)

#     for cycle in range(cycles):
#         # TP53的影响
#         for i in range(random.randint(10, 30)):
#             random.seed(42 + cycle * 100 + i)
#             H3_ini_test = np.array([random.uniform(0.0001, 0.0004), 1, 0.0010, 0])
#             MLN_output_TP53, _ = fn010_translp(v1_tp53_damage, v2_TP53, u_ini, H3_ini_test, 50, 50,debug_mode=False, test_random=True)
#             # MLN_output, NL_final = fn010_translp(v1_test, v2_test, u_ini_test, H3_ini_test, lay1_iterations_test, lay2_iterations_test, debug_mode=False, test_random=True)
#             u_ini = MLN_output_TP53[-1]
#             total_MLN_output.extend(MLN_output_TP53)

#         # BRCA1的影响
#         for i in range(random.randint(10, 30)):
#             random.seed(43 + cycle * 100 + i)
#             # H3_ini_test = np.array([random.uniform(0.0001, 0.00025), 1, 0.0008, 0])
#             MLN_output_BRCA1, _ = fn010_translp(v1_brca1_damage, v2_BRCA1, u_ini, H3_ini_test, 50, 50,debug_mode=False, test_random=True)
#             u_ini = MLN_output_BRCA1[-1]
#             total_MLN_output.extend(MLN_output_BRCA1)

    # 绘制子图
    axs[index].plot(total_MLN_output, color=colors[index])
    axs[index].set_xlabel('Hours')
    axs[index].set_ylabel('Neoplastic Load Value')
    axs[index].legend([f'BRCA1 Damage: {v1_brca1_damage},TP53 Damage: {v1_tp53_damage}'])
    axs[index].grid(True)
    axs[index].set_ylim([-0.1, 1.0])

# 添加总标题
plt.suptitle('Impact of TP53 and BRCA1 Gene Alterations on Tumor Dynamics - A Multi-Layer Network Analysis')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # 调整布局以避免重叠
plt.show(block=False)
plt.pause(10)
plt.close()
