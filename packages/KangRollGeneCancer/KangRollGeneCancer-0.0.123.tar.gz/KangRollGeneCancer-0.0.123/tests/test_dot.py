import numpy as np

# 定义一个简单的矩阵 W 和向量 V2
W = np.array([[0, 0, 0],
              [0, 0, 0],
              [0, 0, -1]])
V2 = np.array([0, 1, 1])

# 计算矩阵 W 和向量 V2 的乘积
delta = np.dot(W, V2)

delta
print('delta=',delta)