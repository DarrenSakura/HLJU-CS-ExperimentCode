import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# 设置 Matplotlib 支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

class TemperatureAnalyzer:
    def __init__(self, data_file="city_temperatures.csv"):
        self.data_file = data_file
        self.df = None

    # 1. 准备气温数据集
    def prepare_dataset(self):
        """如果本地没有数据文件，则自动生成一年的模拟气温数据"""
        if not os.path.exists(self.data_file):
            print(f"正在生成模拟数据集: {self.data_file} ...")
            # 生成一年的日期
            dates = pd.date_range(start="2025-01-01", periods=365)
            
            # 模拟北京、上海、广州的气温变化 (基础温度 + 季节性正弦波动 + 随机噪声)
            days = np.arange(365)
            beijing_temp = 12 + 15 * np.sin(2 * np.pi * (days - 100) / 365) + np.random.normal(0, 3, 365)
            shanghai_temp = 18 + 12 * np.sin(2 * np.pi * (days - 100) / 365) + np.random.normal(0, 2.5, 365)
            guangzhou_temp = 24 + 8 * np.sin(2 * np.pi * (days - 100) / 365) + np.random.normal(0, 2, 365)
            
            # 创建 DataFrame 并保存为 CSV
            df_sim = pd.DataFrame({
                'Date': dates,
                '北京': beijing_temp.round(1),
                '上海': shanghai_temp.round(1),
                '广州': guangzhou_temp.round(1)
            })
            df_sim.to_csv(self.data_file, index=False)
            print("数据集生成完毕！")
            
        # 学习Pandas数据处理：读取数据并将日期列设置为索引
        self.df = pd.read_csv(self.data_file, parse_dates=['Date'], index_col='Date')
        print("\n--- 数据集前5行 ---")
        print(self.df.head())

    # 2. 实现基础统计分析
    def basic_statistics(self):
        """计算各城市的基础统计指标：均值、最高温、最低温等"""
        print("\n=== 基础统计分析 ===")
        # describe() 方法可以快速得到计数、均值、标准差、最小最大值及四分位数
        stats = self.df.describe().round(2)
        print(stats)
        return stats

    # 3. 完成季节和气候分析
    def seasonal_analysis(self):
        """根据月份将数据划分为四季，并计算各季节的平均气温"""
        print("\n=== 季节平均气温分析 ===")
        
        # 提取月份
        month = self.df.index.month
        # 定义季节映射：3-5春，6-8夏，9-11秋，12-2冬
        season_map = {
            1: '冬季', 2: '冬季', 3: '春季', 4: '春季', 5: '春季', 6: '夏季',
            7: '夏季', 8: '夏季', 9: '秋季', 10: '秋季', 11: '秋季', 12: '冬季'
        }
        
        # 添加一列 'Season'
        df_season = self.df.copy()
        df_season['Season'] = month.map(season_map)
        
        # 按季节分组计算平均值
        # 保证输出顺序为春夏秋冬
        season_order = ['春季', '夏季', '秋季', '冬季']
        seasonal_avg = df_season.groupby('Season').mean().reindex(season_order).round(1)
        
        print(seasonal_avg)
        return seasonal_avg

    # 4. 创建多种可视化图表
    def create_visualizations(self, seasonal_avg):
        """绘制全年气温折线图和季节平均气温柱状图"""
        print("\n正在生成可视化图表...")
        
        # 创建一个 1x2 的画布
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        
        # 图1：全年气温变化趋势（折线图）
        axes[0].plot(self.df.index, self.df['北京'], label='北京', alpha=0.7)
        axes[0].plot(self.df.index, self.df['上海'], label='上海', alpha=0.7)
        axes[0].plot(self.df.index, self.df['广州'], label='广州', alpha=0.7)
        axes[0].set_title('各城市全年气温变化趋势')
        axes[0].set_xlabel('日期')
        axes[0].set_ylabel('气温 (℃)')
        axes[0].legend()
        axes[0].grid(True, linestyle='--', alpha=0.6)
        
        # 图2：各季节平均气温（柱状图）
        seasonal_avg.plot(kind='bar', ax=axes[1], alpha=0.8)
        axes[1].set_title('各城市季节平均气温对比')
        axes[1].set_xlabel('季节')
        axes[1].set_ylabel('平均气温 (℃)')
        axes[1].tick_params(axis='x', rotation=0) # X轴标签水平显示
        axes[1].grid(axis='y', linestyle='--', alpha=0.6)
        
        plt.tight_layout()
        
        # 5. 添加数据导出功能 (图表保存)
        chart_file = "temperature_analysis_charts.png"
        plt.savefig(chart_file, dpi=300)
        print(f"图表已保存至: {os.path.abspath(chart_file)}")
        
        # 显示图表
        plt.show()

    # 5. 添加数据导出功能 (数据表格保存)
    def export_results(self, stats, seasonal_avg, export_file="analysis_results.xlsx"):
        """将统计分析结果导出为 Excel 或 CSV (这里为了不引入额外依赖，导出为 CSV)"""
        try:
            # 分别保存基础统计和季节分析结果
            stats.to_csv("basic_statistics.csv")
            seasonal_avg.to_csv("seasonal_analysis.csv")
            print(f"\n分析数据已导出为: basic_statistics.csv 和 seasonal_analysis.csv")
        except Exception as e:
            print(f"导出结果时出错: {e}")

def main():
    analyzer = TemperatureAnalyzer()
    
    # 执行分析流程
    analyzer.prepare_dataset()
    stats = analyzer.basic_statistics()
    seasonal_avg = analyzer.seasonal_analysis()
    
    # 导出并可视化
    analyzer.export_results(stats, seasonal_avg)
    analyzer.create_visualizations(seasonal_avg)

if __name__ == "__main__":
    main()