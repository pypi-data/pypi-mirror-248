import matplotlib.pyplot as plt
import numpy as np
import random
from sa005package.kangroll_basic_fn001_mln_com_release import fn010_translp

# 定义TP53和BRCA1的基因功能特征谱
        # GFFS:
        # - TP 53   : [0 0 -1 0 ]  -tau2

        # v2_test = np.array([0, 0, -1, 0] + [0]*12 + [v1_test])  # BRAC1 的基因功能特征谱
        
        # -  BRAC1: [1 0 0 0 ]    - tau1
        # v2_test = np.array([1, 0, 0, 0] + [0]*12 + [v1_test])  # BRAC1 的基因功能特征谱 




# 初始化参数
u_ini = 0.01  # 初始的双层网络值
cycles = 10  # 总循环次数

# 四组不同的损伤对
damage_pairs = [(0.1, 0.3),(0.1, 0.2), (0.9, 0.2), (0.1, 0.5)]
colors = ['blue', 'green', 'red', 'black']  # 颜色列表

# 准备图形
fig, axs = plt.subplots(4, 1, figsize=(10, 8))

# 遍历每组损伤对
for index, (v1_brca1_damage,v1_tp53_damage) in enumerate(damage_pairs):
    total_MLN_output = []

    print ('v1_brca1_damage',v1_brca1_damage)
    print ('v1_tp53_damage=',v1_tp53_damage)


    # v2_TP53 = np.array([0, 0, -1, 0] + [0]*12 + [0.2])  # TP53示例参数
    # v2_BRCA1 = np.array([1, 0, 0,0] + [0]*12 + [0.3])  # BRCA1示例参数

    v2_TP53 = np.array([0, 0, -1, 0] + [0]*12 + [v1_tp53_damage])  # TP53示例参数
    v2_BRCA1 = np.array([1, 0, 0,0] + [0]*12 + [v1_brca1_damage])  # BRCA1示例参数

    # v1_test_barc1_inverse = (1 - v1_brca1_damage)
    # print("v1_test_barc1_inverse",v1_test_barc1_inverse)

    for cycle in range(cycles):
        # TP53的影响
        for i in range(random.randint(10, 30)):
            random.seed(42 + cycle * 100 + i)
            H3_ini_test = np.array([random.uniform(0.0001, 0.0004), 1, 0.0010, 0])
            MLN_output_TP53, _ = fn010_translp(v1_tp53_damage, v2_TP53, u_ini, H3_ini_test, 50, 50,debug_mode=False, test_random=True)
            # MLN_output, NL_final = fn010_translp(v1_test, v2_test, u_ini_test, H3_ini_test, lay1_iterations_test, lay2_iterations_test, debug_mode=False, test_random=True)
            u_ini = MLN_output_TP53[-1]
            total_MLN_output.extend(MLN_output_TP53)

        # BRCA1的影响
        for i in range(random.randint(10, 30)):
            random.seed(43 + cycle * 100 + i)
            # H3_ini_test = np.array([random.uniform(0.0001, 0.00025), 1, 0.0008, 0])
            MLN_output_BRCA1, _ = fn010_translp(v1_brca1_damage, v2_BRCA1, u_ini, H3_ini_test, 50, 50,debug_mode=False, test_random=True)
            u_ini = MLN_output_BRCA1[-1]
            total_MLN_output.extend(MLN_output_BRCA1)

    # 绘制子图
    axs[index].plot(total_MLN_output, color=colors[index])
    axs[index].set_xlabel('Hours')
    axs[index].set_ylabel('Neoplastic Load Value')
    axs[index].legend([f'BRCA1 Damage: {v1_brca1_damage},TP53 Damage: {v1_tp53_damage}'])
    axs[index].grid(True)
    axs[index].set_ylim([0, 0.9])

# 添加总标题
plt.suptitle('Impact of TP53 and BRCA1 Gene Alterations on Tumor Dynamics - A Multi-Layer Network Analysis')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # 调整布局以避免重叠
plt.show(block=False)
plt.pause(10)
plt.close()
