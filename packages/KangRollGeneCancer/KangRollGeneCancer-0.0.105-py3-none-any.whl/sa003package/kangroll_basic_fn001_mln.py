# kangroll_basic_fn001_mln.py 

import matplotlib.pyplot as plt
import numpy as np

def fn001_mln(a, b):
    return a + b

def layer_one(u1, tau1, B1, iterations):
    u1_values = []
    for _ in range(iterations):
        u1 = u1 + tau1 * (B1 - u1)
        u1_values.append(u1)
    return u1_values

def layer_two(u2, tau2, B2, iterations):
    u2_values = []
    for _ in range(iterations):
        u2 = u2 + tau2 * (B2 - u2)
        u2_values.append(u2)
    return u2_values

def V3_simulate_MLN(H3, u_ini, lay1_iterations, lay2_iterations):
    tau1, B1, tau2, B2 = H3
    u1_values = layer_one(u_ini, tau1, B1, lay1_iterations)
    u2_values = layer_two(u1_values[-1], tau2, B2, lay2_iterations)
    return u1_values + u2_values


if __name__ == "__main__":
    # 测试 fn001_mln 函数
    print("Test: add(2, 3) =", fn001_mln(2, 3))

    print('kangroll_basic_fn001_mln.py go mln :\n')
    # 测试数据
    H3 = [0.001, 1, 0.005, 0]  # 和谐集合H的初始值
    u_ini = 0  # 双层网络的初始值
    lay1_iterations = 50  # 第一层迭代次数
    lay2_iterations = 200  # 第二层迭代次数

    # 进行模拟
    MLN_output = V3_simulate_MLN(H3, u_ini, lay1_iterations, lay2_iterations)

    # 绘制图像
    plt.plot(MLN_output)
    plt.title('Multi-Layer Network Output')
    plt.xlabel('Iterations')
    plt.ylabel('Output')
    plt.show(block=False)

    # 显示3秒后关闭
    plt.pause(1)
    plt.close()
