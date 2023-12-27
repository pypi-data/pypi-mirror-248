import matplotlib.pyplot as plt
import numpy as np
import random
from sa004package.kangroll_basic_fn001_mln_com_release import fn010_translp

# 定义TP53和BRCA1的基因功能特征谱
v2_TP53 = np.array([0, 1, 1, 0] + [0]*12 + [0.2])  # 示例参数
v2_BRCA1 = np.array([0, 1, 1, 0] + [0]*12 + [0.3])  # 示例参数

# 初始化参数
u_ini = 0.1  # 初始的双层网络值
iterations_per_gene = 300  # 每个基因的迭代次数
cycles = 10  # 总循环次数

# 损伤值的列表
v1_values = [0.02, 0.10, 0.25, 0.4]
total_MLN_outputs = []

# 对每个损伤值进行模拟
for v1_test in v1_values:
    total_MLN_output = []
    for cycle in range(cycles):
        # TP53的影响
        for i in range(random.randint(100, 300)):
            random.seed(42 + i)
            H3_ini_test = np.array([random.uniform(0.0003, 0.001), 1, 0.0018, 0])
            MLN_output_TP53, _ = fn010_translp(v1_test, v2_TP53, u_ini, H3_ini_test, 50, 100)
            u_ini = MLN_output_TP53[-1]  # 更新u_ini为TP53影响后的最后一个值
            total_MLN_output.extend(MLN_output_TP53)

        # BRCA1的影响
        for i in range(random.randint(100, 300)):
            random.seed(42 + i + iterations_per_gene)
            H3_ini_test = np.array([random.uniform(0.0003, 0.001), 1, 0.0018, 0])
            MLN_output_BRCA1, _ = fn010_translp(v1_test, v2_BRCA1, u_ini, H3_ini_test, 50, 100)
            u_ini = MLN_output_BRCA1[-1]  # 更新u_ini为BRCA1影响后的最后一个值
            total_MLN_output.extend(MLN_output_BRCA1)

    total_MLN_outputs.append(total_MLN_output)

# 绘制图像
colors = ['blue', 'green', 'red', 'black']
fig, axs = plt.subplots(len(v1_values), 1, figsize=(10, 8))
for index, total_MLN_output in enumerate(total_MLN_outputs):
    axs[index].plot(total_MLN_output, color=colors[index])
    axs[index].set_title(f'TP53 Damage: {v2_TP53[-1]}, BRCA1 Damage: {v2_BRCA1[-1]}, V1 Damage: {v1_values[index]}')
    axs[index].set_xlabel('Hours')
    axs[index].set_ylabel('Neoplastic Load Value')
    axs[index].set_ylim([0, 0.8])
    axs[index].grid(True)

plt.tight_layout()
plt.show(block=False)
plt.pause(10)
plt.close()
