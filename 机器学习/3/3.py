import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import time
# 设置 Matplotlib 中文字体显示 (适用于 Mac)
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei'] 
plt.rcParams['axes.unicode_minus'] = False  
# 用户ID、物品ID、评分
def load_data(file_path):
    df = pd.read_csv(file_path, sep='\s+', header=None, names=['user_id', 'item_id', 'rating'])
    return df
#路径
train_path = '/Users/darren/Desktop/ML/3/train.txt'
test_path = '/Users/darren/Desktop/ML/3/test.txt'
try:
    train_df = load_data(train_path)
    test_df = load_data(test_path)
    print(f"成功加载数据！训练集共 {len(train_df)} 条，测试集共 {len(test_df)} 条。\n")
except FileNotFoundError as e:
    print(f"文件读取失败，请检查路径：{e}")
    exit()
# 获取用户和物品的数量
num_users = max(train_df['user_id'].max(), test_df['user_id'].max()) + 1
num_items = max(train_df['item_id'].max(), test_df['item_id'].max()) + 1
#矩阵分解(MF)算法模型
class MatrixFactorization:
    def __init__(self, num_users, num_items, k=10, alpha=0.01, beta=0.0, epochs=10):
        self.num_users = num_users
        self.num_items = num_items
        self.k = k            # 隐向量维度
        self.alpha = alpha    # 学习率
        self.beta = beta      # 正则化系数
        self.epochs = epochs  # 将默认 epoch 改小，加快运行速度    
        # 初始化用户和物品的隐向量矩阵
        self.P = np.random.normal(scale=1./self.k, size=(self.num_users, self.k))
        self.Q = np.random.normal(scale=1./self.k, size=(self.num_items, self.k))   
        # 记录训练和测试集的RMSE历史
        self.train_rmse_history = []
        self.test_rmse_history = []    
    def fit(self, train_df, test_df):
        train_data = train_df.values    
        # 跑'epochs'轮迭代
        for epoch in range(self.epochs):
            start_time = time.time()
            np.random.shuffle(train_data)       
            # 遍历训练数据, 更新用户和物品的隐向量
            for user, item, rating in train_data:
                user, item = int(user), int(item)         
                # 取用户 user 的向量 和 物品 item 的向量，做内积
                prediction = np.dot(self.P[user, :], self.Q[item, :].T)
                # 计算误差, 真实 - 预测
                error = rating - prediction
                # 提取用户和物品的隐向量
                P_u = self.P[user, :]
                Q_i = self.Q[item, :]
                # 更新用户和物品的隐向量，考虑正则化项
                self.P[user, :] += self.alpha * (error * Q_i - self.beta * P_u)
                self.Q[item, :] += self.alpha * (error * P_u - self.beta * Q_i)
            # 每轮结束后计算并记录训练集和测试集的 RMSE
            train_rmse = self.calculate_rmse(train_df)
            test_rmse = self.calculate_rmse(test_df)
            self.train_rmse_history.append(train_rmse)
            self.test_rmse_history.append(test_rmse)
            end_time = time.time()
            # 打印当前进度和耗时
            print(f"  [Epoch {epoch+1}/{self.epochs}] 耗时: {end_time - start_time:.2f}s | Train RMSE: {train_rmse:.4f} | Test RMSE: {test_rmse:.4f}")
    def calculate_rmse(self, df):
        # 提取用户ID、物品ID和评分，转换为整型
        users = df['user_id'].values.astype(int)
        items = df['item_id'].values.astype(int)
        ratings = df['rating'].values
        # 两个大矩阵对应位置相乘，然后按行求和 (axis=1)，算预测评分
        predictions = np.sum(self.P[users] * self.Q[items], axis=1)
        # 先算 MSE (均方误差)，再套一层 np.sqrt (开根号)
        return np.sqrt(mean_squared_error(ratings, predictions))
# 不带正则化测试10轮
print("1.运行不带正则化的 MF (beta=0.0) ")
mf_unreg = MatrixFactorization(num_users, num_items, k=10, alpha=0.01, beta=0.0, epochs=10)
mf_unreg.fit(train_df, test_df)
print(f"不带正则化的最终测试集的RMSE: {mf_unreg.test_rmse_history[-1]:.4f}\n")
# 带正则化测试10轮
print("2.运行带正则化的 MF (beta=0.1) ")
mf_reg = MatrixFactorization(num_users, num_items, k=10, alpha=0.01, beta=0.1, epochs=10)
mf_reg.fit(train_df, test_df)
print(f"带正则化的最终测试集的RMSE: {mf_reg.test_rmse_history[-1]:.4f}\n")
# 对模型调参，计算最优的 RMSE 值
print("3.进行调参")
# 候选参数列表
param_grid = [
    {'k': 10, 'beta': 0.05},
    {'k': 20, 'beta': 0.05},
    {'k': 10, 'beta': 0.1},
    {'k': 20, 'beta': 0.1}
]
best_rmse = float('inf')
best_params = None
tuning_results = []
# 用 for 循环试每个组合，记录每个组合的RMSE
for params in param_grid:
    print(f"正在训练模型: 隐向量维度 k={params['k']}, 正则化系数 beta={params['beta']}...")
    model = MatrixFactorization(num_users, num_items, k=params['k'], alpha=0.01, beta=params['beta'], epochs=10)
    model.fit(train_df, test_df)
    # 获取当前组合的最终测试集 RMSE
    final_test_rmse = model.test_rmse_history[-1]
    tuning_results.append((params, model.test_rmse_history))
    # 更新最佳参数组合和 RMSE
    if final_test_rmse < best_rmse:
        best_rmse = final_test_rmse
        best_params = params
print(f"\n>> 最佳参数组合: {best_params}, 最优测试集 RMSE: {best_rmse:.4f}\n")
#数据可视化
print("4.生成可视化图表")
plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
plt.plot(mf_unreg.test_rmse_history, label='无正则化 (beta=0.0)', linestyle='--')
plt.plot(mf_reg.test_rmse_history, label='带正则化 (beta=0.1)')
plt.title("有无正则化的测试集对比")
plt.xlabel("迭代次数 (Epochs)")
plt.ylabel("测试集的RMSE值")
plt.legend()
plt.grid(True)
plt.subplot(1, 2, 2)
for params, history in tuning_results:
    label = f"k={params['k']}, beta={params['beta']}"
    if params == best_params:
        plt.plot(history, label=f"{label} (最佳组合)", linewidth=2.5)
    else:
        plt.plot(history, label=label, alpha=0.7)
plt.title("不同超参数组合测试集的调参过程")
plt.xlabel("迭代次数 (Epochs)")
plt.ylabel("测试集的RMSE值")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()