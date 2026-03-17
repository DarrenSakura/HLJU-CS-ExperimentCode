import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix

from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

# 设置中文字体以便在Mac的图表中显示中文
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

def run_ml_pipeline(X, y, dataset_name):
    print(f"\n{'='*50}")
    print(f"开始处理数据集: {dataset_name}")
    print(f"{'='*50}")

    # ==========================================
    # 步骤1：实现数据的预处理
    # ==========================================
    # 划分训练集和测试集 (70%训练，30%测试)，不使用交叉验证
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # 数据标准化 (Z-score归一化)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print(f"[预处理] 训练集大小: {X_train.shape}，测试集大小: {X_test.shape}")

    # ==========================================
    # 步骤2 & 6：KNN分类器及其调参
    # ==========================================
    knn_k_range = range(1, 21)
    knn_scores = []
    for k in knn_k_range:
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(X_train_scaled, y_train)
        knn_scores.append(accuracy_score(y_test, knn.predict(X_test_scaled)))
    best_k = knn_k_range[np.argmax(knn_scores)]
    best_knn_acc = max(knn_scores)
    print(f"[KNN] 最佳 K = {best_k}, 准确率 = {best_knn_acc:.4f}")

    # ==========================================
    # 步骤3 & 6：贝叶斯分类器
    # ==========================================
    nb = GaussianNB()
    nb.fit(X_train_scaled, y_train)
    y_pred_nb = nb.predict(X_test_scaled) # 保存预测结果用于画混淆矩阵
    best_nb_acc = accuracy_score(y_test, y_pred_nb)
    print(f"[Naive Bayes] 准确率 = {best_nb_acc:.4f}")

    # ==========================================
    # 步骤4 & 6：决策树分类器及其调参
    # ==========================================
    dt_depth_range = range(1, 16)
    dt_scores = []
    for depth in dt_depth_range:
        dt = DecisionTreeClassifier(max_depth=depth, random_state=42)
        dt.fit(X_train_scaled, y_train)
        dt_scores.append(accuracy_score(y_test, dt.predict(X_test_scaled)))
    best_depth = dt_depth_range[np.argmax(dt_scores)]
    best_dt_acc = max(dt_scores)
    print(f"[Decision Tree] 最佳 max_depth = {best_depth}, 准确率 = {best_dt_acc:.4f}")

    # ==========================================
    # 步骤5 & 6：SVM分类器及其调参
    # ==========================================
    svm_c_range = [0.001, 0.01, 0.1, 1, 10, 100]
    svm_scores = []
    for c in svm_c_range:
        svm = SVC(C=c, kernel='rbf', random_state=42)
        svm.fit(X_train_scaled, y_train)
        svm_scores.append(accuracy_score(y_test, svm.predict(X_test_scaled)))
    best_c = svm_c_range[np.argmax(svm_scores)]
    best_svm_acc = max(svm_scores)
    print(f"[SVM] 最佳 C = {best_c}, 准确率 = {best_svm_acc:.4f}")

    # ==========================================
    # 步骤7：数据可视化 (3个模型调参 + 贝叶斯混淆矩阵)
    # ==========================================
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f'数据集: {dataset_name} - 模型调参及验证可视化', fontsize=16)

    # 1. KNN调参图
    axes[0, 0].plot(knn_k_range, knn_scores, marker='o', color='b')
    axes[0, 0].set_title("KNN: 准确率 vs 邻居数(K)")
    axes[0, 0].set_xlabel("n_neighbors (K)")
    axes[0, 0].set_ylabel("Accuracy")
    axes[0, 0].grid(True)

    # 2. 决策树调参图
    axes[0, 1].plot(dt_depth_range, dt_scores, marker='s', color='g')
    axes[0, 1].set_title("决策树: 准确率 vs 最大深度(max_depth)")
    axes[0, 1].set_xlabel("max_depth")
    axes[0, 1].set_ylabel("Accuracy")
    axes[0, 1].grid(True)

    # 3. SVM调参图
    axes[1, 0].plot(svm_c_range, svm_scores, marker='^', color='r')
    axes[1, 0].set_xscale('log')
    axes[1, 0].set_title("SVM: 准确率 vs 惩罚系数(C)")
    axes[1, 0].set_xlabel("C (log scale)")
    axes[1, 0].set_ylabel("Accuracy")
    axes[1, 0].grid(True)

    # 4. 朴素贝叶斯 验证结果可视化 (混淆矩阵)
    cm = confusion_matrix(y_test, y_pred_nb)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[1, 1], cbar=False)
    axes[1, 1].set_title(f"朴素贝叶斯: 测试集混淆矩阵 (Acc: {best_nb_acc:.4f})")
    axes[1, 1].set_xlabel("预测类别 (Predicted)")
    axes[1, 1].set_ylabel("真实类别 (True)")

    plt.tight_layout()
    plt.show()

def main():
    try:
        # 处理 Iris 数据集
        df_iris = pd.read_csv('iris.data', header=None)
        X_iris = df_iris.iloc[:, :-1].values
        # 将字符串标签转换为数字
        y_iris = LabelEncoder().fit_transform(df_iris.iloc[:, -1].values)
        run_ml_pipeline(X_iris, y_iris, "Iris Dataset")
    except FileNotFoundError:
        print("未找到 iris.data，请检查文件路径。")

    try:
        # 处理 Wine 数据集
        df_wine = pd.read_csv('wine.data', header=None)
        X_wine = df_wine.iloc[:, 1:].values
        y_wine = df_wine.iloc[:, 0].values
        run_ml_pipeline(X_wine, y_wine, "Wine Dataset")
    except FileNotFoundError:
        print("未找到 wine.data，请检查文件路径。")

if __name__ == "__main__":
    main()