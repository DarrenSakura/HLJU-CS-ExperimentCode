import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']  
plt.rcParams['axes.unicode_minus'] = False    

# 1. 模糊量的定义
weight = ctrl.Antecedent(np.arange(0, 21, 1), '衣物重量 (kg)')
dirt = ctrl.Antecedent(np.arange(0, 101, 1), '污浊程度 (%)')
wash_time = ctrl.Consequent(np.arange(0, 61, 1), '洗涤时间 (分钟)')

# 2. 定义模糊子集及隶属度函数
weight['轻'] = fuzz.trimf(weight.universe, [0, 0, 10])
weight['中等'] = fuzz.trimf(weight.universe, [0, 10, 20])
weight['重'] = fuzz.trimf(weight.universe, [10, 20, 20])

dirt['轻微'] = fuzz.trimf(dirt.universe, [0, 0, 50])
dirt['中等'] = fuzz.trimf(dirt.universe, [0, 50, 100])
dirt['严重'] = fuzz.trimf(dirt.universe, [50, 100, 100])

wash_time['极短'] = fuzz.trimf(wash_time.universe, [0, 0, 15])
wash_time['短'] = fuzz.trimf(wash_time.universe, [0, 15, 30])
wash_time['中等'] = fuzz.trimf(wash_time.universe, [15, 30, 45])
wash_time['长'] = fuzz.trimf(wash_time.universe, [30, 45, 60])
wash_time['极长'] = fuzz.trimf(wash_time.universe, [45, 60, 60])

# 3. 模糊控制规则的设订
rule1 = ctrl.Rule(weight['轻'] & dirt['轻微'], wash_time['极短'])
rule2 = ctrl.Rule(weight['轻'] & dirt['中等'], wash_time['短'])
rule3 = ctrl.Rule(weight['轻'] & dirt['严重'], wash_time['中等'])
rule4 = ctrl.Rule(weight['中等'] & dirt['轻微'], wash_time['短'])
rule5 = ctrl.Rule(weight['中等'] & dirt['中等'], wash_time['中等'])
rule6 = ctrl.Rule(weight['中等'] & dirt['严重'], wash_time['长'])
rule7 = ctrl.Rule(weight['重'] & dirt['轻微'], wash_time['中等'])
rule8 = ctrl.Rule(weight['重'] & dirt['中等'], wash_time['长'])
rule9 = ctrl.Rule(weight['重'] & dirt['严重'], wash_time['极长'])
# 创建控制系统与仿真器
washing_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
washing_sim = ctrl.ControlSystemSimulation(washing_ctrl)

# 4. 键盘交互输入测试数据
print("--- 欢迎使用模糊控制全自动洗衣机系统 ---")
# 循环获取合法的重量输入
while True:
    try:
        test_weight = float(input("请输入衣物重量 (0 - 20 kg): "))
        if 0 <= test_weight <= 20:
            break
        print("错误：重量必须在 0 到 20 之间，请重新输入！")
    except ValueError:
        print("错误：请输入有效的数字！")
# 循环获取合法的污浊度输入
while True:
    try:
        test_dirt = float(input("请输入污浊程度 (0 - 100 %): "))
        if 0 <= test_dirt <= 100:
            break
        print("错误：污浊程度必须在 0 到 100 之间，请重新输入！")
    except ValueError:
        print("错误：请输入有效的数字！")

# 5. 进行计算与结果输出
washing_sim.input['衣物重量 (kg)'] = test_weight
washing_sim.input['污浊程度 (%)'] = test_dirt
washing_sim.compute()
computed_time = washing_sim.output['洗涤时间 (分钟)']
print("\n" + "="*40)
print(f"输入条件: 衣物重量 = {test_weight} kg, 污浊程度 = {test_dirt}%")
print(f"模糊推理得出的洗涤时间: {computed_time:.2f} 分钟")
print("="*40 + "\n正在生成3D控制曲面图")

# 6. 生成简单易懂的 3D 控制曲面图
x_weight = np.arange(0, 21, 1)
y_dirt = np.arange(0, 101, 5)
x_mesh, y_mesh = np.meshgrid(x_weight, y_dirt)
z_time = np.zeros_like(x_mesh, dtype=float)
# 遍历计算曲面高度
for i in range(x_mesh.shape[0]):
    for j in range(x_mesh.shape[1]):
        washing_sim.input['衣物重量 (kg)'] = x_mesh[i, j]
        washing_sim.input['污浊程度 (%)'] = y_mesh[i, j]
        washing_sim.compute()
        z_time[i, j] = washing_sim.output['洗涤时间 (分钟)']
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(x_mesh, y_mesh, z_time, cmap='viridis', edgecolor='none', alpha=0.9)
# 在3D图中标记用户输入的点
ax.scatter(test_weight, test_dirt, computed_time, color='black', s=100, label=f'您的输入点: {computed_time:.1f}分钟')
ax.set_title('全自动洗衣机模糊控制策略曲面\n(展示衣物重量与污浊度如何共同决定洗涤时间)', fontsize=14, pad=20)
ax.set_xlabel('衣物重量 (kg)', fontsize=12)
ax.set_ylabel('污浊程度 (%)', fontsize=12)
ax.set_zlabel('洗涤时间 (分钟)', fontsize=12)
ax.legend()
fig.colorbar(surf, shrink=0.5, aspect=10, label='时间长短')
plt.show()