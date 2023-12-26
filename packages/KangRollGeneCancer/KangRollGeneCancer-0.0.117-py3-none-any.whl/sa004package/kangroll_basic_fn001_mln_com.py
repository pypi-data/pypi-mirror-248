# kangroll_basic_fn001_mln.py 

import matplotlib.pyplot as plt
import numpy as np
import random

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


# 定义函数
def fn010_translp(v1, v2, u_ini, H3_ini, lay1_iterations, lay2_iterations, debug_mode=False, test_random=True):
    
    # 初始化17维的权重矩阵 W
    W_v3 = np.zeros((4, 17))
    W_v3[0, 16] = -1 * v2[0]  # 第1位控制W的第1行
    W_v3[2, 16] = -1 * v2[1]  # 第2位控制W的第3行

    # 计算调整因子 Delta

    delta_v3 = W_v3 @ v2

    # print('delta_v3 =',delta_v3)
    w =2;
    # 调整和谐集合 H3
    H3_after_genamonic_tf = H3_ini + w*delta_v3 * H3_ini

    if debug_mode:
        print("Debug Information:")
        print("V1:", v1)
        print("V2:", v2)
        print("W:", W_v3)
        print("Delta:", delta_v3)
        print("H3:", H3_after_genamonic_tf)


    # 模拟多层网络动态
    MLN_output_V3 = V3_simulate_MLN(H3_after_genamonic_tf, u_ini,lay1_iterations, lay2_iterations)

    # 计算新生负荷
    NL_final_V4 = MLN_output_V3[-1]

    if debug_mode:
        print("V3:", MLN_output_V3)
        print("NL final V4:", NL_final_V4)

    return MLN_output_V3, NL_final_V4

# if __name__ == "__main__":
#     # 测试 fn001_mln 函数
#     print("Test: add(2, 3) =", fn001_mln(2, 3))

#     print('kangroll_basic_fn001_mln.py go mln :\n')
#     # 测试数据
#     H3 = [0.001, 1, 0.005, 0]  # 和谐集合H的初始值
#     u_ini = 0  # 双层网络的初始值
#     lay1_iterations = 50  # 第一层迭代次数
#     lay2_iterations = 200  # 第二层迭代次数

#     # 进行模拟
#     MLN_output = V3_simulate_MLN(H3, u_ini, lay1_iterations, lay2_iterations)

#     # 绘制图像
#     plt.plot(MLN_output)
#     plt.title('Multi-Layer Network Output')
#     plt.xlabel('Iterations')
#     plt.ylabel('Output')
#     plt.show(block=False)

#     # 显示3秒后关闭
#     plt.pause(1)
#     plt.close()



if __name__ == "__main__":
    # print('test from usr,import add sa002package.exfn001add_release:')
    # test_add()

    # 测试 fn001_mln 函数
    print("Test: add(2, 3) =", fn001_mln(2, 3))

    print('kangroll_basic_fn001_mln.py go mln :\n')


    print('kangroll_basic_fn001_mln_test_kangroll_basic_fn001_mln_fromHiglevel.py go mln :\n')
    # 设置相同的随机数生成种子
    random.seed(42)

    # 图像设置为一列三行
    # fig, axs = plt.subplots(3, 1, figsize=(10, 15))
    # 图像设置为一列三行，但尺寸更小
    fig, axs = plt.subplots(4, 1, figsize=(6, 8))  # 尺寸调整为8x12

    # 损伤值的列表
    v1_values = [0.02, 0.10, 0.25,0.4]

    # 颜色列表，用于区分不同的损伤值
    colors = ['blue', 'green', 'red','black']


    # 对每个损伤值进行模拟
    for index, v1_test in enumerate(v1_values):
        v2_test = np.array([0, 1, 1, 0] + [0]*12 + [v1_test])  # TP 53的基因功能特征谱
        u_ini_test = 0.1   # 双层网络的初始值
        # 总的MLN_output存储变量
        total_MLN_output = []

        # 进行三十次循环迭代
        for i in range(600):
            # 为每次迭代设置相同的随机数种子
            random.seed(42 + i)

            # 生成随机数
            H3_ini_test = np.array([random.uniform(0.0003, 0.001), 1, 0.0018, 0])
            lay1_iterations_test = random.randint(10, 150)
            # lay2_iterations_test = 500 # 第二层迭代次数
            # lay1_iterations_test=100
            lay2_iterations_test=100

            # lay1_iterations_test =20
             # 打印当前迭代的随机数值
            # print(f"Iteration {i}: H3_ini_test = {H3_ini_test}, lay1_iterations_test = {lay1_iterations_test}")

            # print(f"----------lay1_iterations_test = {lay1_iterations_test}\n")

            # 调用函数
            MLN_output, NL_final = fn010_translp(v1_test, v2_test, u_ini_test, H3_ini_test, lay1_iterations_test, lay2_iterations_test, debug_mode=False, test_random=True)

            # 更新u_ini_test为MLN_output的最后一个值
            u_ini_test = MLN_output[-1]

            # 将MLN_output加入总的MLN_output
            total_MLN_output.extend(MLN_output)

        # 绘制每个损伤值的图像
        axs[index].plot(total_MLN_output, label=f'TP53 Damage: {v1_test}', color=colors[index])
        axs[index].set_title(f'TP53 Damage: {v1_test}')
        axs[index].set_xlabel('Hours')
        axs[index].set_ylabel('Neoplastic Load Value')
        axs[index].legend()
        axs[index].grid(True)
        axs[index].set_ylim([0, 0.8])  # 设置y轴的上下限



    # 显示整个图像
    plt.tight_layout()
    # plt.show()

    plt.tight_layout()
    # plt.savefig('./result/test_kangroll_basic_fn001_mln_v2_20231219_result.pdf')
    # plt.show()

    # # 显示图像，但不阻塞后续代码的执行
    plt.show(block=False)

    # 图像显示5秒后自动关闭
    plt.pause(2)
    plt.close()

