import matplotlib.pyplot as plt
import numpy as np
import random
from sa005package.kangroll_basic_fn001_mln_com_release import fn010_translp, V3_simulate_MLN

def fn011_combined_delta(v2_TP53, v2_BRCA1, u_ini, H3_ini, lay1_iterations, lay2_iterations, debug_mode=False, test_random=True):
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
    weight = 0.02
    H3_after_genamonic_tf = H3_ini + weight * delta_combined * H3_ini
    MLN_output_V3 = V3_simulate_MLN(H3_after_genamonic_tf, u_ini, lay1_iterations, lay2_iterations)
    NL_final_V4 = MLN_output_V3[-1]

    # 调试信息输出
    if debug_mode:
            # 输出MLN_output_V3的尺寸
        #print("-------------->Size of MLN_output_V3:", len(MLN_output_V3))

        print("Combined Delta:", delta_combined)
        print("NL final V4:", NL_final_V4)
        print("H3_after_genamonic_tf:",H3_after_genamonic_tf)

    return delta_combined, MLN_output_V3, NL_final_V4,H3_after_genamonic_tf

# 四组不同的损伤对
damage_pairs = [(0.0, 0.0), (0.01, 0.02) , (0.15, 0.20), (0.15, 0.21)]
colors = ['blue', 'green', 'red', 'black']

# 准备图形
fig, axs = plt.subplots(4, 1, figsize=(10, 8))

# 遍历每组损伤对，进行多层网络分析
for index, (v1_brca1_damage, v1_tp53_damage) in enumerate(damage_pairs):
    total_MLN_output = []
    u_ini = 0.01
    cycles = 365 * 10 # 5年周期
    H3_ini = np.array([0.0001, 5, 0.020, 0])

    v2_TP53 = np.array([0, 0, -1, 0] + [0] * 12 + [v1_tp53_damage])
    v2_BRCA1 = np.array([1, 0, 0, 0] + [0] * 12 + [v1_brca1_damage])


    for cycle in range(cycles):
        # 使用固定的随机数种子产生的随机数
        mutation_duration = random.randint(12, 19)
        repair_duration = 24 - mutation_duration

        # 突变周期的分析...
        delta_combined, MLN_output_V3, NL_final_V4,H3_after_genamonic_tf= fn011_combined_delta(v2_TP53, v2_BRCA1, u_ini, H3_ini, mutation_duration, repair_duration, debug_mode=True, test_random=True)
        total_MLN_output.extend(MLN_output_V3)
        u_ini  = MLN_output_V3[-1]
        H3_ini = H3_after_genamonic_tf



    # 绘制每组损伤对的结果
    axs[index].plot(total_MLN_output, color=colors[index])
    axs[index].set_xlabel('Hours')  # (length : Cycles * (lay1_inte + lay2 -inte)) = 40 * 200 = 8000
    axs[index].set_ylabel('Neoplastic Load Value')
    axs[index].legend([f'BRCA1 Damage: {v1_brca1_damage}, TP53 Damage: {v1_tp53_damage}'])
    axs[index].grid(True)
    axs[index].set_ylim([-0.1, 5.0])

# 设置总标题并调整布局
plt.suptitle('Impact of TP53 and BRCA1 Gene Alterations on Tumor Dynamics - A Multi-Layer Network Analysis')
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show(block=False)
plt.pause(10)
plt.close()
