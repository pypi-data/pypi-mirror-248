import matplotlib.pyplot as plt
import numpy as np
import random
from sa004package.kangroll_basic_fn001_mln_com_release import fn010_translp

# 定义TP53和BRCA1的基因功能特征谱
v2_TP53 = np.array([0, 1, 1, 0] + [0]*12 + [0.2])  # 示例参数
v2_BRCA1 = np.array([0, 1, 1, 0] + [0]*12 + [0.3])  # 示例参数

# 初始化参数
u_ini = 0.01  # 初始的双层网络值
cycles = 10  # 总循环次数

# 损伤值
v1_tp53_damage = 0.1
v1_brca1_damage = 0.3

total_MLN_output = []

for cycle in range(cycles):
    # TP53的影响
    tp53_iterations = random.randint(10, 50)  # 随机决定TP53的迭代次数
    for i in range(tp53_iterations):
        random.seed(42 + cycle * 100 + i)  # 每个周期使用不同的随机种子
        H3_ini_test = np.array([random.uniform(0.0001, 0.0002), 1, 0.0011, 0])
        MLN_output_TP53, _ = fn010_translp(v1_tp53_damage, v2_TP53, u_ini, H3_ini_test, 50, 100)
        u_ini = MLN_output_TP53[-1]  # 更新u_ini为TP53影响后的最后一个值
        total_MLN_output.extend(MLN_output_TP53)

    # BRCA1的影响
    brca1_iterations = random.randint(10, 50)  # 随机决定BRCA1的迭代次数
    for i in range(brca1_iterations):
        random.seed(43 + cycle * 100 + i)  # 更新随机数种子，保持与TP53不同
        H3_ini_test = np.array([random.uniform(0.0001, 0.00025), 1, 0.0008, 0])
        MLN_output_BRCA1, _ = fn010_translp(v1_brca1_damage, v2_BRCA1, u_ini, H3_ini_test, 50, 100)
        u_ini = MLN_output_BRCA1[-1]  # 更新u_ini为BRCA1影响后的最后一个值
        total_MLN_output.extend(MLN_output_BRCA1)

# 绘制图像
plt.figure(figsize=(10, 6))
plt.plot(total_MLN_output, color='blue')
plt.title(f'Multi-Layer Network Output with TP53 Damage: {v1_tp53_damage} and BRCA1 Damage: {v1_brca1_damage}')
plt.xlabel('Hours')
plt.ylabel('Neoplastic Load Value')
plt.grid(True)
plt.ylim([0, 0.5])
plt.show(block=False)
plt.pause(5)
plt.close()
