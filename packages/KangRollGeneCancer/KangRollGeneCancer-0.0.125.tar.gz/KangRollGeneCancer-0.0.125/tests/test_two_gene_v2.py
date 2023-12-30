import matplotlib.pyplot as plt
import numpy as np
import random
from sa004package.kangroll_basic_fn001_mln_com_release import fn010_translp

# 更新基因功能特征谱
v2_TP53 = np.array([0, 1, 1, 0] + [0]*12 + [0.2])  # TP53基因特征谱
v2_BRCA1 = np.array([0, 1, 1, 0] + [0]*12 + [0.3])  # BRCA1基因特征谱

# 初始化参数
u_ini = 0.1  # 初始的双层网络值
iterations_per_gene = 300  # 每个基因的迭代次数
cycles = 10  # 总循环次数
total_MLN_output = []

# 模拟过程
for cycle in range(cycles):
    # TP53的影响
    for i in range(iterations_per_gene):
        random.seed(42 + i)
        H3_ini_test = np.array([random.uniform(0.0003, 0.001), 1, 0.0018, 0])
        MLN_output_TP53, NL_final = fn010_translp(0.2, v2_TP53, u_ini, H3_ini_test, 50, 100)
        u_ini = MLN_output_TP53[-1]  # 更新u_ini为TP53影响后的最后一个值
        total_MLN_output.extend(MLN_output_TP53)

    # BRCA1的影响
    for i in range(iterations_per_gene):
        random.seed(42 + i + iterations_per_gene)
        H3_ini_test = np.array([random.uniform(0.0003, 0.001), 1, 0.0018, 0])
        MLN_output_BRCA1, NL_final = fn010_translp(0.3, v2_BRCA1, u_ini, H3_ini_test, 50, 100)
        u_ini = MLN_output_BRCA1[-1]  # 更新u_ini为BRCA1影响后的最后一个值
        total_MLN_output.extend(MLN_output_BRCA1)

# 绘制图像
plt.figure(figsize=(10, 6))  # 设置图像大小
plt.plot(total_MLN_output, color='blue')  # 绘制总的MLN输出
plt.title('Impact of TP53 and BRCA1 Gene Alterations on Tumor Dynamics: A Multi-Layer Network Analysis')
plt.xlabel('Hours')
plt.ylabel('Neoplastic Load Value')

# 添加图例
plt.legend(["TP53 Damage: 0.2, BRCA1 Damage: 0.3"])

# 添加网格
plt.grid(True)

# 设置y轴的上下限
plt.ylim([0, 0.5])

# 显示图像
plt.show()
