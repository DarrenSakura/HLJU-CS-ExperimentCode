import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import os

# ==========================================
# 设置 Matplotlib 中文字体显示
# ==========================================
# 'SimHei' 适用于 Windows，'Arial Unicode MS' 适用于 Mac，'Microsoft YaHei' 是备选
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS'] 
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# ==========================================
# 数据加载与预处理
# ==========================================
def load_data(file_path):
    # 假设数据格式为: user_id, item_id, rating
    df = pd.read_csv(file_path, sep='\s+', header=None, names=['user_id', 'item_id', 'rating'])
    return df

# 获取桌面路径
desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
train_path = os.path.join(desktop_path, 'train.txt')
test_path = os.path.join(desktop_path, 'test.txt')

# 加载数据（为了防止报错，如果桌面没文件会自动生成模拟数据）
try:
    train_df = load_data(train_path)
    test_df = load_data(test_path)
    print("成功加载桌面上的 train.txt 和 test.txt")
except FileNotFoundError:
    print("未在桌面找到文件，生成随机模拟数据进行演示...")
    train_df = pd.DataFrame({'user_id': np.random.randint(0, 100, 1000), 
                             'item_id': np.random.randint(0, 100, 1000), 
                             'rating': np.random.randint(1, 6, 1000)})
    test_df = pd.DataFrame({'user_id': np.random.randint(0, 100, 200), 
                            'item_id': np.random.randint(0, 100, 200), 
                            'rating': np.random.randint(1, 6, 200)})

num_users = max(train_df['user_id'].max(), test_df['user_id'].max()) + 1
num_items = max(train_df['item_id'].max(), test_df['item_id'].max()) + 1

# ==========================================
# 步骤1 & 步骤2：矩阵分解(MF)算法模型定义
# ==========================================
class MatrixFactorization:
    def __init__(self, num_users, num_items, k=10, alpha=0.01, beta=0.0, epochs=50):
        self.num_users = num_users
        self.num_items = num_items
        self.k = k            
        self.alpha = alpha    
        self.beta = beta      
        self.epochs = epochs  
        
        self.P = np.random.normal(scale=1./self.k, size=(self.num_users, self.k))
        self.Q = np.random.normal(scale=1./self.k, size=(self.num_items, self.k))
        
        self.train_rmse_history = []
        self.test_rmse_history = []
        
    def fit(self, train_df, test_df):
        train_data = train_df.values
        for epoch in range(self.epochs):
            np.random.shuffle(train_data)
            for user, item, rating in train_data:
                user, item = int(user), int(item)
                
                prediction = np.dot(self.P[user, :], self.Q[item, :].T)
                error = rating - prediction
                
                P_u = self.P[user, :]
                Q_i = self.Q[item, :]
                
                self.P[user, :] += self.alpha * (error * Q_i - self.beta * P_u)
                self.Q[item, :] += self.alpha * (error * P_u - self.beta * Q_i)
            
            self.train_rmse_history.append(self.calculate_rmse(train_df))
            self.test_rmse_history.append(self.calculate_rmse(test_df))
            
    def calculate_rmse(self, df):
        users = df['user_id'].values.astype(int)
        items = df['item_id'].values.astype(int)
        ratings = df['rating'].values
        predictions = np.sum(self.P[users] * self.Q[items], axis=1)
        return np.sqrt(mean_squared_error(ratings, predictions))


print("=== 步骤1：运行不带正则化的 MF (beta=0.0) ===")
mf_unreg = MatrixFactorization(num_users, num_items, k=10, alpha=0.01, beta=0.0, epochs=30)
mf_unreg.fit(train_df, test_df)
print(f"不带正则化 - 最终测试集 RMSE: {mf_unreg.test_rmse_history[-1]:.4f}\n")

print("=== 步骤2：运行带正则化的 MF (beta=0.1) ===")
mf_reg = MatrixFactorization(num_users, num_items, k=10, alpha=0.01, beta=0.1, epochs=30)
mf_reg.fit(train_df, test_df)
print(f"带正则化 - 最终测试集 RMSE: {mf_reg.test_rmse_history[-1]:.4f}\n")

# ==========================================
# 步骤3：对推荐模型调参，计算最优的 RMSE 值
# ==========================================
print("=== 步骤3：进行超参数搜索 (调参) ===")
param_grid = [
    {'k': 5, 'beta': 0.05},
    {'k': 10, 'beta': 0.1},
    {'k': 20, 'beta': 0.1},
    {'k': 20, 'beta': 0.2}
]

best_rmse = float('inf')
best_params = None
tuning_results = []

for params in param_grid:
    print(f"正在训练模型: 隐向量维度 k={params['k']}, 正则化系数 beta={params['beta']}...")
    model = MatrixFactorization(num_users, num_items, k=params['k'], alpha=0.01, beta=params['beta'], epochs=40)
    model.fit(train_df, test_df)
    
    final_test_rmse = model.test_rmse_history[-1]
    tuning_results.append((params, model.test_rmse_history))
    
    if final_test_rmse < best_rmse:
        best_rmse = final_test_rmse
        best_params = params

print(f"\n>> 最佳参数组合: {best_params}, 最优测试集 RMSE: {best_rmse:.4f}\n")

# ==========================================
# 步骤4：数据可视化 (全中文)
# ==========================================
print("=== 步骤4：生成可视化图表 ===")
plt.figure(figsize=(14, 6))

# 子图1：不带正则化 vs 带正则化的验证集 RMSE 对比
plt.subplot(1, 2, 1)
plt.plot(mf_unreg.test_rmse_history, label='无正则化 (beta=0.0)', linestyle='--')
plt.plot(mf_reg.test_rmse_history, label='带正则化 (beta=0.1)')
plt.title("步骤1 & 2：有无正则化的测试集 RMSE 对比")
plt.xlabel("迭代次数 (Epochs)")
plt.ylabel("测试集 RMSE")
plt.legend()
plt.grid(True)

# 子图2：调参过程中不同参数组合的测试集 RMSE 下降曲线
plt.subplot(1, 2, 2)
for params, history in tuning_results:
    label = f"k={params['k']}, beta={params['beta']}"
    # 高亮最佳参数组
    if params == best_params:
        plt.plot(history, label=f"{label} (最佳组合)", linewidth=2.5)
    else:
        plt.plot(history, label=label, alpha=0.7)

plt.title("步骤3：不同超参数组合的测试集 RMSE 调参过程")
plt.xlabel("迭代次数 (Epochs)")
plt.ylabel("测试集 RMSE")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()