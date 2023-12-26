# from sa003package.kankrool_basiac_fn001_mln import fn001_mln

# import sys
# import os

# # 计算 my_package 的路径
# my_package_path = os.path.dirname(os.path.abspath(__file__))

# # 将 my_package 添加到 sys.path
# if my_package_path not in sys.path:
#     sys.path.append(my_package_path)

# import sys
# sys.path.append('/Users/kang/1.live_wit_GPT4/code_pypi/standalone003gntmcallmlnWrokspace/sa003_env/lib/python3.8/site-packages/sa003package/')

import matplotlib.pyplot as plt
import numpy as np


from sa003package.kangroll_basic_fn001_mln_release import fn001_mln,V3_simulate_MLN

# sa003package;sa003package.

def test_add():
    result = fn001_mln(3, 50)
    print("Obfuscated:", result)

if __name__ == "__main__":
    print('test from usr,import add sa002package.exfn001add_release:')
    test_add()

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
    plt.pause(3)
    plt.close()

