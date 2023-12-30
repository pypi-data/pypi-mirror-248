import matplotlib.pyplot as plt
import numpy as np
import random
from sa004package.kangroll_basic_fn001_mln_com_release import fn010_translp

# 定义TP53和BRCA1的基因功能特征谱
v2_TP53 = np.array([0, 1, 1, 0] + [0]*12 + [0.2])  # 示例参数
# v2_BRCA1 = np.array([0.1] * 16)  # 示例参数
# 假设BRCA1的基因功能特征谱的长度与TP53一样
# 由于v2_TP53数组的最后一个元素为损伤值，我们也需要在v2_BRCA1中添加类似的值
v2_BRCA1 = np.array([0.1] * 16 + [0.2])  # 最后一个元素0.2为示例损伤值


# 初始化参数
u_ini = 0.1
iterations_per_gene = 300
total_MLN_output = []

# 模拟过程
for cycle in range(10):  # 总循环次数
    # TP53的影响
    for i in range(iterations_per_gene):
        random.seed(42 + i)
        H3_ini_test = np.array([random.uniform(0.0003, 0.001), 1, 0.0018, 0])
        MLN_output_TP53, _ = fn010_translp(0.2, v2_TP53, u_ini, H3_ini_test, 50, 100)
        total_MLN_output.extend(MLN_output_TP53)

    # BRCA1的影响
    for i in range(iterations_per_gene):
        random.seed(42 + i + iterations_per_gene)
        H3_ini_test = np.array([random.uniform(0.0003, 0.001), 1, 0.0018, 0])
        MLN_output_BRCA1, _ = fn010_translp(0.2, v2_BRCA1, u_ini, H3_ini_test, 50, 100)
        total_MLN_output.extend(MLN_output_BRCA1)

# 绘制图像
plt.plot(total_MLN_output)
plt.title('Multi-Layer Network Output with TP53 and BRCA1')
plt.xlabel('Iterations')
plt.ylabel('Output')
plt.show(block=False)
plt.pause(5)
plt.close()
